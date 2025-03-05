import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class TeamRegistration(models.Model):
    """
    Model representing a team's registration for a specific sport event.
    This creates a many-to-many relationship between teams and sport events.
    """
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    team = models.ForeignKey(
        'teams.Team',
        on_delete=models.CASCADE,
        related_name='event_registrations',
        verbose_name=_('Team')
    )
    sport_event = models.ForeignKey(
        'events.SportEvent',
        on_delete=models.CASCADE,
        related_name='team_registrations',
        verbose_name=_('Sport Event')
    )
    registration_date = models.DateTimeField(_('Registration Date'), auto_now_add=True)
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    notes = models.TextField(_('Notes'), blank=True)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='approved_registrations',
        verbose_name=_('Approved By'),
        null=True,
        blank=True,
        limit_choices_to={'role': 'admin'}
    )
    approval_date = models.DateTimeField(_('Approval Date'), null=True, blank=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Team Registration')
        verbose_name_plural = _('Team Registrations')
        ordering = ['-registration_date']
        constraints = [
            models.UniqueConstraint(
                fields=['team', 'sport_event'],
                name='unique_team_registration_per_event'
            )
        ]
        
    def __str__(self):
        return f"{self.team.name} registration for {self.sport_event.name}"