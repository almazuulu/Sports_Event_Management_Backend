from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.html import format_html
from .models import Leaderboard, LeaderboardEntry


class LeaderboardEntryInline(admin.TabularInline):
    """
    Inline admin for LeaderboardEntries within a Leaderboard.
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


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """
    Admin interface for Leaderboard model.
    """
    list_display = ['get_sport_event_name', 'last_updated', 'is_final', 'get_entries_count']
    list_filter = ['is_final', 'last_updated']
    search_fields = ['sport_event__name']
    readonly_fields = ['last_updated']
    inlines = [LeaderboardEntryInline]
    actions = ['recalculate_leaderboards', 'finalize_leaderboards']
    
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
    
    def get_entries_count(self, obj):
        """Return the number of entries in the leaderboard"""
        return obj.entries.count()
    get_entries_count.short_description = _('Teams')
    
    def recalculate_leaderboards(self, request, queryset):
        """
        Admin action to recalculate the selected leaderboards.
        """
        from django.contrib import messages
        
        for leaderboard in queryset:
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
                messages.warning(
                    request, 
                    _(f"No completed and verified games found for {sport_event.name}.")
                )
                continue
            
            # Get all teams that participated in these games
            team_ids = set()
            for game in games:
                for game_team in game.game_teams.all():
                    team_ids.add(game_team.team_id)
            
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
            leaderboard.save()
            
            # Show success message
            messages.success(
                request, 
                _(f"Successfully recalculated leaderboard for {sport_event.name} with {len(entries)} teams.")
            )
            
    recalculate_leaderboards.short_description = _("Recalculate selected leaderboards")
    
    def finalize_leaderboards(self, request, queryset):
        """
        Admin action to mark selected leaderboards as final.
        """
        from django.contrib import messages
        
        for leaderboard in queryset:
            if leaderboard.is_final:
                messages.info(
                    request, 
                    _(f"Leaderboard for {leaderboard.sport_event.name} is already marked as final.")
                )
                continue
                
            leaderboard.is_final = True
            leaderboard.save(update_fields=['is_final'])
            
            messages.success(
                request, 
                _(f"Successfully marked leaderboard for {leaderboard.sport_event.name} as final.")
            )
            
    finalize_leaderboards.short_description = _("Mark selected leaderboards as final")


@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    """
    Admin interface for LeaderboardEntry model.
    """
    list_display = [
        'get_team_name', 'get_leaderboard_name', 'position', 
        'played', 'won', 'drawn', 'lost', 'points', 'goal_difference'
    ]
    list_filter = ['leaderboard__sport_event', 'leaderboard', 'team']
    search_fields = ['team__name', 'leaderboard__sport_event__name']
    readonly_fields = [
        'position', 'played', 'won', 'drawn', 'lost', 
        'points', 'goals_for', 'goals_against', 'goal_difference',
        'clean_sheets', 'yellow_cards', 'red_cards'
    ]
    ordering = ['leaderboard', 'position']
    
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
                '<a href="{}">{}</a>',
                reverse('admin:events_sportevent_change', args=[obj.leaderboard.sport_event.id]),
                obj.leaderboard.sport_event.name
            )
        return "-"
    get_leaderboard_name.short_description = _('Sport Event')
    get_leaderboard_name.admin_order_field = 'leaderboard__sport_event__name'