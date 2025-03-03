from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from apps.games.models import Game, GameTeam


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Public Games List Example',
            value=[
                {
                    'id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                    'name': 'Semifinals - Round 1',
                    'sport_event_name': 'Annual Basketball Tournament 2025',
                    'location': 'Main Court',
                    'start_datetime': '2025-04-15T14:00:00Z',
                    'status': 'scheduled',
                    'teams': [
                        {
                            'team_name': 'Thunderbolts',
                            'designation': 'Team A'
                        },
                        {
                            'team_name': 'Lightning Strikes',
                            'designation': 'Team B'
                        }
                    ]
                }
            ],
            response_only=True,
        )
    ]
)
class PublicGameListSerializer(serializers.ModelSerializer):
    """
    Serializer for public games list with limited information.
    This serializer is designed for public endpoints that don't require authentication.
    """
    sport_event_name = serializers.CharField(source='sport_event.name', read_only=True)
    teams = serializers.SerializerMethodField()
    
    class Meta:
        model = Game
        fields = [
            'id', 'name', 'sport_event_name', 'location',
            'start_datetime', 'status', 'teams'
        ]
    
    def get_teams(self, obj):
        result = []
        for game_team in obj.game_teams.select_related('team').all():
            result.append({
                'team_name': game_team.team.name,
                'designation': game_team.get_designation_display()
            })
        return result


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Public Game Detail Example',
            value={
                'id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                'name': 'Semifinals - Round 1',
                'sport_event_name': 'Annual Basketball Tournament 2025',
                'description': 'First semifinal match',
                'location': 'Main Court',
                'start_datetime': '2025-04-15T14:00:00Z',
                'end_datetime': '2025-04-15T16:00:00Z',
                'status': 'scheduled',
                'teams': [
                    {
                        'team_name': 'Thunderbolts',
                        'designation': 'Team A',
                        'players': [
                            {
                                'name': 'John Smith',
                                'jersey_number': 23,
                                'position': 'Forward'
                            }
                        ]
                    },
                    {
                        'team_name': 'Lightning Strikes',
                        'designation': 'Team B',
                        'players': [
                            {
                                'name': 'Mike Johnson',
                                'jersey_number': 10,
                                'position': 'Guard'
                            }
                        ]
                    }
                ]
            },
            response_only=True,
        )
    ]
)
class PublicGameDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for public game details with team and player information.
    This serializer is designed for public endpoints that don't require authentication.
    """
    sport_event_name = serializers.CharField(source='sport_event.name', read_only=True)
    teams = serializers.SerializerMethodField()
    
    class Meta:
        model = Game
        fields = [
            'id', 'name', 'sport_event_name', 'description', 'location',
            'start_datetime', 'end_datetime', 'status', 'teams'
        ]
    
    def get_teams(self, obj):
        result = []
        for game_team in obj.game_teams.select_related('team').all():
            # Get players for this game team
            players = []
            for player in game_team.selected_players.select_related('player').all():
                players.append({
                    'name': player.player.get_full_name(),
                    'jersey_number': player.player.jersey_number,
                    'position': player.position
                })
            
            result.append({
                'team_name': game_team.team.name,
                'designation': game_team.get_designation_display(),
                'players': players
            })
        
        return result


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Upcoming Games Example',
            value=[
                {
                    'id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                    'name': 'Semifinals - Round 1',
                    'sport_event_name': 'Annual Basketball Tournament 2025',
                    'start_datetime': '2025-04-15T14:00:00Z',
                    'location': 'Main Court',
                    'teams': [
                        'Thunderbolts vs Lightning Strikes'
                    ]
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
    sport_event_name = serializers.CharField(source='sport_event.name', read_only=True)
    teams = serializers.SerializerMethodField()
    
    class Meta:
        model = Game
        fields = [
            'id', 'name', 'sport_event_name', 'start_datetime',
            'location', 'teams'
        ]
    
    def get_teams(self, obj):
        teams = obj.game_teams.select_related('team').all()
        if len(teams) == 2:
            return [f"{teams[0].team.name} vs {teams[1].team.name}"]
        else:
            return [team.team.name for team in teams]