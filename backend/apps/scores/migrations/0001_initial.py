# Generated by Django 5.1.6 on 2025-03-05 07:19

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("games", "0001_initial"),
        ("teams", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Score",
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
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("in_progress", "In Progress"),
                            ("completed", "Completed"),
                            ("cancelled", "Cancelled"),
                        ],
                        default="pending",
                        max_length=20,
                        verbose_name="Status",
                    ),
                ),
                (
                    "final_score_team1",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Final Score Team 1"
                    ),
                ),
                (
                    "final_score_team2",
                    models.PositiveIntegerField(
                        blank=True, null=True, verbose_name="Final Score Team 2"
                    ),
                ),
                (
                    "is_draw",
                    models.BooleanField(
                        default=False,
                        help_text="Whether the game ended in a draw",
                        verbose_name="Is Draw",
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
                    "verified_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Verified At"
                    ),
                ),
                (
                    "game",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="score",
                        to="games.game",
                        verbose_name="Game",
                    ),
                ),
                (
                    "scorekeeper",
                    models.ForeignKey(
                        blank=True,
                        limit_choices_to={"role": "scorekeeper"},
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="scorekeeping_games",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Scorekeeper",
                    ),
                ),
                (
                    "verified_by",
                    models.ForeignKey(
                        blank=True,
                        limit_choices_to={"role": "admin"},
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="verified_scores",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Verified By",
                    ),
                ),
                (
                    "winner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="won_games",
                        to="teams.team",
                        verbose_name="Winner",
                    ),
                ),
            ],
            options={
                "verbose_name": "Score",
                "verbose_name_plural": "Scores",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="ScoreDetail",
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
                    "points",
                    models.PositiveIntegerField(
                        default=1,
                        help_text="Number of points for this scoring event",
                        verbose_name="Points",
                    ),
                ),
                (
                    "time_occurred",
                    models.TimeField(
                        help_text="Time when the scoring event occurred",
                        verbose_name="Time Occurred",
                    ),
                ),
                (
                    "period",
                    models.CharField(
                        blank=True,
                        help_text="Game period (e.g., quarter, half) when the scoring occurred",
                        max_length=50,
                        verbose_name="Period",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Optional description of the scoring event",
                        verbose_name="Description",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        help_text="User who recorded this scoring event",
                        limit_choices_to={"role__in": ["scorekeeper", "admin"]},
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_score_details",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created By",
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        blank=True,
                        help_text="The player who scored (if applicable)",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="scoring_events",
                        to="teams.player",
                        verbose_name="Player",
                    ),
                ),
                (
                    "score",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="score_details",
                        to="scores.score",
                        verbose_name="Score",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="scoring_events",
                        to="teams.team",
                        verbose_name="Team",
                    ),
                ),
            ],
            options={
                "verbose_name": "Score Detail",
                "verbose_name_plural": "Score Details",
                "ordering": ["score", "time_occurred"],
            },
        ),
    ]
