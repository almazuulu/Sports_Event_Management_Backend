import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class ScoreDetail(models.Model):
    """
    Model for tracking detailed scoring events within a game.
    Each ScoreDetail represents one scoring event (e.g., a goal, point, etc.).
    """
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
    points = models.PositiveIntegerField(
        _('Points'),
        default=1,
        help_text=_('Number of points for this scoring event')
    )
    time_occurred = models.TimeField(
        _('Time Occurred'),
        help_text=_('Time when the scoring event occurred')
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