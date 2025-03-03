from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from apps.games.models import GameTeam


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Game Team Example',
            value={
                'id': '3fa85f64-5717-4562-b3fc-2c963f66afa9',
                'game': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                'game_name': 'Semifinals - Round 1',
                'team': '3fa85f64-5717-4562-b3fc-2c963f66afaa',
                'team_name': 'Thunderbolts',
                'designation': 'team_a',
                'designation_display': 'Team A',
                'selected_players_count': 10
            },
            response_only=True,
        )
    ]
)
class GameTeamSerializer(serializers.ModelSerializer):
    """
    Serializer for the GameTeam model with detailed information.
    """
    game_name = serializers.CharField(source='game.name', read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)
    designation_display = serializers.CharField(source='get_designation_display', read_only=True)
    selected_players_count = serializers.SerializerMethodField()
    
    class Meta:
        model = GameTeam
        fields = [
            'id', 'game', 'game_name', 'team', 'team_name',
            'designation', 'designation_display', 'selected_players_count'
        ]
        read_only_fields = ['id']
    
    def get_selected_players_count(self, obj):
        return obj.selected_players.count()


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Game Team Create Example',
            value={
                'game': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                'team': '3fa85f64-5717-4562-b3fc-2c963f66afaa',
                'designation': 'team_a'
            },
            request_only=True,
        )
    ]
)
class GameTeamCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new game team assignment.
    """
    class Meta:
        model = GameTeam
        fields = ['game', 'team', 'designation']
    
    def validate(self, attrs):
        # Check if team is already assigned to this game
        game = attrs.get('game')
        team = attrs.get('team')
        
        if GameTeam.objects.filter(game=game, team=team).exists():
            raise serializers.ValidationError({
                'team': _('This team is already assigned to this game.')
            })
        
        # Check if designation is already used in this game
        designation = attrs.get('designation')
        if GameTeam.objects.filter(game=game, designation=designation).exists():
            raise serializers.ValidationError({
                'designation': _('This designation is already used in this game.')
            })
        
        # Check if team is registered for the sport event
        if not team.event_registrations.filter(
            sport_event=game.sport_event,
            status='approved'
        ).exists():
            raise serializers.ValidationError({
                'team': _('This team is not registered for the sport event.')
            })
        
        # Check if game already has maximum number of teams
        # This will depend on the sport type
        existing_teams_count = game.game_teams.count()
        
        # Generic limit: 2 teams per game for most sports
        # Could be customized based on sport_event.sport_type
        if existing_teams_count >= 2:
            raise serializers.ValidationError({
                'game': _('This game already has the maximum number of teams assigned.')
            })
        
        return attrs


class GameTeamUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a game team assignment.
    Only allows updating the designation.
    """
    class Meta:
        model = GameTeam
        fields = ['designation']
    
    def validate_designation(self, value):
        game = self.instance.game
        
        # Check if new designation is already used in this game
        if value != self.instance.designation and GameTeam.objects.filter(
            game=game,
            designation=value
        ).exists():
            raise serializers.ValidationError(
                _('This designation is already used in this game.')
            )
        
        return value
    
@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Game Team With Players Example',
            value={
                'id': '3fa85f64-5717-4562-b3fc-2c963f66afa9',
                'game': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                'game_name': 'Semifinals - Round 1',
                'team': '3fa85f64-5717-4562-b3fc-2c963f66afaa',
                'team_name': 'Thunderbolts',
                'designation': 'team_a',
                'designation_display': 'Team A',
                'selected_players': [
                    {
                        'id': '3fa85f64-5717-4562-b3fc-2c963f66afad',
                        'player': '3fa85f64-5717-4562-b3fc-2c963f66afae',
                        'player_name': 'John Smith',
                        'jersey_number': 23,
                        'is_captain_for_game': True,
                        'position': 'Forward'
                    }
                ]
            },
            response_only=True,
        )
    ]
)
class GameTeamDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for a game team including all selected players.
    """
    game_name = serializers.CharField(source='game.name', read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)
    designation_display = serializers.CharField(source='get_designation_display', read_only=True)
    selected_players = serializers.SerializerMethodField()
    
    class Meta:
        model = GameTeam
        fields = [
            'id', 'game', 'game_name', 'team', 'team_name',
            'designation', 'designation_display', 'selected_players'
        ]
        read_only_fields = ['id']
    
    def get_selected_players(self, obj):
        players = []
        for player in obj.selected_players.select_related('player').all():
            players.append({
                'id': player.id,
                'player': player.player.id,
                'player_name': player.player.get_full_name(),
                'jersey_number': player.player.jersey_number,
                'is_captain_for_game': player.is_captain_for_game,
                'position': player.position,
                'notes': player.notes
            })
        return players