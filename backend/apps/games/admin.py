from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.html import format_html

from .models import Game, GameTeam, GamePlayer


class GameTeamInline(admin.TabularInline):
    """
    Inline admin for GameTeam to show teams within a Game.
    """
    model = GameTeam
    extra = 1
    max_num = 2
    fields = ('team', 'designation')


class GamePlayerInline(admin.TabularInline):
    """
    Inline admin for GamePlayer to show players within a GameTeam.
    """
    model = GamePlayer
    extra = 0
    fields = ('player', 'is_captain_for_game', 'position', 'notes')
    readonly_fields = ('created_at', 'updated_at')


class GameTeamAdmin(admin.ModelAdmin):
    """
    Admin for the GameTeam model, representing teams in a game.
    """
    list_display = ['id', 'game', 'team', 'designation', 'get_player_count']
    list_filter = ['designation', 'team']
    search_fields = ['game__name', 'team__name']
    inlines = [GamePlayerInline]
    
    def get_player_count(self, obj):
        """Return count of selected players for this game team"""
        return obj.selected_players.count()
    get_player_count.short_description = _('Selected Players')
    

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """
    Admin for the Game model, representing scheduled games.
    """
    list_display = [
        'name', 'sport_event', 'location', 'start_datetime', 
        'status', 'get_teams', 'scorekeeper'
    ]
    list_filter = [
        'status', 'sport_event', 'start_datetime'
    ]
    search_fields = [
        'name', 'description', 'location', 'sport_event__name'
    ]
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
    date_hierarchy = 'start_datetime'
    inlines = [GameTeamInline]
    
    fieldsets = (
        (None, {
            'fields': ('sport_event', 'name', 'description', 'location')
        }),
        (_('Schedule'), {
            'fields': ('start_datetime', 'end_datetime', 'status')
        }),
        (_('Scoring'), {
            'fields': ('scorekeeper',)
        }),
        (_('Metadata'), {
            'fields': ('created_by', 'created_at', 'updated_by', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_teams(self, obj):
        """Return team names for the game"""
        if not hasattr(obj, 'game_teams'):
            return "-"
            
        teams = obj.game_teams.all()
        if teams.count() == 0:
            return "-"
            
        team_names = []
        for game_team in teams:
            team_names.append(
                format_html(
                    '<a href="{}">{}</a> ({})',
                    reverse('admin:teams_team_change', args=[game_team.team.id]),
                    game_team.team.name,
                    game_team.get_designation_display()
                )
            )
        return format_html(' vs '.join(team_names))
    get_teams.short_description = _('Teams')
    
    def save_model(self, request, obj, form, change):
        """Set created_by and updated_by fields"""
        if not change:  # New object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        """Optimize queryset to reduce number of database queries"""
        queryset = super().get_queryset(request)
        return queryset.select_related(
            'sport_event', 'scorekeeper', 'created_by', 'updated_by'
        ).prefetch_related(
            'game_teams__team'
        )


@admin.register(GameTeam)
class GameTeamAdmin(admin.ModelAdmin):
    """
    Admin for the GameTeam model, representing teams participating in a game.
    """
    list_display = ['id', 'game', 'team', 'designation', 'get_player_count']
    list_filter = ['designation', 'game__status']
    search_fields = ['game__name', 'team__name']
    inlines = [GamePlayerInline]
    
    def get_player_count(self, obj):
        """Return count of selected players for this game team"""
        return obj.selected_players.count()
    get_player_count.short_description = _('Selected Players')


@admin.register(GamePlayer)
class GamePlayerAdmin(admin.ModelAdmin):
    """
    Admin for the GamePlayer model, representing players selected for a game.
    """
    list_display = [
        'id', 'get_game_name', 'get_team_name', 'player', 
        'is_captain_for_game', 'position'
    ]
    list_filter = [
        'is_captain_for_game', 'game_team__team', 
        'game_team__game__status'
    ]
    search_fields = [
        'player__first_name', 'player__last_name', 
        'game_team__game__name', 'position', 'notes'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (None, {
            'fields': ('game_team', 'player')
        }),
        (_('Role Information'), {
            'fields': ('is_captain_for_game', 'position')
        }),
        (_('Additional Information'), {
            'fields': ('notes',)
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_game_name(self, obj):
        """Return game name for the player selection"""
        if not obj.game_team or not obj.game_team.game:
            return "-"
            
        return format_html(
            '<a href="{}">{}</a>',
            reverse('admin:games_game_change', args=[obj.game_team.game.id]),
            obj.game_team.game.name
        )
    get_game_name.short_description = _('Game')
    get_game_name.admin_order_field = 'game_team__game__name'
    
    def get_team_name(self, obj):
        """Return team name for the player selection"""
        if not obj.game_team or not obj.game_team.team:
            return "-"
            
        return format_html(
            '<a href="{}">{}</a>',
            reverse('admin:teams_team_change', args=[obj.game_team.team.id]),
            obj.game_team.team.name
        )
    get_team_name.short_description = _('Team')
    get_team_name.admin_order_field = 'game_team__team__name'