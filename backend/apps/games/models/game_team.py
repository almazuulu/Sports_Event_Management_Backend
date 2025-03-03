import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class GameTeam(models.Model):
    """
    Model representing a team participating in a specific game.
    According to section 2.4 of the SRS, teams need to be assigned to games.
    """
    TEAM_DESIGNATION_CHOICES = (
        ('team_a', _('Team A')),
        ('team_b', _('Team B')),
        ('home', _('Home')),
        ('away', _('Away')),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    game = models.ForeignKey(
        'games.Game',
        on_delete=models.CASCADE,
        related_name='game_teams',
        verbose_name=_('Game')
    )
    team = models.ForeignKey(
        'teams.Team',
        on_delete=models.CASCADE,
        related_name='game_participations',
        verbose_name=_('Team')
    )
    designation = models.CharField(
        _('Team Designation'),
        max_length=20,
        choices=TEAM_DESIGNATION_CHOICES,
        help_text=_('Designation for this team in the context of the game')
    )
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Game Team')
        verbose_name_plural = _('Game Teams')
        ordering = ['game', 'designation']
        constraints = [
            models.UniqueConstraint(
                fields=['game', 'team'],
                name='unique_team_per_game'
            ),
            models.UniqueConstraint(
                fields=['game', 'designation'],
                name='unique_designation_per_game'
            )
        ]
        
    def __str__(self):
        return f"{self.team.name} as {self.get_designation_display()} in {self.game.name}"