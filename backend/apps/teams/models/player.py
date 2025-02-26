from django.db import models
from django.conf import settings


class Player(models.Model):
    team = models.ForeignKey(
        'teams.Team',
        on_delete=models.CASCADE,
        related_name='players'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='player_profiles',
        blank=True,
        null=True
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    jersey_number = models.IntegerField()
    position = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField()
    photo = models.ImageField(upload_to='player_photos/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    joined_date = models.DateField()
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['team', 'last_name', 'first_name']
        verbose_name = 'Player'
        verbose_name_plural = 'Players'
        unique_together = [['team', 'jersey_number']]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.team.name})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"