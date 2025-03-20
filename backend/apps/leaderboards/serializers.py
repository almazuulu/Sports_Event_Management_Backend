from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from .models import Leaderboard, LeaderboardEntry


class LeaderboardEntrySerializer(serializers.ModelSerializer):
    """
    Serializer for the LeaderboardEntry model.
    """
    team_name = serializers.CharField(source='team.name', read_only=True)
    
    class Meta:
        model = LeaderboardEntry
        fields = [
            'id', 'team', 'team_name', 'position', 'played', 'won', 'drawn', 'lost',
            'points', 'goals_for', 'goals_against', 'goal_difference',
            'clean_sheets', 'yellow_cards', 'red_cards'
        ]
        read_only_fields = fields


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Leaderboard Example',
            value={
                'id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                'sport_event': '3fa85f64-5717-4562-b3fc-2c963f66afa7',
                'sport_event_name': 'Annual Football Tournament 2025',
                'last_updated': '2025-03-15T14:30:00Z',
                'is_final': False,
                'entries': [
                    {
                        'id': '3fa85f64-5717-4562-b3fc-2c963f66afa8',
                        'team': '3fa85f64-5717-4562-b3fc-2c963f66afa9',
                        'team_name': 'Eagles',
                        'position': 1,
                        'played': 5,
                        'won': 4,
                        'drawn': 0,
                        'lost': 1,
                        'points': 12,
                        'goals_for': 12,
                        'goals_against': 5,
                        'goal_difference': 7,
                        'clean_sheets': 2,
                        'yellow_cards': 3,
                        'red_cards': 0
                    }
                ]
            },
            response_only=True
        )
    ]
)
class LeaderboardSerializer(serializers.ModelSerializer):
    """
    Serializer for the Leaderboard model.
    """
    sport_event_name = serializers.CharField(source='sport_event.name', read_only=True)
    entries = LeaderboardEntrySerializer(many=True, read_only=True)
    
    class Meta:
        model = Leaderboard
        fields = ['id', 'sport_event', 'sport_event_name', 'last_updated', 'is_final', 'entries']
        read_only_fields = fields


class LeaderboardSummarySerializer(serializers.ModelSerializer):
    """
    Simplified serializer for Leaderboard model without entries.
    Used for listing leaderboards.
    """
    sport_event_name = serializers.CharField(source='sport_event.name', read_only=True)
    sport_type = serializers.CharField(source='sport_event.get_sport_type_display', read_only=True)
    teams_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Leaderboard
        fields = ['id', 'sport_event', 'sport_event_name', 'sport_type', 'last_updated', 'is_final', 'teams_count']
        read_only_fields = fields
    
    def get_teams_count(self, obj):
        return obj.entries.count()


class TeamLeaderboardSerializer(serializers.Serializer):
    """
    Serializer for a team's standings across multiple leaderboards.
    """
    sport_event_id = serializers.CharField()
    sport_event_name = serializers.CharField()
    position = serializers.IntegerField()
    played = serializers.IntegerField()
    won = serializers.IntegerField()
    drawn = serializers.IntegerField()
    lost = serializers.IntegerField()
    points = serializers.IntegerField()
    goals_for = serializers.IntegerField()
    goals_against = serializers.IntegerField()
    goal_difference = serializers.IntegerField()
    is_final = serializers.BooleanField()