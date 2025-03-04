from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from games.models import GamePlayer


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Game Player Example',
            value={
                'id': '3fa85f64-5717-4562-b3fc-2c963f66afad',
                'game_team': '3fa85f64-5717-4562-b3fc-2c963f66afa9',
                'game_name': 'Semifinals - Round 1',
                'team_name': 'Thunderbolts',
                'player': '3fa85f64-5717-4562-b3fc-2c963f66afae',
                'player_name': 'John Smith',
                'jersey_number': 23,
                'is_captain_for_game': True,
                'position': 'Forward',
                'notes': 'Starting player'
            },
            response_only=True,
        )
    ]
)
class GamePlayerSerializer(serializers.ModelSerializer):
    """
    Serializer for the GamePlayer model with detailed information.
    """
    game_name = serializers.CharField(source='game_team.game.name', read_only=True)
    team_name = serializers.CharField(source='game_team.team.name', read_only=True)
    player_name = serializers.CharField(source='player.get_full_name', read_only=True)
    jersey_number = serializers.IntegerField(source='player.jersey_number', read_only=True)
    
    class Meta:
        model = GamePlayer
        fields = [
            'id', 'game_team', 'game_name', 'team_name', 'player',
            'player_name', 'jersey_number', 'is_captain_for_game',
            'position', 'notes'
        ]
        read_only_fields = ['id']


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Game Player Create Example',
            value={
                'game_team': '3fa85f64-5717-4562-b3fc-2c963f66afa9',
                'player': '3fa85f64-5717-4562-b3fc-2c963f66afae',
                'is_captain_for_game': True,
                'position': 'Forward',
                'notes': 'Starting player'
            },
            request_only=True,
        ),
        OpenApiExample(
            'Game Player Bulk Create Example',
            value=[
                {
                    'game_team': '3fa85f64-5717-4562-b3fc-2c963f66afa9',
                    'player': '3fa85f64-5717-4562-b3fc-2c963f66afae',
                    'is_captain_for_game': True,
                    'position': 'Forward'
                },
                {
                    'game_team': '3fa85f64-5717-4562-b3fc-2c963f66afa9',
                    'player': '3fa85f64-5717-4562-b3fc-2c963f66afaf',
                    'position': 'Guard'
                }
            ],
            request_only=True,
        )
    ]
)
class GamePlayerCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for adding a player to a game team.
    """
    class Meta:
        model = GamePlayer
        fields = ['game_team', 'player', 'is_captain_for_game', 'position', 'notes']
    
    def validate(self, attrs):
        # Check if player is already selected for this game team
        game_team = attrs.get('game_team')
        player = attrs.get('player')
        
        if GamePlayer.objects.filter(game_team=game_team, player=player).exists():
            raise serializers.ValidationError({
                'player': _('This player is already selected for this game team.')
            })
        
        # Check if player belongs to the team
        if player.team != game_team.team:
            raise serializers.ValidationError({
                'player': _('This player does not belong to the team participating in this game.')
            })
        
        # Check if player is active
        if not player.is_active:
            raise serializers.ValidationError({
                'player': _('This player is not active and cannot be selected for games.')
            })
        
        # Ensure there's only one captain per game team
        if attrs.get('is_captain_for_game') and GamePlayer.objects.filter(
            game_team=game_team,
            is_captain_for_game=True
        ).exists():
            raise serializers.ValidationError({
                'is_captain_for_game': _('This game team already has a designated captain.')
            })
        
        return attrs


class GamePlayerUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a player selection for a game.
    Does not allow changing the player or game team.
    """
    class Meta:
        model = GamePlayer
        fields = ['is_captain_for_game', 'position', 'notes']
    
    def validate(self, attrs):
        # Ensure there's only one captain per game team
        if attrs.get('is_captain_for_game') and not self.instance.is_captain_for_game:
            if GamePlayer.objects.filter(
                game_team=self.instance.game_team,
                is_captain_for_game=True
            ).exists():
                raise serializers.ValidationError({
                    'is_captain_for_game': _('This game team already has a designated captain.')
                })
        
        return attrs


class GamePlayerBulkCreateSerializer(serializers.ListSerializer):
    """
    Serializer for bulk creating multiple player selections for a game team.
    """
    child = GamePlayerCreateSerializer()
    
    def validate(self, attrs):
        # Check for duplicates in the submitted data
        player_ids = [item['player'].id for item in attrs]
        if len(player_ids) != len(set(player_ids)):
            raise serializers.ValidationError(_('Duplicate players in the selection list.'))
        
        # Check for multiple captains
        captain_count = sum(1 for item in attrs if item.get('is_captain_for_game'))
        if captain_count > 1:
            raise serializers.ValidationError(_('Only one player can be designated as captain.'))
        
        # If bulk adding players and team already has a captain, check for conflicts
        if captain_count > 0 and attrs[0]['game_team'] and GamePlayer.objects.filter(
            game_team=attrs[0]['game_team'],
            is_captain_for_game=True
        ).exists():
            raise serializers.ValidationError(_('This game team already has a designated captain.'))
        
        return attrs