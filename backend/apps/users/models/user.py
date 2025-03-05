from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid
from .user_manager import UserManager

class User(AbstractUser):
    """
    Custom User model that uses email as the unique identifier
    and has role-based permissions for the Sports Event Management system.
    Uses UUID as primary key instead of auto-incrementing integer.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('ID'),
        help_text=_('A unique identifier for the user')
    )
    
    ROLE_CHOICES = (
        ('admin', _('Administrator')),
        ('team_manager', _('Team Manager')), 
        ('player', _('Player')),
        ('scorekeeper', _('Scorekeeper')),
        ('public', _('Public User')),
    )
   
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(
        max_length=15,
        choices=ROLE_CHOICES,
        default='public',
        help_text=_('User role determines permissions in the system')
    )
   
    # Make email the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
   
    objects = UserManager()
   
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
       
    def __str__(self):
        return self.email
   
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()
   
    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name