from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from games.models import Game


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Game Example",
            value={
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "sport_event": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
                "sport_event_name": "Annual Basketball Tournament 2025",
                "name": "Semifinals - Round 1",
                "description": "First semifinal match",
                "location": "Main Court",
                "start_datetime": "2025-04-15T14:00:00Z",
                "end_datetime": "2025-04-15T16:00:00Z",
                "status": "scheduled",
                "scorekeeper": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
                "scorekeeper_name": "John Scorer",
                "teams": [
                    {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
                        "team": "3fa85f64-5717-4562-b3fc-2c963f66afaa",
                        "team_name": "Thunderbolts",
                        "designation": "team_a",
                        "designation_display": "Team A",
                    },
                    {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afab",
                        "team": "3fa85f64-5717-4562-b3fc-2c963f66afac",
                        "team_name": "Lightning Strikes",
                        "designation": "team_b",
                        "designation_display": "Team B",
                    },
                ],
                "created_at": "2025-04-01T10:30:00Z",
            },
            response_only=True,
        )
    ]
)
class GameSerializer(serializers.ModelSerializer):
    """
    Serializer for the Game model with detailed information.
    """

    sport_event_name = serializers.CharField(source="sport_event.name", read_only=True)
    scorekeeper_name = serializers.SerializerMethodField()
    teams = serializers.SerializerMethodField()
    time_display = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = [
            "id",
            "sport_event",
            "sport_event_name",
            "name",
            "description",
            "location",
            "start_datetime",
            "end_datetime",
            "time_display",
            "status",
            "scorekeeper",
            "scorekeeper_name",
            "teams",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def get_scorekeeper_name(self, obj):
        if obj.scorekeeper:
            return obj.scorekeeper.get_full_name()
        return None

    def get_time_display(self, obj):
        return obj.start_datetime.strftime("%H:%M")

    def get_teams(self, obj):
        from ..serializers.game_team_serializers import GameTeamSerializer

        return GameTeamSerializer(obj.game_teams.all(), many=True).data


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Game Create Example",
            value={
                "sport_event": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
                "name": "Semifinals - Round 1",
                "description": "First semifinal match",
                "location": "Main Court",
                "start_datetime": "2025-04-15T14:00:00Z",
                "end_datetime": "2025-04-15T16:00:00Z",
                "scorekeeper": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
            },
            request_only=True,
        )
    ]
)
class GameCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new game with scorekeeper availability checking.
    """

    class Meta:
        model = Game
        fields = [
            "sport_event",
            "name",
            "description",
            "location",
            "start_datetime",
            "end_datetime",
            "scorekeeper",
        ]

    def validate(self, attrs):
        # Base validation from the original serializer
        # Ensure start time is before end time
        if attrs.get("start_datetime") >= attrs.get("end_datetime"):
            raise serializers.ValidationError(
                {"end_datetime": _("End time must be after start time.")}
            )

        # Ensure game is scheduled in the future
        if attrs.get("start_datetime") < timezone.now():
            raise serializers.ValidationError(
                {"start_datetime": _("Game must be scheduled for a future time.")}
            )

        # Ensure the sport event is active or in registration phase
        sport_event = attrs.get("sport_event")
        if sport_event.status not in ["registration", "ongoing"]:
            raise serializers.ValidationError(
                {
                    "sport_event": _(
                        "Games can only be scheduled for active or registration phase sport events."
                    )
                }
            )

        # Check scorekeeper availability
        scorekeeper = attrs.get("scorekeeper")
        if scorekeeper:
            # First, validate that the scorekeeper has the correct role
            if scorekeeper.role != "scorekeeper":
                raise serializers.ValidationError(
                    {"scorekeeper": _("Selected user is not a scorekeeper.")}
                )

            # Then check if they're already assigned to another game at the same time
            start_datetime = attrs.get("start_datetime")
            end_datetime = attrs.get("end_datetime")

            # Find any overlapping games
            # Game times would overlap if: (new_start < existing_end) AND (new_end > existing_start)
            conflicting_games = Game.objects.filter(
                scorekeeper=scorekeeper,
                end_datetime__gt=start_datetime,
                start_datetime__lt=end_datetime,
                status__in=["scheduled", "ongoing"],
            )

            # Exclude current game if we're updating
            instance = self.instance
            if instance:
                conflicting_games = conflicting_games.exclude(pk=instance.pk)

            if conflicting_games.exists():
                conflict = conflicting_games.first()
                raise serializers.ValidationError(
                    {
                        "scorekeeper": _(
                            'This scorekeeper is already assigned to "{game_name}" during this time '
                            "({start} to {end})."
                        ).format(
                            game_name=conflict.name,
                            start=conflict.start_datetime.strftime("%Y-%m-%d %H:%M"),
                            end=conflict.end_datetime.strftime("%Y-%m-%d %H:%M"),
                        )
                    }
                )

        return attrs

    def create(self, validated_data):
        # Set the created_by field to the current user
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class GameUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating an existing game with scorekeeper availability checking.
    """

    class Meta:
        model = Game
        fields = [
            "name",
            "description",
            "location",
            "start_datetime",
            "end_datetime",
            "scorekeeper",
        ]

    def validate(self, attrs):
        # Get the current instance for partial updates
        instance = getattr(self, "instance", None)

        # Combine with new data for validation
        start_datetime = attrs.get(
            "start_datetime", instance.start_datetime if instance else None
        )
        end_datetime = attrs.get(
            "end_datetime", instance.end_datetime if instance else None
        )

        # Ensure start time is before end time
        if start_datetime and end_datetime and start_datetime >= end_datetime:
            raise serializers.ValidationError(
                {"end_datetime": _("End time must be after start time.")}
            )

        # If game is already ongoing or completed, don't allow schedule changes
        if (
            instance
            and instance.status in ["ongoing", "completed"]
            and ("start_datetime" in attrs or "end_datetime" in attrs)
        ):
            raise serializers.ValidationError(
                {
                    "status": _(
                        "Cannot change schedule for games that are ongoing or completed."
                    )
                }
            )

        # Check scorekeeper availability if a scorekeeper is being assigned or schedule is changing
        scorekeeper = attrs.get(
            "scorekeeper", instance.scorekeeper if instance else None
        )
        schedule_changed = "start_datetime" in attrs or "end_datetime" in attrs
        scorekeeper_changed = "scorekeeper" in attrs

        if scorekeeper and (schedule_changed or scorekeeper_changed):
            # First, validate that the scorekeeper has the correct role
            if scorekeeper.role != "scorekeeper":
                raise serializers.ValidationError(
                    {"scorekeeper": _("Selected user is not a scorekeeper.")}
                )

            # Then check if they're already assigned to another game at the same time
            # Find any overlapping games
            # Game times would overlap if: (new_start < existing_end) AND (new_end > existing_start)
            conflicting_games = Game.objects.filter(
                scorekeeper=scorekeeper,
                end_datetime__gt=start_datetime,
                start_datetime__lt=end_datetime,
                status__in=["scheduled", "ongoing"],
            ).exclude(pk=instance.pk)

            if conflicting_games.exists():
                conflict = conflicting_games.first()
                raise serializers.ValidationError(
                    {
                        "scorekeeper": _(
                            'This scorekeeper is already assigned to "{game_name}" during this time '
                            "({start} to {end})."
                        ).format(
                            game_name=conflict.name,
                            start=conflict.start_datetime.strftime("%Y-%m-%d %H:%M"),
                            end=conflict.end_datetime.strftime("%Y-%m-%d %H:%M"),
                        )
                    }
                )

        return attrs

    def update(self, instance, validated_data):
        # Set the updated_by field to the current user
        validated_data["updated_by"] = self.context["request"].user
        return super().update(instance, validated_data)


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Game Status Update Example",
            value={"status": "ongoing"},
            request_only=True,
        )
    ]
)
class GameStatusUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating only the status of a game.
    For use by scorekeepers and admins.
    """

    class Meta:
        model = Game
        fields = ["status"]

    def validate_status(self, value):
        # Get current status
        current_status = self.instance.status

        # Define valid status transitions
        valid_transitions = {
            "scheduled": ["ongoing", "cancelled"],
            "ongoing": ["completed", "cancelled"],
            "completed": [],  # No transitions allowed from completed
            "cancelled": [],  # No transitions allowed from cancelled
        }

        if value not in valid_transitions.get(current_status, []):
            raise serializers.ValidationError(
                _("Invalid status transition from {} to {}.").format(
                    self.instance.get_status_display(),
                    dict(Game.STATUS_CHOICES).get(value),
                )
            )

        return value

    def update(self, instance, validated_data):
        # Set the updated_by field to the current user
        validated_data["updated_by"] = self.context["request"].user
        return super().update(instance, validated_data)


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Public Game Example",
            value={
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "name": "Semifinals - Round 1",
                "sport_event_name": "Annual Basketball Tournament 2025",
                "location": "Main Court",
                "start_datetime": "2025-04-15T14:00:00Z",
                "end_datetime": "2025-04-15T16:00:00Z",
                "status": "scheduled",
                "teams": [
                    {"team_name": "Thunderbolts", "designation_display": "Team A"},
                    {"team_name": "Lightning Strikes", "designation_display": "Team B"},
                ],
            },
            response_only=True,
        )
    ]
)
class PublicGameSerializer(serializers.ModelSerializer):
    """
    Serializer for public game information.
    Contains limited information for use in public API endpoints.
    """

    sport_event_name = serializers.CharField(source="sport_event.name", read_only=True)
    teams = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = [
            "id",
            "name",
            "sport_event_name",
            "location",
            "start_datetime",
            "end_datetime",
            "status",
            "teams",
        ]

    def get_teams(self, obj):
        result = []
        for game_team in obj.game_teams.select_related("team").all():
            result.append(
                {
                    "team_name": game_team.team.name,
                    "designation_display": game_team.get_designation_display(),
                }
            )
        return result


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Game List Example",
            value={
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "name": "Semifinals - Round 1",
                "sport_event_name": "Annual Basketball Tournament 2025",
                "start_datetime": "2025-04-15T14:00:00Z",
                "location": "Main Court",
                "status": "scheduled",
                "teams": [
                    {"team_name": "Thunderbolts", "designation": "Team A"},
                    {"team_name": "Lightning Strikes", "designation": "Team B"},
                ],
            },
            response_only=True,
        )
    ]
)
class GameListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing games with team information.
    Used for all list views of games.
    """

    sport_event_name = serializers.CharField(source="sport_event.name", read_only=True)
    teams = serializers.SerializerMethodField()
    time_display = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = [
            "id",
            "name",
            "sport_event_name",
            "start_datetime",
            "time_display",
            "location",
            "status",
            "teams",
        ]

    def get_teams(self, obj):
        result = []
        for game_team in obj.game_teams.select_related("team").all():
            result.append(
                {
                    "team_name": game_team.team.name,
                    "designation": game_team.get_designation_display(),
                }
            )
        return result

    def get_time_display(self, obj):
        return obj.start_datetime.strftime("%H:%M")
    

class ScorekeeperAssignmentSerializer(GameListSerializer):
    game_id = serializers.CharField(source='id', read_only=True)
    
    class Meta:
        model = Game
        fields = ['game_id', 'name', 'sport_event_name', 'start_datetime', 'time_display', 
                 'location', 'status', 'teams']

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Scorekeeper Game List Example",
            value={
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "name": "Semifinals - Round 1",
                "sport_event_name": "Annual Basketball Tournament 2025",
                "start_datetime": "2025-04-15T14:00:00Z",
                "end_datetime": "2025-04-15T16:00:00Z",
                "location": "Main Court",
                "status": "scheduled",
                "teams": [
                    {"team_name": "Thunderbolts", "designation_display": "Team A"},
                    {"team_name": "Lightning Strikes", "designation_display": "Team B"},
                ],
            },
            response_only=True,
        )
    ]
)
class ScorekeeperGameSerializer(serializers.ModelSerializer):
    """
    Serializer for games assigned to a scorekeeper.
    Focuses on information needed for scorekeeping.
    """

    sport_event_name = serializers.CharField(source="sport_event.name", read_only=True)
    teams = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = [
            "id",
            "name",
            "sport_event_name",
            "start_datetime",
            "end_datetime",
            "location",
            "status",
            "teams",
        ]

    def get_teams(self, obj):
        result = []
        for game_team in obj.game_teams.select_related("team").all():
            result.append(
                {
                    "id": game_team.id,
                    "team_name": game_team.team.name,
                    "designation": game_team.designation,
                    "designation_display": game_team.get_designation_display(),
                }
            )
        return result


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Game Detail Example",
            value={
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "sport_event": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
                "sport_event_name": "Annual Basketball Tournament 2025",
                "name": "Semifinals - Round 1",
                "description": "First semifinal match",
                "location": "Main Court",
                "start_datetime": "2025-04-15T14:00:00Z",
                "end_datetime": "2025-04-15T16:00:00Z",
                "status": "scheduled",
                "scorekeeper_name": "John Scorer",
                "teams": [
                    {
                        "team_name": "Thunderbolts",
                        "designation": "Team A",
                        "players": [
                            {
                                "name": "John Smith",
                                "jersey_number": 23,
                                "position": "Forward",
                            }
                        ],
                    }
                ],
                "created_at": "2025-04-01T10:30:00Z",
            },
            response_only=True,
        )
    ]
)
class GameDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for a game including teams and players.
    """

    sport_event_name = serializers.CharField(source="sport_event.name", read_only=True)
    scorekeeper_name = serializers.SerializerMethodField()
    teams = serializers.SerializerMethodField()
    time_display = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = [
            "id",
            "sport_event",
            "sport_event_name",
            "name",
            "description",
            "location",
            "start_datetime",
            "end_datetime",
            "time_display",
            "status",
            "scorekeeper",
            "scorekeeper_name",
            "teams",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_scorekeeper_name(self, obj):
        if obj.scorekeeper:
            return obj.scorekeeper.get_full_name()
        return None

    def get_time_display(self, obj):
        return obj.start_datetime.strftime("%H:%M")

    def get_teams(self, obj):
        result = []
        for game_team in obj.game_teams.select_related("team").all():
            team_data = {
                "team_name": game_team.team.name,
                "designation": game_team.get_designation_display(),
            }

            # Include additional data for authenticated users
            if (
                self.context.get("request")
                and self.context["request"].user.is_authenticated
            ):
                team_data["id"] = game_team.id
                team_data["team"] = game_team.team.id

            # Always include player data
            players = []
            for player in game_team.selected_players.select_related("player").all():
                player_data = {
                    "name": player.player.get_full_name(),
                    "jersey_number": player.player.jersey_number,
                    "position": player.position,
                }

                # Include additional player data for authenticated users
                if (
                    self.context.get("request")
                    and self.context["request"].user.is_authenticated
                ):
                    player_data["id"] = player.id
                    player_data["player"] = player.player.id
                    player_data["is_captain_for_game"] = player.is_captain_for_game
                    player_data["notes"] = player.notes

                players.append(player_data)

            team_data["players"] = players
            result.append(team_data)

        return result


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Upcoming Games Example",
            value=[
                {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "name": "Semifinals - Round 1",
                    "sport_event_name": "Annual Basketball Tournament 2025",
                    "start_datetime": "2025-04-15T14:00:00Z",
                    "location": "Main Court",
                    "teams": ["Thunderbolts vs Lightning Strikes"],
                }
            ],
            response_only=True,
        )
    ]
)
class UpcomingGamesSerializer(serializers.ModelSerializer):
    """
    Serializer for upcoming games with simplified information.
    Used for homepage or dashboard widgets.
    """

    sport_event_name = serializers.CharField(source="sport_event.name", read_only=True)
    teams = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = [
            "id",
            "name",
            "sport_event_name",
            "start_datetime",
            "location",
            "teams",
        ]

    def get_teams(self, obj):
        teams = obj.game_teams.select_related("team").all()
        if len(teams) == 2:
            return [f"{teams[0].team.name} vs {teams[1].team.name}"]
        else:
            return [team.team.name for team in teams]
