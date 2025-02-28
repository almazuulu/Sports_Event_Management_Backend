import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class Player(models.Model):
    """
    Model representing a player who belongs to a team.
    A player may or may not be a registered user in the system.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    team = models.ForeignKey(
        'teams.Team',
        on_delete=models.CASCADE,
        related_name='players',
        verbose_name=_('Team')
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='player_profiles',
        verbose_name=_('User Account'),
        null=True,
        blank=True,
        help_text=_('If the player has a user account in the system')
    )
    first_name = models.CharField(_('First Name'), max_length=100)
    last_name = models.CharField(_('Last Name'), max_length=100)
    jersey_number = models.PositiveSmallIntegerField(_('Jersey Number'))
    position = models.CharField(_('Position'), max_length=50, blank=True)
    date_of_birth = models.DateField(_('Date of Birth'))
    photo = models.ImageField(
        _('Photo'), 
        upload_to='player_photos/', 
        null=True, 
        blank=True
    )
    is_active = models.BooleanField(_('Is Active'), default=True)
    joined_date = models.DateField(_('Joined Date'))
    notes = models.TextField(_('Notes'), blank=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Player')
        verbose_name_plural = _('Players')
        ordering = ['team', 'last_name', 'first_name']
        constraints = [
            models.UniqueConstraint(
                fields=['team', 'jersey_number'],
                name='unique_jersey_number_per_team'
            )
        ]
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.team.name})"
        
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"