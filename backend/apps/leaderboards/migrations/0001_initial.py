# Generated by Django 5.1.6 on 2025-03-20 04:29

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("events", "0001_initial"),
        ("teams", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Leaderboard",
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
                    "last_updated",
                    models.DateTimeField(auto_now=True, verbose_name="Last Updated"),
                ),
                (
                    "is_final",
                    models.BooleanField(
                        default=False,
                        help_text="Whether this leaderboard represents the final standings",
                        verbose_name="Is Final",
                    ),
                ),
                (
                    "sport_event",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="leaderboard",
                        to="events.sportevent",
                        verbose_name="Sport Event",
                    ),
                ),
            ],
            options={
                "verbose_name": "Leaderboard",
                "verbose_name_plural": "Leaderboards",
                "ordering": ["sport_event__name"],
            },
        ),
        migrations.CreateModel(
            name="LeaderboardEntry",
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
                    "position",
                    models.PositiveIntegerField(
                        help_text="Team ranking position", verbose_name="Position"
                    ),
                ),
                (
                    "played",
                    models.PositiveIntegerField(default=0, verbose_name="Played"),
                ),
                ("won", models.PositiveIntegerField(default=0, verbose_name="Won")),
                ("drawn", models.PositiveIntegerField(default=0, verbose_name="Drawn")),
                ("lost", models.PositiveIntegerField(default=0, verbose_name="Lost")),
                (
                    "points",
                    models.PositiveIntegerField(default=0, verbose_name="Points"),
                ),
                (
                    "goals_for",
                    models.PositiveIntegerField(default=0, verbose_name="Goals For"),
                ),
                (
                    "goals_against",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Goals Against"
                    ),
                ),
                (
                    "goal_difference",
                    models.IntegerField(default=0, verbose_name="Goal Difference"),
                ),
                (
                    "clean_sheets",
                    models.PositiveIntegerField(default=0, verbose_name="Clean Sheets"),
                ),
                (
                    "yellow_cards",
                    models.PositiveIntegerField(default=0, verbose_name="Yellow Cards"),
                ),
                (
                    "red_cards",
                    models.PositiveIntegerField(default=0, verbose_name="Red Cards"),
                ),
                (
                    "leaderboard",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="entries",
                        to="leaderboards.leaderboard",
                        verbose_name="Leaderboard",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="leaderboard_entries",
                        to="teams.team",
                        verbose_name="Team",
                    ),
                ),
            ],
            options={
                "verbose_name": "Leaderboard Entry",
                "verbose_name_plural": "Leaderboard Entries",
                "ordering": ["leaderboard", "position"],
                "unique_together": {("leaderboard", "team")},
            },
        ),
    ]
