import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class Team(models.Model):
    """
    Model representing a team in the sports event management system.
    Each team can participate in different sport events through TeamRegistration.
    """
    STATUS_CHOICES = (
        ('active', _('Active')),
        ('inactive', _('Inactive')),
        ('suspended', _('Suspended')),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(_('Team Name'), max_length=100, unique=True)
    logo = models.ImageField(
        _('Team Logo'), 
        upload_to='team_logos/', 
        null=True, 
        blank=True
    )
    description = models.TextField(_('Description'), blank=True)
    captain = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='captained_teams',
        verbose_name=_('Team Captain'),
        limit_choices_to={'role': 'team_captain'}
    )
    contact_email = models.EmailField(_('Contact Email'))
    contact_phone = models.CharField(_('Contact Phone'), max_length=20, blank=True)
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Team')
        verbose_name_plural = _('Teams')
        ordering = ['name']
        
    def __str__(self):
        return self.name

    @property
    def player_count(self):
        """Return the count of active players"""
        return self.players.filter(is_active=True).count()