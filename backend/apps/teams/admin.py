from django.contrib import admin
from django.contrib import messages
from django.contrib.admin import SimpleListFilter
from .models import Team, Player, TeamRegistration

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'team_captain', 'status', 'player_count', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'description', 'manager__username', 'manager__email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'logo', 'description')
        }),
        ('Management', {
            'fields': ('manager', 'team_captain', 'status')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def player_count(self, obj):
        return obj.players.filter(is_active=True).count()
    player_count.short_description = 'Active Players'

class TeamFilter(SimpleListFilter):
    title = 'team'
    parameter_name = 'team'
    
    def lookups(self, request, model_admin):
        teams = Team.objects.all()
        return [(team.id, team.name) for team in teams]
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(team__id=self.value())
        return queryset


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'team', 'jersey_number', 'position', 'is_captain', 'is_active')
    list_filter = (TeamFilter, 'is_active', 'is_captain', 'joined_date')
    search_fields = ('first_name', 'last_name', 'team__name', 'position', 'user__email', 'user__username')
    readonly_fields = ('created_at', 'updated_at', 'first_name', 'last_name')
    fieldsets = (
        ('Required Information', {
            'fields': ('team', 'user', 'jersey_number', 'date_of_birth', 'joined_date')
        }),
        ('Player Information', {
            'fields': ('position', 'is_captain', 'is_active')
        }),
        ('Personal Details', {
            'fields': ('first_name', 'last_name', 'photo'),
            'description': 'First and last name are automatically populated from the user account if selected.',
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        """Return player's full name or placeholder if empty"""
        if obj.first_name and obj.last_name:
            return f"{obj.first_name} {obj.last_name}"
        elif obj.first_name:
            return obj.first_name
        elif obj.last_name:
            return obj.last_name
        elif obj.user:
            # Если имя не установлено, но есть пользователь, используем имя пользователя
            return f"{obj.user.first_name} {obj.user.last_name}"
        else:
            return "Player without name"
    get_full_name.short_description = 'Player Name'
    
    def save_model(self, request, obj, form, change):
        """
        Проверяем и обновляем данные игрока при сохранении.
        """
        # Если выбран пользователь и не установлены имя и фамилия, берем их из данных пользователя
        if obj.user:
            if not obj.first_name:
                obj.first_name = obj.user.first_name
            if not obj.last_name:
                obj.last_name = obj.user.last_name
                
        # Если выбраны first_name и last_name для игрока без пользователя, используем их
        
        # Проверить уникальность номера в команде
        if Player.objects.filter(team=obj.team, jersey_number=obj.jersey_number).exclude(id=obj.id).exists():
            messages.error(request, f'Номер {obj.jersey_number} уже используется другим игроком в этой команде')
            return
        
        super().save_model(request, obj, form, change)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Пользовательская фильтрация выпадающих списков
        if db_field.name == "user":
            # Получаем ID пользователей, которые уже привязаны к любым игрокам
            used_users = Player.objects.exclude(user=None).values_list('user_id', flat=True)
            
            # Фильтруем пользователей с ролью "player", которые еще не привязаны к игрокам
            kwargs["queryset"] = db_field.related_model.objects.filter(
                role='player'
            ).exclude(
                id__in=used_users
            )
            
            # Если редактируем существующего игрока, включаем его пользователя в выборку
            if request.resolver_match.kwargs.get('object_id'):
                try:
                    player = Player.objects.get(id=request.resolver_match.kwargs['object_id'])
                    if player.user:
                        kwargs["queryset"] = kwargs["queryset"] | db_field.related_model.objects.filter(id=player.user.id)
                except Player.DoesNotExist:
                    pass
        
        elif db_field.name == "team":
            # Создаем кастомное поле для команд
            from django.forms.models import ModelChoiceField
            from django.db.models import Count
            
            class TeamWithPlayerCountField(ModelChoiceField):
                def label_from_instance(self, obj):
                    # Получаем количество игроков для каждой команды при отображении
                    player_count = Player.objects.filter(team=obj).count()
                    return f"{obj.name} ({player_count} players)"
            
            # Получаем все команды
            teams = Team.objects.all()
            
            # Если есть максимальное количество игроков, можно отфильтровать команды
            # MAX_PLAYERS_PER_TEAM = 20
            # teams_with_count = {team.id: Player.objects.filter(team=team).count() for team in teams}
            # filtered_teams = [team for team in teams if teams_with_count[team.id] < MAX_PLAYERS_PER_TEAM]
            # teams = Team.objects.filter(id__in=[team.id for team in filtered_teams])
            
            kwargs["queryset"] = teams
            
            # Если редактируем существующего игрока, включаем его команду в выборку
            if request.resolver_match.kwargs.get('object_id'):
                try:
                    player = Player.objects.get(id=request.resolver_match.kwargs['object_id'])
                    if player.team and player.team not in teams:
                        kwargs["queryset"] = kwargs["queryset"] | Team.objects.filter(id=player.team.id)
                except Player.DoesNotExist:
                    pass
            
            # Возвращаем наше кастомное поле
            return TeamWithPlayerCountField(**kwargs)
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(TeamRegistration)
class TeamRegistrationAdmin(admin.ModelAdmin):
    list_display = ('team', 'sport_event', 'status', 'registration_date', 'approved_by')
    list_filter = ('status', 'registration_date', 'approval_date')
    search_fields = ('team__name', 'sport_event__name', 'notes')
    readonly_fields = ('registration_date', 'created_at', 'updated_at')
    fieldsets = (
        ('Registration Information', {
            'fields': ('team', 'sport_event', 'status', 'registration_date')
        }),
        ('Approval Information', {
            'fields': ('approved_by', 'approval_date', 'notes')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # Automatically set approved_by to the current user
        # if the status is changed to "approved"
        if 'status' in form.changed_data and obj.status == 'approved':
            obj.approved_by = request.user
        super().save_model(request, obj, form, change)