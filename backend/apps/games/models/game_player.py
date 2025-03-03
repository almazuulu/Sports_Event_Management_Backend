import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class GamePlayer(models.Model):
    """
    Model representing a player selected to participate in a specific game.
    According to section 2.3 of the SRS, team captains need to assign players to matches.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    game_team = models.ForeignKey(
        'games.GameTeam',
        on_delete=models.CASCADE,
        related_name='selected_players',
        verbose_name=_('Game Team')
    )
    player = models.ForeignKey(
        'teams.Player',
        on_delete=models.CASCADE,
        related_name='game_selections',
        verbose_name=_('Player')
    )
    is_captain_for_game = models.BooleanField(
        _('Is Captain for this Game'),
        default=False,
        help_text=_('Indicates if this player is the captain for this specific game')
    )
    position = models.CharField(_('Position'), max_length=50, blank=True)
    notes = models.TextField(_('Notes'), blank=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Game Player')
        verbose_name_plural = _('Game Players')
        ordering = ['game_team', 'player__last_name']
        constraints = [
            models.UniqueConstraint(
                fields=['game_team', 'player'],
                name='unique_player_selection_per_game_team'
            )
        ]
        
    def __str__(self):
        return f"{self.player.get_full_name()} - {self.game_team}"
        
    def clean(self):
        """
        Ensure the player belongs to the team that is participating in the game.
        """
        from django.core.exceptions import ValidationError
        
        if self.player.team != self.game_team.team:
            raise ValidationError({
                'player': _('This player does not belong to the selected team.')
            })
        
        super().clean()