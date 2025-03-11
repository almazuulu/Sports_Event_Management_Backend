import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class ScoreDetail(models.Model):
    """
    Model for tracking detailed scoring events within a game.
    Each ScoreDetail represents one scoring event (e.g., a goal, point, etc.).
    """
    # Added event types to track different kinds of scoring events
    EVENT_TYPE_CHOICES = (
        ('goal', _('Goal')),
        ('assist', _('Assist')),
        ('own_goal', _('Own Goal')),
        ('penalty', _('Penalty')),
        ('free_kick', _('Free Kick')),
        ('basket', _('Basket')),
        ('point', _('Point')),
        ('other', _('Other')),
    )
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    score = models.ForeignKey(
        'scores.Score',
        on_delete=models.CASCADE,
        related_name='score_details',
        verbose_name=_('Score')
    )
    team = models.ForeignKey(
        'teams.Team',
        on_delete=models.CASCADE,
        related_name='scoring_events',
        verbose_name=_('Team')
    )
    player = models.ForeignKey(
        'teams.Player',
        on_delete=models.SET_NULL,
        related_name='scoring_events',
        verbose_name=_('Player'),
        null=True,
        blank=True,
        help_text=_('The player who scored (if applicable)')
    )
    # Added assisted_by to track assists
    assisted_by = models.ForeignKey(
        'teams.Player',
        on_delete=models.SET_NULL,
        related_name='player_assists',
        verbose_name=_('Assisted By'),
        null=True,
        blank=True,
        help_text=_('The player who provided the assist (if applicable)')
    )
    points = models.PositiveIntegerField(
        _('Points'),
        default=1,
        help_text=_('Number of points for this scoring event')
    )
    # Event type field to categorize scoring events
    event_type = models.CharField(
        _('Event Type'),
        max_length=20,
        choices=EVENT_TYPE_CHOICES,
        default='goal',
        help_text=_('Type of scoring event')
    )
    time_occurred = models.TimeField(
        _('Time Occurred'),
        help_text=_('Time when the scoring event occurred')
    )
    # Added minute field for easier tracking of game time
    minute = models.PositiveSmallIntegerField(
        _('Minute'),
        null=True,
        blank=True,
        help_text=_('Minute of the game when the event occurred')
    )
    period = models.CharField(
        _('Period'),
        max_length=50,
        blank=True,
        help_text=_('Game period (e.g., quarter, half) when the scoring occurred')
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        help_text=_('Optional description of the scoring event')
    )
    # Added video_url to potentially link to video clips of the event
    video_url = models.URLField(
        _('Video URL'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('URL to video clip of the scoring event')
    )
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='created_score_details',
        verbose_name=_('Created By'),
        null=True,
        help_text=_('User who recorded this scoring event'),
        limit_choices_to={'role__in': ['scorekeeper', 'admin']}
    )

    class Meta:
        verbose_name = _('Score Detail')
        verbose_name_plural = _('Score Details')
        ordering = ['score', 'time_occurred']
        
    def __str__(self):
        return f"{self.team.name} - {self.points} points at {self.time_occurred}"
    
    def save(self, *args, **kwargs):
        """
        Override save to update the overall score when a scoring event is created or modified.
        """
        super().save(*args, **kwargs)
        
        # Update the parent score's statistics
        self.update_parent_score()
    
    def update_parent_score(self):
        """
        Update the parent score based on this score detail.
        This ensures that the overall score stays in sync with individual events.
        """
        # This would be implemented based on business logic
        # Get all score details for this score and recalculate
        if self.score:
            # Get game_teams to determine which team is team1 and which is team2
            if hasattr(self.score.game, 'game_teams') and self.score.game.game_teams.exists():
                team1_relation = self.score.game.game_teams.filter(designation__in=['team_a', 'home']).first()
                team2_relation = self.score.game.game_teams.filter(designation__in=['team_b', 'away']).first()
                
                if team1_relation and team2_relation:
                    team1 = team1_relation.team
                    team2 = team2_relation.team
                    
                    # Calculate scores by summing points for each team
                    team1_score = self.score.score_details.filter(team=team1).aggregate(
                        models.Sum('points'))['points__sum'] or 0
                    team2_score = self.score.score_details.filter(team=team2).aggregate(
                        models.Sum('points'))['points__sum'] or 0
                    
                    # Update the score
                    self.score.final_score_team1 = team1_score
                    self.score.final_score_team2 = team2_score
                    
                    # Determine winner based on updated scores
                    winner = self.score.determine_winner()
                    if winner:
                        self.score.winner = winner
                        self.score.is_draw = False
                    else:
                        self.score.winner = None
                        self.score.is_draw = True
                    
                    # Save the score
                    self.score.save(update_fields=[
                        'final_score_team1', 'final_score_team2', 
                        'winner', 'is_draw', 'updated_at'
                    ])