from django.db.models.signals import post_save
from django.dispatch import receiver
from scores.models import Score
from .models import Leaderboard, LeaderboardEntry
from django.db import transaction


@receiver(post_save, sender=Score)
def update_leaderboard_on_score_change(sender, instance, **kwargs):
    """
    Signal handler to update leaderboards when a score is updated.
    When a score is completed and verified, automatically recalculate
    the leaderboard for the corresponding sport event.
    """
    # Only respond when score is completed and verified
    if instance.status == 'completed' and instance.verification_status == 'verified':
        # Recalculate in a transaction to ensure data consistency
        transaction.on_commit(lambda: recalculate_leaderboard_for_sport_event(instance.game.sport_event))
        
        
def recalculate_leaderboard_for_sport_event(sport_event):
    """
    Recalculate leaderboard for a specific sport event based on verified scores.
    """
    # Get or create the leaderboard
    leaderboard, created = Leaderboard.objects.get_or_create(
        sport_event=sport_event
    )
    
    # Skip recalculation if leaderboard is marked as final
    if leaderboard.is_final:
        return
    
    # Get all completed and verified games for this sport event
    from games.models import Game
    
    games = Game.objects.filter(
        sport_event=sport_event,
        status='completed',
        score__verification_status='verified'
    ).select_related('score')
    
    # If no games, just update timestamp
    if not games.exists():
        leaderboard.save()
        return
    
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
            
            # Check for cards from score details if available
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
    leaderboard.save()
