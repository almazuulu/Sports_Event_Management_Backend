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
        """
        if self.final_score_team1 is None or self.final_score_team2 is None:
            return None
            
        if self.final_score_team1 > self.final_score_team2:
            return self.game.team1
        elif self.final_score_team2 > self.final_score_team1:
            return self.game.team2
        else:
            # It's a draw
            return None