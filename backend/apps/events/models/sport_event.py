import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class SportEvent(models.Model):
    """
    Model representing specific sports within an event.
    According to requirements, only administrators can create and modify sport events.
    """
    SPORT_TYPE_CHOICES = (
        ('football', _('Football')),
        ('basketball', _('Basketball')),
        ('volleyball', _('Volleyball')),
        ('cricket', _('Cricket')),
        ('tennis', _('Tennis')),
        ('badminton', _('Badminton')),
        ('swimming', _('Swimming')),
        ('athletics', _('Athletics')),
        ('chess', _('Chess')),
        ('other', _('Other')),
    )
    
    GAME_STATUS_CHOICES = (
        ('scheduled', _('Scheduled')),
        ('registration', _('Registration Open')),
        ('registration_closed', _('Registration Closed')),
        ('ongoing', _('Ongoing')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    event = models.ForeignKey(
        'events.Event', 
        on_delete=models.CASCADE, 
        related_name='sport_events',
        verbose_name=_('Event')
    )
    sport_type = models.CharField(
        _('Sport Type'), 
        max_length=20, 
        choices=SPORT_TYPE_CHOICES
    )
    name = models.CharField(_('Name'), max_length=255)
    description = models.TextField(_('Description'), blank=True)
    start_date = models.DateField(_('Start Date'))
    end_date = models.DateField(_('End Date'))
    max_teams = models.PositiveIntegerField(
        _('Maximum Teams'), 
        default=0,  # 0 means unlimited
        help_text=_('Set to 0 for unlimited teams')
    )
    registration_deadline = models.DateTimeField(_('Registration Deadline'))
    rules = models.TextField(_('Rules'), blank=True)
    scoring_system = models.TextField(_('Scoring System'), blank=True)
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=GAME_STATUS_CHOICES,
        default='scheduled'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_sport_events',
        verbose_name=_('Created By'),
        help_text=_('Administrator who created this sport event'),
        limit_choices_to={'role': 'admin'}
    )
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='updated_sport_events',
        verbose_name=_('Updated By'),
        null=True,
        blank=True,
        help_text=_('Administrator who last updated this sport event'),
        limit_choices_to={'role': 'admin'}
    )

    class Meta:
        verbose_name = _('Sport Event')
        verbose_name_plural = _('Sport Events')
        ordering = ['event', 'start_date']
        constraints = [
            models.UniqueConstraint(
                fields=['event', 'sport_type', 'name'],
                name='unique_sport_event'
            )
        ]
        permissions = [
            ('view_sportevent_admin', _('Can view sport event as admin')),
            ('assign_scorekeeper', _('Can assign scorekeepers to sport event')),
        ]
        
    def __str__(self):
        return f"{self.name} ({self.get_sport_type_display()}) - {self.event.name}"