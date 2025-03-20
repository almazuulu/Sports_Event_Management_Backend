import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class Leaderboard(models.Model):
    """
    Model representing a leaderboard for a specific sport event.
    Stores the overall ranking table for teams in a sport event.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    sport_event = models.OneToOneField(
        'events.SportEvent',
        on_delete=models.CASCADE,
        related_name='leaderboard',
        verbose_name=_('Sport Event')
    )
    last_updated = models.DateTimeField(_('Last Updated'), auto_now=True)
    is_final = models.BooleanField(
        _('Is Final'),
        default=False,
        help_text=_('Whether this leaderboard represents the final standings')
    )

    class Meta:
        verbose_name = _('Leaderboard')
        verbose_name_plural = _('Leaderboards')
        ordering = ['sport_event__name']
        
    def __str__(self):
        return f"Leaderboard for {self.sport_event.name}"


class LeaderboardEntry(models.Model):
    """
    Model representing a team's position and stats in a leaderboard.
    Each entry corresponds to one team's statistics in the leaderboard.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    leaderboard = models.ForeignKey(
        'leaderboards.Leaderboard',
        on_delete=models.CASCADE,
        related_name='entries',
        verbose_name=_('Leaderboard')
    )
    team = models.ForeignKey(
        'teams.Team',
        on_delete=models.CASCADE,
        related_name='leaderboard_entries',
        verbose_name=_('Team')
    )
    position = models.PositiveIntegerField(
        _('Position'),
        help_text=_('Team ranking position')
    )
    played = models.PositiveIntegerField(_('Played'), default=0)
    won = models.PositiveIntegerField(_('Won'), default=0)
    drawn = models.PositiveIntegerField(_('Drawn'), default=0)
    lost = models.PositiveIntegerField(_('Lost'), default=0)
    points = models.PositiveIntegerField(_('Points'), default=0)
    goals_for = models.PositiveIntegerField(_('Goals For'), default=0)
    goals_against = models.PositiveIntegerField(_('Goals Against'), default=0)
    goal_difference = models.IntegerField(_('Goal Difference'), default=0)
    # Additional stats for different sports
    clean_sheets = models.PositiveIntegerField(_('Clean Sheets'), default=0)
    yellow_cards = models.PositiveIntegerField(_('Yellow Cards'), default=0)
    red_cards = models.PositiveIntegerField(_('Red Cards'), default=0)
    
    class Meta:
        verbose_name = _('Leaderboard Entry')
        verbose_name_plural = _('Leaderboard Entries')
        ordering = ['leaderboard', 'position']
        unique_together = ['leaderboard', 'team']
        
    def __str__(self):
        return f"{self.team.name} - Position {self.position}"
