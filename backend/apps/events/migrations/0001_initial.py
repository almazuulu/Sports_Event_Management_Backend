# Generated by Django 5.1.6 on 2025-03-05 07:19

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
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
                ("name", models.CharField(max_length=255, verbose_name="Name")),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="Description"),
                ),
                ("start_date", models.DateField(verbose_name="Start Date")),
                ("end_date", models.DateField(verbose_name="End Date")),
                ("location", models.CharField(max_length=255, verbose_name="Location")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("draft", "Draft"),
                            ("registration", "Registration"),
                            ("active", "Active"),
                            ("completed", "Completed"),
                            ("cancelled", "Cancelled"),
                        ],
                        default="draft",
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
                        help_text="Only administrators can create events",
                        limit_choices_to={"role": "admin"},
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="created_events",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created By",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        help_text="Administrator who last updated this event",
                        limit_choices_to={"role": "admin"},
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="updated_events",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Updated By",
                    ),
                ),
            ],
            options={
                "verbose_name": "Event",
                "verbose_name_plural": "Events",
                "ordering": ["start_date"],
                "permissions": [("view_event_admin", "Can view event as admin")],
            },
        ),
        migrations.CreateModel(
            name="SportEvent",
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
                    "sport_type",
                    models.CharField(
                        choices=[
                            ("football", "Football"),
                            ("basketball", "Basketball"),
                            ("volleyball", "Volleyball"),
                            ("cricket", "Cricket"),
                            ("tennis", "Tennis"),
                            ("badminton", "Badminton"),
                            ("swimming", "Swimming"),
                            ("athletics", "Athletics"),
                            ("chess", "Chess"),
                            ("other", "Other"),
                        ],
                        max_length=20,
                        verbose_name="Sport Type",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Name")),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="Description"),
                ),
                ("start_date", models.DateField(verbose_name="Start Date")),
                ("end_date", models.DateField(verbose_name="End Date")),
                (
                    "max_teams",
                    models.PositiveIntegerField(
                        default=0,
                        help_text="Set to 0 for unlimited teams",
                        verbose_name="Maximum Teams",
                    ),
                ),
                (
                    "registration_deadline",
                    models.DateTimeField(verbose_name="Registration Deadline"),
                ),
                ("rules", models.TextField(blank=True, verbose_name="Rules")),
                (
                    "scoring_system",
                    models.TextField(blank=True, verbose_name="Scoring System"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("scheduled", "Scheduled"),
                            ("registration", "Registration Open"),
                            ("registration_closed", "Registration Closed"),
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
                        help_text="Administrator who created this sport event",
                        limit_choices_to={"role": "admin"},
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="created_sport_events",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created By",
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sport_events",
                        to="events.event",
                        verbose_name="Event",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        help_text="Administrator who last updated this sport event",
                        limit_choices_to={"role": "admin"},
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="updated_sport_events",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Updated By",
                    ),
                ),
            ],
            options={
                "verbose_name": "Sport Event",
                "verbose_name_plural": "Sport Events",
                "ordering": ["event", "start_date"],
                "permissions": [
                    ("view_sportevent_admin", "Can view sport event as admin"),
                    ("assign_scorekeeper", "Can assign scorekeepers to sport event"),
                ],
                "constraints": [
                    models.UniqueConstraint(
                        fields=("event", "sport_type", "name"),
                        name="unique_sport_event",
                    )
                ],
            },
        ),
    ]
