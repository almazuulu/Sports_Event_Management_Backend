# Generated by Django 5.1.6 on 2025-03-05 07:19

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("events", "0001_initial"),
        ("teams", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Game",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Game Name")),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="Description"),
                ),
                ("location", models.CharField(max_length=255, verbose_name="Location")),
                ("start_datetime", models.DateTimeField(verbose_name="Start Time")),
                ("end_datetime", models.DateTimeField(verbose_name="End Time")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("scheduled", "Scheduled"),
                            ("ongoing", "Ongoing"),
                            ("completed", "Completed"),
                            ("cancelled", "Cancelled"),
                        ],
                        default="scheduled",
                        max_length=20,
                        verbose_name="Status",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated At"),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        help_text="Administrator who created this game",
                        limit_choices_to={"role": "admin"},
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="created_games",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created By",
                    ),
                ),
                (
                    "scorekeeper",
                    models.ForeignKey(
                        blank=True,
                        help_text="User responsible for keeping score for this game",
                        limit_choices_to={"role": "scorekeeper"},
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="assigned_games",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Scorekeeper",
                    ),
                ),
                (
                    "sport_event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="games",
                        to="events.sportevent",
                        verbose_name="Sport Event",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        help_text="User who last updated this game",
                        limit_choices_to={"role": "admin"},
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="updated_games",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Updated By",
                    ),
                ),
            ],
            options={
                "verbose_name": "Game",
                "verbose_name_plural": "Games",
                "ordering": ["start_datetime"],
            },
        ),
        migrations.CreateModel(
            name="GameTeam",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "designation",
                    models.CharField(
                        choices=[
                            ("team_a", "Team A"),
                            ("team_b", "Team B"),
                            ("home", "Home"),
                            ("away", "Away"),
                        ],
                        help_text="Designation for this team in the context of the game",
                        max_length=20,
                        verbose_name="Team Designation",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated At"),
                ),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="game_teams",
                        to="games.game",
                        verbose_name="Game",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="game_participations",
                        to="teams.team",
                        verbose_name="Team",
                    ),
                ),
            ],
            options={
                "verbose_name": "Game Team",
                "verbose_name_plural": "Game Teams",
                "ordering": ["game", "designation"],
            },
        ),
        migrations.CreateModel(
            name="GamePlayer",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "is_captain_for_game",
                    models.BooleanField(
                        default=False,
                        help_text="Indicates if this player is the captain for this specific game",
                        verbose_name="Is Captain for this Game",
                    ),
                ),
                (
                    "position",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="Position"
                    ),
                ),
                ("notes", models.TextField(blank=True, verbose_name="Notes")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Updated At"),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="game_selections",
                        to="teams.player",
                        verbose_name="Player",
                    ),
                ),
                (
                    "game_team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="selected_players",
                        to="games.gameteam",
                        verbose_name="Game Team",
                    ),
                ),
            ],
            options={
                "verbose_name": "Game Player",
                "verbose_name_plural": "Game Players",
                "ordering": ["game_team", "player__last_name"],
            },
        ),
        migrations.AddConstraint(
            model_name="gameteam",
            constraint=models.UniqueConstraint(
                fields=("game", "team"), name="unique_team_per_game"
            ),
        ),
        migrations.AddConstraint(
            model_name="gameteam",
            constraint=models.UniqueConstraint(
                fields=("game", "designation"), name="unique_designation_per_game"
            ),
        ),
        migrations.AddConstraint(
            model_name="gameplayer",
            constraint=models.UniqueConstraint(
                fields=("game_team", "player"),
                name="unique_player_selection_per_game_team",
            ),
        ),
    ]
