from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.html import format_html
from django.utils import timezone
from django.db.models import Count, Q
from .models import Leaderboard, LeaderboardEntry


class LeaderboardEntryInline(admin.TabularInline):
    """
    Inline admin for LeaderboardEntries within a Leaderboard.
    Shows team standings directly on the leaderboard page.
    """
    model = LeaderboardEntry
    extra = 0
    readonly_fields = [
        'position', 'team', 'played', 'won', 'drawn', 'lost', 
        'points', 'goals_for', 'goals_against', 'goal_difference',
        'clean_sheets', 'yellow_cards', 'red_cards'
    ]
    ordering = ['position']
    max_num = 0  # Prevent adding new entries manually
    can_delete = False  # Prevent deleting entries manually
    
    # Make the inline display more compact for better overview
    # fields = [
        #'position', 'team', 'played', 'won', 'drawn', 'lost', 
        #'points', 'goal_difference', 'goals_for', 'goals_against'
    #]
    
    # Show additional fields in expanded view
    fieldsets = [
        (None, {
            'fields': [
                'position', 'team', 'played', 'won', 'drawn', 'lost', 
                'points', 'goal_difference'
            ]
        }),
        (_('Detailed Stats'), {
            'fields': [
                'goals_for', 'goals_against', 'clean_sheets', 
                'yellow_cards', 'red_cards'
            ],
            'classes': ['collapse']
        })
    ]


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """
    Admin interface for Leaderboard model.
    Provides comprehensive management of tournament standings.
    """
    list_display = [
        'get_sport_event_name', 'get_sport_type', 'get_entries_count', 
        'is_final', 'last_updated', 'get_update_status'
    ]
    list_filter = [
        'is_final', 'sport_event__sport_type', 
        ('last_updated', admin.DateFieldListFilter)
    ]
    search_fields = ['sport_event__name', 'sport_event__description']
    readonly_fields = ['last_updated', 'get_update_status', 'get_sport_type']
    inlines = [LeaderboardEntryInline]
    actions = ['recalculate_leaderboards', 'finalize_leaderboards', 'unfinalize_leaderboards']
    date_hierarchy = 'last_updated'
    
    fieldsets = [
        (None, {
            'fields': ['sport_event', 'is_final']
        }),
        (_('Status Information'), {
            'fields': ['last_updated', 'get_update_status']
        })
    ]
    
    def get_sport_event_name(self, obj):
        """Return a clickable link to the sport event"""
        if obj.sport_event:
            return format_html(
                '<a href="{}">{}</a>',
                reverse('admin:events_sportevent_change', args=[obj.sport_event.id]),
                obj.sport_event.name
            )
        return "-"
    get_sport_event_name.short_description = _('Sport Event')
    get_sport_event_name.admin_order_field = 'sport_event__name'
    
    def get_sport_type(self, obj):
        """Return the sport type of the event"""
        if obj.sport_event:
            return obj.sport_event.get_sport_type_display()
        return "-"
    get_sport_type.short_description = _('Sport Type')
    get_sport_type.admin_order_field = 'sport_event__sport_type'
    
    def get_entries_count(self, obj):
        """Return the number of entries in the leaderboard"""
        return obj.entries.count()
    get_entries_count.short_description = _('Teams')
    
    def get_update_status(self, obj):
        """Return formatted last update status with visual indicator"""
        if not obj.last_updated:
            return format_html('<span style="color: #999;">Not updated yet</span>')
        
        time_diff = timezone.now() - obj.last_updated
        hours_diff = time_diff.total_seconds() / 3600
        
        # Get count of games that happened after the last update
        from games.models import Game
        recent_games = Game.objects.filter(
            sport_event=obj.sport_event,
            status='completed',
            score__verification_status='verified',
            updated_at__gt=obj.last_updated
        ).count()
        
        if hours_diff < 1 and recent_games == 0:
            return format_html('<span style="color: green;">Up to date</span>')
        elif recent_games > 0:
            return format_html(
                '<span style="color: red;">{} new game results since last update</span>',
                recent_games
            )
        elif hours_diff > 24:
            return format_html(
                '<span style="color: orange;">Last updated {} days ago</span>',
                int(hours_diff // 24)
            )
        else:
            return format_html(
                '<span style="color: blue;">Last updated {} hours ago</span>',
                int(hours_diff)
            )
    get_update_status.short_description = _('Update Status')
    
    def recalculate_leaderboards(self, request, queryset):
        """
        Admin action to recalculate the selected leaderboards.
        """
        from django.contrib import messages
        
        success_count = 0
        warning_count = 0
        error_count = 0
        
        for leaderboard in queryset:
            try:
                updated_entries = self._calculate_leaderboard(leaderboard)
                
                if updated_entries is None:
                    # No games found
                    warning_count += 1
                    continue
                
                success_count += 1
                messages.success(
                    request, 
                    _(f"Successfully recalculated leaderboard for {leaderboard.sport_event.name} with {len(updated_entries)} teams.")
                )
                
            except Exception as e:
                error_count += 1
                messages.error(
                    request,
                    _(f"Error recalculating leaderboard for {leaderboard.sport_event.name}: {str(e)}")
                )
        
        # Summary message
        if success_count > 0:
            messages.success(request, _(f"Successfully recalculated {success_count} leaderboard(s)."))
        if warning_count > 0:
            messages.warning(request, _(f"{warning_count} leaderboard(s) had no completed games to calculate from."))
        if error_count > 0:
            messages.error(request, _(f"Failed to recalculate {error_count} leaderboard(s) due to errors."))
            
    recalculate_leaderboards.short_description = _("Recalculate selected leaderboards")
    
    def _calculate_leaderboard(self, leaderboard):
        """
        Helper method to calculate a leaderboard.
        Extracted to avoid code duplication with the API view.
        
        Returns:
            list: Updated entries if successful
            None: If no completed games found
        """
        # Get the sport event
        sport_event = leaderboard.sport_event
        
        # Get all completed and verified games for this sport event
        from scores.models import Score
        from games.models import Game
        
        games = Game.objects.filter(
            sport_event=sport_event,
            status='completed',
            score__verification_status='verified'
        ).select_related('score')
        
        if not games.exists():
            return None
        
        # Get all teams that participated in these games
        team_ids = set()
        for game in games:
            for game_team in game.game_teams.all():
                team_ids.add(game_team.team.id)
        
        # Calculate stats for each team
        entries = []
        for team_id in team_ids:
            # Get team object
            from teams.models import Team
            team = Team.objects.get(id=team_id)
            
            # Calculate team statistics
            stats = {
                'team': team,
                'played': 0,
                'won': 0,
                'drawn': 0,
                'lost': 0,
                'goals_for': 0,
                'goals_against': 0,
                'goal_difference': 0,
                'points': 0,
                'clean_sheets': 0,
                'yellow_cards': 0,
                'red_cards': 0
            }
            
            # Process each game
            for game in games:
                # Check if this team participated in this game
                team_designations = game.game_teams.filter(team_id=team_id)
                if not team_designations.exists():
                    continue
                
                # Increment games played
                stats['played'] += 1
                
                # Get the score
                score = game.score
                
                # Get team designation
                team_designation = team_designations.first().designation
                
                # Set team position (1 or 2) based on designation
                team_position = 1 if team_designation in ['team_a', 'home'] else 2
                
                # Get goals for/against
                if team_position == 1:
                    goals_for = score.final_score_team1 or 0
                    goals_against = score.final_score_team2 or 0
                else:
                    goals_for = score.final_score_team2 or 0
                    goals_against = score.final_score_team1 or 0
                
                stats['goals_for'] += goals_for
                stats['goals_against'] += goals_against
                
                # Check for clean sheet
                if goals_against == 0:
                    stats['clean_sheets'] += 1
                
                # Determine win/loss/draw
                if score.is_draw:
                    stats['drawn'] += 1
                    stats['points'] += 1  # 1 point for a draw
                elif score.winner and score.winner.id == team_id:
                    stats['won'] += 1
                    stats['points'] += 3  # 3 points for a win
                else:
                    stats['lost'] += 1  # 0 points for a loss
                
                # Check for cards
                # This is just a placeholder; implementation depends on how cards are tracked
                if hasattr(score, 'score_details'):
                    yellow_cards = score.score_details.filter(
                        team_id=team_id, 
                        event_type='yellow_card'
                    ).count()
                    
                    red_cards = score.score_details.filter(
                        team_id=team_id, 
                        event_type='red_card'
                    ).count()
                    
                    stats['yellow_cards'] += yellow_cards
                    stats['red_cards'] += red_cards
            
            # Calculate goal difference
            stats['goal_difference'] = stats['goals_for'] - stats['goals_against']
            
            # Update or create leaderboard entry
            entry, created = LeaderboardEntry.objects.update_or_create(
                leaderboard=leaderboard,
                team=team,
                defaults={
                    'played': stats['played'],
                    'won': stats['won'],
                    'drawn': stats['drawn'],
                    'lost': stats['lost'],
                    'goals_for': stats['goals_for'],
                    'goals_against': stats['goals_against'],
                    'goal_difference': stats['goal_difference'],
                    'points': stats['points'],
                    'clean_sheets': stats['clean_sheets'],
                    'yellow_cards': stats['yellow_cards'],
                    'red_cards': stats['red_cards'],
                    'position': 0  # Temporary position, will be updated below
                }
            )
            entries.append(entry)
        
        # Sort entries by points, goal difference, goals for
        sorted_entries = sorted(
            entries,
            key=lambda x: (-x.points, -x.goal_difference, -x.goals_for)
        )
        
        # Update positions
        for i, entry in enumerate(sorted_entries):
            entry.position = i + 1
            entry.save(update_fields=['position'])
        
        # Update leaderboard's last_updated timestamp
        leaderboard.last_updated = timezone.now()
        leaderboard.save(update_fields=['last_updated'])
        
        return entries
    
    def finalize_leaderboards(self, request, queryset):
        """
        Admin action to mark selected leaderboards as final.
        """
        from django.contrib import messages
        
        finalized_count = 0
        already_final_count = 0
        
        for leaderboard in queryset:
            if leaderboard.is_final:
                already_final_count += 1
                continue
                
            leaderboard.is_final = True
            leaderboard.save(update_fields=['is_final'])
            
            finalized_count += 1
        
        if finalized_count > 0:
            messages.success(request, _(f"Successfully marked {finalized_count} leaderboard(s) as final."))
        if already_final_count > 0:
            messages.info(request, _(f"{already_final_count} leaderboard(s) were already marked as final."))
            
    finalize_leaderboards.short_description = _("Mark selected leaderboards as final")
    
    def unfinalize_leaderboards(self, request, queryset):
        """
        Admin action to unmark selected leaderboards as final.
        Useful if a tournament needs to be reopened.
        """
        from django.contrib import messages
        
        unfinalized_count = 0
        already_not_final_count = 0
        
        for leaderboard in queryset:
            if not leaderboard.is_final:
                already_not_final_count += 1
                continue
                
            leaderboard.is_final = False
            leaderboard.save(update_fields=['is_final'])
            
            unfinalized_count += 1
        
        if unfinalized_count > 0:
            messages.success(request, _(f"Successfully unmarked {unfinalized_count} leaderboard(s) as not final."))
        if already_not_final_count > 0:
            messages.info(request, _(f"{already_not_final_count} leaderboard(s) were already not marked as final."))
            
    unfinalize_leaderboards.short_description = _("Unmark selected leaderboards as final")
    
    def get_queryset(self, request):
        """Optimize queryset to reduce number of database queries"""
        queryset = super().get_queryset(request)
        return queryset.select_related('sport_event').annotate(
            entry_count=Count('entries')
        )


@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    """
    Admin interface for LeaderboardEntry model.
    Provides detailed view of team standings in tournaments.
    """
    list_display = [
        'get_team_name', 'get_leaderboard_name', 'position', 
        'played', 'won', 'drawn', 'lost', 'points', 'goal_difference',
        'get_performance'
    ]
    list_filter = [
        'leaderboard__sport_event__sport_type', 
        'leaderboard__sport_event', 
        'leaderboard', 
        'team'
    ]
    search_fields = ['team__name', 'leaderboard__sport_event__name']
    readonly_fields = [
        'position', 'played', 'won', 'drawn', 'lost', 
        'points', 'goals_for', 'goals_against', 'goal_difference',
        'clean_sheets', 'yellow_cards', 'red_cards', 'get_win_percentage',
        'get_performance'
    ]
    ordering = ['leaderboard', 'position']
    
    fieldsets = [
        (None, {
            'fields': [
                'leaderboard', 'team', 'position'
            ]
        }),
        (_('Results'), {
            'fields': [
                'played', 'won', 'drawn', 'lost', 'points', 'get_win_percentage'
            ]
        }),
        (_('Goals'), {
            'fields': [
                'goals_for', 'goals_against', 'goal_difference', 'clean_sheets'
            ]
        }),
        (_('Discipline'), {
            'fields': [
                'yellow_cards', 'red_cards'
            ],
            'classes': ['collapse']
        })
    ]
    
    def get_team_name(self, obj):
        """Return a clickable link to the team"""
        if obj.team:
            return format_html(
                '<a href="{}">{}</a>',
                reverse('admin:teams_team_change', args=[obj.team.id]),
                obj.team.name
            )
        return "-"
    get_team_name.short_description = _('Team')
    get_team_name.admin_order_field = 'team__name'
    
    def get_leaderboard_name(self, obj):
        """Return a clickable link to the leaderboard's sport event"""
        if obj.leaderboard and obj.leaderboard.sport_event:
            return format_html(
                '<a href="{}">{} ({})</a>',
                reverse('admin:events_sportevent_change', args=[obj.leaderboard.sport_event.id]),
                obj.leaderboard.sport_event.name,
                obj.leaderboard.sport_event.get_sport_type_display()
            )
        return "-"
    get_leaderboard_name.short_description = _('Sport Event')
    get_leaderboard_name.admin_order_field = 'leaderboard__sport_event__name'
    
    def get_win_percentage(self, obj):
        """Calculate and return the win percentage"""
        if obj.played == 0:
            return "0.0%"
        win_percentage = (obj.won / obj.played) * 100
        return f"{win_percentage:.1f}%"
    get_win_percentage.short_description = _('Win %')
    
    def get_performance(self, obj):
        """Return a visual indicator of recent performance"""
        if obj.played == 0:
            return "-"
        
        # Create performance indicator based on points percentage
        max_possible_points = obj.played * 3
        if max_possible_points == 0:
            return "-"
            
        points_percentage = (obj.points / max_possible_points) * 100
        
        if points_percentage >= 80:
            return format_html('<span style="color:green;">★★★★★</span>')
        elif points_percentage >= 60:
            return format_html('<span style="color:green;">★★★★</span>')
        elif points_percentage >= 45:
            return format_html('<span style="color:blue;">★★★</span>')
        elif points_percentage >= 30:
            return format_html('<span style="color:orange;">★★</span>')
        else:
            return format_html('<span style="color:red;">★</span>')
    get_performance.short_description = _('Performance')