from django.db import models
from django.conf import settings


class TeamRegistration(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    team = models.ForeignKey(
        'teams.Team',
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    sport_event = models.ForeignKey(
        'events.SportEvent',
        on_delete=models.CASCADE,
        related_name='team_registrations'
    )
    registration_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='approved_registrations',
        blank=True,
        null=True
    )
    approval_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-registration_date']
        verbose_name = 'Team Registration'
        verbose_name_plural = 'Team Registrations'
        unique_together = [['team', 'sport_event']]

    def __str__(self):
        return f"{self.team.name} - {self.sport_event.name} ({self.get_status_display()})"