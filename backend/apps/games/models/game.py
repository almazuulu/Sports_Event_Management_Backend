import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class Game(models.Model):
    """
    Model representing a scheduled game/match within a sport event.
    According to section 2.4 of the SRS, games need defined start/end times
    and must be assignable to teams.
    """
    STATUS_CHOICES = (
        ('scheduled', _('Scheduled')),
        ('ongoing', _('Ongoing')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    sport_event = models.ForeignKey(
        'events.SportEvent', 
        on_delete=models.CASCADE, 
        related_name='games',
        verbose_name=_('Sport Event')
    )
    name = models.CharField(_('Game Name'), max_length=255)
    description = models.TextField(_('Description'), blank=True)
    location = models.CharField(_('Location'), max_length=255)
    start_datetime = models.DateTimeField(_('Start Time'))
    end_datetime = models.DateTimeField(_('End Time'))
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled'
    )
    # According to section 2.2, admins assign scorekeepers to games
    scorekeeper = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='assigned_games',
        verbose_name=_('Scorekeeper'),
        null=True,
        blank=True,
        limit_choices_to={'role': 'scorekeeper'},
        help_text=_('User responsible for keeping score for this game')
    )
    # Audit fields
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_games',
        verbose_name=_('Created By'),
        help_text=_('Administrator who created this game'),
        limit_choices_to={'role': 'admin'}
    )
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='updated_games',
        verbose_name=_('Updated By'),
        null=True,
        blank=True,
        help_text=_('User who last updated this game'),
        limit_choices_to={'role': 'admin'}
    )

    class Meta:
        verbose_name = _('Game')
        verbose_name_plural = _('Games')
        ordering = ['start_datetime']
        
    def __str__(self):
        return f"{self.name} - {self.sport_event.name}"