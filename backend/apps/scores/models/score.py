import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class Score(models.Model):
    """
    Model for tracking scores for a specific game.
    Each Score object represents the overall scoring record for a game.
    """
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('in_progress', _('In Progress')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    )
    
    VERIFICATION_STATUS_CHOICES = (
        ('unverified', _('Unverified')),
        ('pending_verification', _('Pending Verification')),
        ('verified', _('Verified')),
        ('disputed', _('Disputed')),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    game = models.OneToOneField(
        'games.Game',
        on_delete=models.CASCADE,
        related_name='score',
        verbose_name=_('Game')
    )
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    final_score_team1 = models.PositiveIntegerField(
        _('Final Score Team 1'),
        null=True,
        blank=True
    )
    final_score_team2 = models.PositiveIntegerField(
        _('Final Score Team 2'),
        null=True,
        blank=True
    )
    # Added statistics fields similar to Premier League
    goals_for_team1 = models.PositiveIntegerField(
        _('Goals For Team 1'),
        default=0
    )
    goals_against_team1 = models.PositiveIntegerField(
        _('Goals Against Team 1'),
        default=0
    )
    goals_for_team2 = models.PositiveIntegerField(
        _('Goals For Team 2'),
        default=0
    )
    goals_against_team2 = models.PositiveIntegerField(
        _('Goals Against Team 2'),
        default=0
    )
    # Field to track time elapsed in the game (for live updates)
    time_elapsed = models.CharField(
        _('Time Elapsed'),
        max_length=20,
        blank=True,
        help_text=_('Current time elapsed in the game (e.g., "45+2", "90")')
    )
    winner = models.ForeignKey(
        'teams.Team',
        on_delete=models.SET_NULL,
        related_name='won_games',
        verbose_name=_('Winner'),
        null=True,
        blank=True
    )
    is_draw = models.BooleanField(
        _('Is Draw'),
        default=False,
        help_text=_('Whether the game ended in a draw')
    )
    notes = models.TextField(_('Notes'), blank=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    scorekeeper = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='scorekeeping_games',
        verbose_name=_('Scorekeeper'),
        null=True,
        blank=True,
        limit_choices_to={'role': 'scorekeeper'}
    )
    # Enhanced verification system
    verification_status = models.CharField(
        _('Verification Status'),
        max_length=20,
        choices=VERIFICATION_STATUS_CHOICES,
        default='unverified'
    )
    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='verified_scores',
        verbose_name=_('Verified By'),
        null=True,
        blank=True,
        limit_choices_to={'role': 'admin'}
    )
    verified_at = models.DateTimeField(_('Verified At'), null=True, blank=True)

    class Meta:
        verbose_name = _('Score')
        verbose_name_plural = _('Scores')
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Score for {self.game}"
        
    def determine_winner(self):
        """
        Determine the winner based on final scores.
        Returns the winning team or None if it's a draw or incomplete.
        
        This implementation handles GameTeam relationships properly.
        """
        if self.final_score_team1 is None or self.final_score_team2 is None:
            return None
            
        # Get teams from GameTeam relations
        team1 = None
        team2 = None
        
        if hasattr(self.game, 'game_teams') and self.game.game_teams.exists():
            team1_relation = self.game.game_teams.filter(designation__in=['team_a', 'home']).first()
            team2_relation = self.game.game_teams.filter(designation__in=['team_b', 'away']).first()
            
            if team1_relation:
                team1 = team1_relation.team
            if team2_relation:
                team2 = team2_relation.team
        
        if self.final_score_team1 > self.final_score_team2:
            return team1
        elif self.final_score_team2 > self.final_score_team1:
            return team2
        else:
            # It's a draw
            return None
    
    def calculate_goal_difference(self, team_number):
        """
        Calculate the goal difference for a team.
        
        Args:
            team_number: 1 for team1, 2 for team2
        """
        if team_number == 1:
            return self.goals_for_team1 - self.goals_against_team1
        elif team_number == 2:
            return self.goals_for_team2 - self.goals_against_team2
        return 0
    
    def update_statistics(self):
        """
        Update goal statistics based on the current score details.
        Should be called after adding or removing score details.
        """
        # Implementation would depend on business logic
        # This is a placeholder for the actual implementation
        pass