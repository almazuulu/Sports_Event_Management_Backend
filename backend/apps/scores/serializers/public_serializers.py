from rest_framework import serializers
from ..models import Score


class PublicScoreSerializer(serializers.ModelSerializer):
    """
    Serializer for public (unauthenticated) access to scores.
    Returns limited information about game scores.
    """
    game_name = serializers.CharField(source='game.name', read_only=True)
    sport_type = serializers.CharField(source='game.sport_event.sport_type', read_only=True)
    sport_name = serializers.CharField(source='game.sport_event.get_sport_type_display', read_only=True)
    event_name = serializers.CharField(source='game.sport_event.event.name', read_only=True)
    team1_name = serializers.CharField(source='game.team1.name', read_only=True)
    team2_name = serializers.CharField(source='game.team2.name', read_only=True)
    winner_name = serializers.CharField(source='winner.name', read_only=True, allow_null=True)
    
    class Meta:
        model = Score
        fields = [
            'id', 'game_name', 'event_name', 'sport_type', 'sport_name',
            'team1_name', 'team2_name', 'final_score_team1', 'final_score_team2',
            'status', 'winner_name', 'is_draw'
        ]
        read_only_fields = fields


class PublicLiveScoreSerializer(serializers.ModelSerializer):
    """
    Serializer for live score updates for public viewing.
    Includes current score and game status.
    """
    game_name = serializers.CharField(source='game.name', read_only=True)
    team1_name = serializers.CharField(source='game.team1.name', read_only=True)
    team2_name = serializers.CharField(source='game.team2.name', read_only=True)
    location = serializers.CharField(source='game.location', read_only=True)
    scheduled_start = serializers.DateTimeField(source='game.scheduled_start', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    score_updates = serializers.SerializerMethodField()
    
    class Meta:
        model = Score
        fields = [
            'id', 'game_name', 'team1_name', 'team2_name', 'location',
            'scheduled_start', 'status', 'status_display',
            'final_score_team1', 'final_score_team2', 'score_updates'
        ]
        read_only_fields = fields
    
    def get_score_updates(self, obj):
        # Return the latest 5 scoring events
        score_details = obj.score_details.order_by('-time_occurred')[:5]
        result = []
        for detail in score_details:
            result.append({
                'team': detail.team.name,
                'points': detail.points,
                'time': detail.time_occurred.strftime('%H:%M:%S'),
                'period': detail.period,
                'description': detail.description
            })
        return result