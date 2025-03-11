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
    # Use SerializerMethodField to properly handle game_teams
    team1_name = serializers.SerializerMethodField()
    team2_name = serializers.SerializerMethodField()
    winner_name = serializers.CharField(source='winner.name', read_only=True, allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    # Add additional stats for Premier League-style display
    goal_difference_team1 = serializers.SerializerMethodField()
    goal_difference_team2 = serializers.SerializerMethodField()
    
    class Meta:
        model = Score
        fields = [
            'id', 'game_name', 'event_name', 'sport_type', 'sport_name',
            'team1_name', 'team2_name', 'final_score_team1', 'final_score_team2',
            'goals_for_team1', 'goals_against_team1', 'goal_difference_team1',
            'goals_for_team2', 'goals_against_team2', 'goal_difference_team2',
            'status', 'status_display', 'winner_name', 'is_draw'
        ]
        read_only_fields = fields
    
    def get_team1_name(self, obj):
        team1_relation = obj.game.game_teams.filter(designation__in=['team_a', 'home']).first()
        if team1_relation:
            return team1_relation.team.name
        return None
    
    def get_team2_name(self, obj):
        team2_relation = obj.game.game_teams.filter(designation__in=['team_b', 'away']).first()
        if team2_relation:
            return team2_relation.team.name
        return None
    
    def get_goal_difference_team1(self, obj):
        return obj.calculate_goal_difference(1)
    
    def get_goal_difference_team2(self, obj):
        return obj.calculate_goal_difference(2)


class PublicLiveScoreSerializer(serializers.ModelSerializer):
    """
    Serializer for live score updates for public viewing.
    Includes current score and game status.
    """
    game_name = serializers.CharField(source='game.name', read_only=True)
    # Use SerializerMethodField to properly handle game_teams
    team1_name = serializers.SerializerMethodField()
    team2_name = serializers.SerializerMethodField()
    location = serializers.CharField(source='game.location', read_only=True)
    scheduled_start = serializers.DateTimeField(source='game.start_datetime', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    score_updates = serializers.SerializerMethodField()
    # Add match day information
    match_day = serializers.CharField(source='game.sport_event.name', read_only=True)
    
    class Meta:
        model = Score
        fields = [
            'id', 'game_name', 'match_day', 'team1_name', 'team2_name', 'location',
            'scheduled_start', 'status', 'status_display', 'time_elapsed',
            'final_score_team1', 'final_score_team2', 'score_updates'
        ]
        read_only_fields = fields
    
    def get_team1_name(self, obj):
        team1_relation = obj.game.game_teams.filter(designation__in=['team_a', 'home']).first()
        if team1_relation:
            return team1_relation.team.name
        return None
    
    def get_team2_name(self, obj):
        team2_relation = obj.game.game_teams.filter(designation__in=['team_b', 'away']).first()
        if team2_relation:
            return team2_relation.team.name
        return None
    
    def get_score_updates(self, obj):
        # Return the latest 5 scoring events with enhanced details
        score_details = obj.score_details.all().order_by('-time_occurred')[:5]
        result = []
        for detail in score_details:
            player_name = None
            if detail.player:
                player_name = f"{detail.player.first_name} {detail.player.last_name}"
            
            assisted_by_name = None
            if detail.assisted_by:
                assisted_by_name = f"{detail.assisted_by.first_name} {detail.assisted_by.last_name}"
            
            result.append({
                'team': detail.team.name,
                'player': player_name,
                'assisted_by': assisted_by_name,
                'points': detail.points,
                'event_type': detail.event_type,
                'time': detail.time_occurred.strftime('%H:%M:%S'),
                'minute': detail.minute,
                'period': detail.period,
                'description': detail.description
            })
        return result


class LeaderboardScoreSerializer(serializers.ModelSerializer):
    """
    Serializer for scores displayed in the leaderboard.
    Similar to Premier League table view with standings information.
    """
    team_name = serializers.SerializerMethodField()
    played = serializers.IntegerField(read_only=True)
    won = serializers.IntegerField(read_only=True)
    drawn = serializers.IntegerField(read_only=True)
    lost = serializers.IntegerField(read_only=True)
    goals_for = serializers.IntegerField(read_only=True)
    goals_against = serializers.IntegerField(read_only=True)
    goal_difference = serializers.IntegerField(read_only=True)
    points = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Score
        fields = [
            'team_name', 'played', 'won', 'drawn', 'lost',
            'goals_for', 'goals_against', 'goal_difference', 'points'
        ]
        read_only_fields = fields
    
    def get_team_name(self, obj):
        # This would be used in a custom query that aggregates team stats
        return obj['team_name'] if 'team_name' in obj else None