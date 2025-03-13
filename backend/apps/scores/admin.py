from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html

from .models import Score, ScoreDetail


class ScoreDetailInline(admin.TabularInline):
    """
    Inline admin for ScoreDetails to show scoring events within a Score.
    """
    model = ScoreDetail
    extra = 0
    readonly_fields = ['created_at', 'created_by']
    autocomplete_fields = ['player', 'assisted_by']
    fieldsets = (
        (None, {
            'fields': ('team', 'player', 'assisted_by', 'points', 'event_type')
        }),
        (_('Time Information'), {
            'fields': ('time_occurred', 'minute', 'period')
        }),
        (_('Additional Information'), {
            'fields': ('description', 'video_url', 'created_by', 'created_at')
        }),
    )


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    """
    Admin for the Score model, representing the overall score for a game.
    """
    list_display = [
        'get_game_name', 'get_teams', 'get_score_display', 'status', 
        'verification_status', 'scorekeeper', 'created_at'
    ]
    list_filter = [
        'status', 'verification_status', 'is_draw', 
        'game__sport_event__name', 'created_at'
    ]
    search_fields = [
        'game__name', 'notes', 'game__sport_event__name',
        'game__game_teams__team__name'
    ]
    readonly_fields = [
        'created_at', 'updated_at', 'verified_at', 'winner', 
        'is_draw', 'goal_difference_team1', 'goal_difference_team2'
    ]
    autocomplete_fields = ['game', 'scorekeeper', 'verified_by']
    date_hierarchy = 'created_at'
    inlines = [ScoreDetailInline]
    actions = ['mark_as_verified', 'mark_as_pending_verification']
    
    fieldsets = (
        (None, {
            'fields': ('game', 'status', 'scorekeeper')
        }),
        (_('Score Information'), {
            'fields': (
                ('final_score_team1', 'final_score_team2'), 
                ('goals_for_team1', 'goals_against_team1'), 
                ('goals_for_team2', 'goals_against_team2'),
                ('goal_difference_team1', 'goal_difference_team2'),
                'time_elapsed', 'winner', 'is_draw'
            )
        }),
        (_('Verification'), {
            'fields': ('verification_status', 'verified_by', 'verified_at', 'notes')
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_game_name(self, obj):
        """Return game name with link to game detail page"""
        if obj.game:
            return format_html(
                '<a href="{}">{}</a>',
                reverse('admin:games_game_change', args=[obj.game.id]),
                obj.game.name
            )
        return "-"
    get_game_name.short_description = _('Game')
    get_game_name.admin_order_field = 'game__name'
    
    def get_teams(self, obj):
        """Return team names for the game"""
        if not hasattr(obj.game, 'game_teams'):
            return "-"
            
        teams = obj.game.game_teams.all()
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
    
    def get_score_display(self, obj):
        """Return formatted score display"""
        if obj.final_score_team1 is None or obj.final_score_team2 is None:
            return "-"
            
        return f"{obj.final_score_team1} - {obj.final_score_team2}"
    get_score_display.short_description = _('Score')
    
    def goal_difference_team1(self, obj):
        return obj.calculate_goal_difference(1)
    goal_difference_team1.short_description = _('Goal Difference Team 1')
    
    def goal_difference_team2(self, obj):
        return obj.calculate_goal_difference(2)
    goal_difference_team2.short_description = _('Goal Difference Team 2')
    
    def mark_as_verified(self, request, queryset):
        """Mark selected scores as verified"""
        for score in queryset:
            if score.status == 'completed':
                score.verification_status = 'verified'
                score.verified_by = request.user
                score.save(update_fields=['verification_status', 'verified_by'])
    mark_as_verified.short_description = _("Mark selected scores as verified")
    
    def mark_as_pending_verification(self, request, queryset):
        """Mark selected scores as pending verification"""
        queryset.update(verification_status='pending_verification')
    mark_as_pending_verification.short_description = _("Mark selected scores as pending verification")
    
    def get_queryset(self, request):
        """Optimize queryset to reduce number of database queries"""
        queryset = super().get_queryset(request)
        return queryset.select_related(
            'game', 'scorekeeper', 'verified_by', 'winner'
        ).prefetch_related(
            'game__game_teams__team'
        )
    
    def save_model(self, request, obj, form, change):
        """Auto-determine winner and is_draw based on scores"""
        if obj.status == 'completed' and obj.final_score_team1 is not None and obj.final_score_team2 is not None:
            winner = obj.determine_winner()
            if winner:
                obj.winner = winner
                obj.is_draw = False
            else:
                obj.winner = None
                obj.is_draw = True
                
        super().save_model(request, obj, form, change)
    
    def save_formset(self, request, form, formset, change):
        """Set created_by for new score details"""
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, ScoreDetail) and not instance.pk:
                instance.created_by = request.user
            instance.save()
        formset.save_m2m()


@admin.register(ScoreDetail)
class ScoreDetailAdmin(admin.ModelAdmin):
    """
    Admin for the ScoreDetail model, representing individual scoring events.
    """
    list_display = [
        'id', 'get_score_game', 'team', 'player', 'event_type', 
        'points', 'time_occurred', 'minute', 'created_at'
    ]
    list_filter = [
        'event_type', 'score__status', 'team', 'created_at'
    ]
    search_fields = [
        'score__game__name', 'player__first_name', 'player__last_name', 
        'team__name', 'description', 'period'
    ]
    readonly_fields = ['created_at', 'created_by']
    autocomplete_fields = ['score', 'team', 'player', 'assisted_by']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (None, {
            'fields': ('score', 'team', 'player', 'assisted_by')
        }),
        (_('Scoring Information'), {
            'fields': ('points', 'event_type', 'time_occurred', 'minute', 'period')
        }),
        (_('Additional Information'), {
            'fields': ('description', 'video_url')
        }),
        (_('Metadata'), {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_score_game(self, obj):
        """Return game name for the score"""
        if not obj.score or not obj.score.game:
            return "-"
            
        return format_html(
            '<a href="{}">{}</a>',
            reverse('admin:games_game_change', args=[obj.score.game.id]),
            obj.score.game.name
        )
    get_score_game.short_description = _('Game')
    get_score_game.admin_order_field = 'score__game__name'
    
    def save_model(self, request, obj, form, change):
        """Set created_by for new score details"""
        if not obj.pk:  # New record
            obj.created_by = request.user
        super().save_model(request, obj, form, change)