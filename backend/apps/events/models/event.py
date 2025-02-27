import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class Event(models.Model):
    """
    The main model for managing sports events.
    According to requirements, only administrators can create and modify events.
    """
    STATUS_CHOICES = (
        ('draft', _('Draft')),
        ('registration', _('Registration')),
        ('active', _('Active')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(_('Name'), max_length=255)
    description = models.TextField(_('Description'), blank=True)
    start_date = models.DateField(_('Start Date'))
    end_date = models.DateField(_('End Date'))
    location = models.CharField(_('Location'), max_length=255)
    status = models.CharField(
        _('Status'), 
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='draft'
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='created_events',
        verbose_name=_('Created By'),
        help_text=_('Only administrators can create events'),
        limit_choices_to={'role': 'admin'}
    )
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='updated_events',
        verbose_name=_('Updated By'),
        null=True,
        blank=True,
        help_text=_('Administrator who last updated this event'),
        limit_choices_to={'role': 'admin'}
    )

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ['start_date']
        permissions = [
            ('view_event_admin', _('Can view event as admin')),
        ]
        
    def __str__(self):
        return self.name