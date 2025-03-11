from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from ..models import Player


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Player Example',
            value={
                'id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                'team': '3fa85f64-5717-4562-b3fc-2c963f66afa7',
                'team_name': 'Thunderbolts',
                'first_name': 'Michael',
                'last_name': 'Johnson',
                'jersey_number': 23,
                'position': 'Forward',
                'is_captain': False,
                'date_of_birth': '1990-05-15',
                'is_active': True,
                'joined_date': '2024-01-10'
            },
            response_only=True,
        )
    ]
)
class PlayerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Player model with detailed information.
    """
    team_name = serializers.CharField(source='team.name', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True, allow_null=True)
    
    class Meta:
        model = Player
        fields = [
            'id', 'team', 'team_name', 'user', 'user_email',
            'first_name', 'last_name', 'jersey_number', 
            'position', 'is_captain', 'date_of_birth', 'photo',
            'is_active', 'joined_date', 'notes'
        ]
        read_only_fields = ['id']


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Player Create Example',
            value={
                'team': '97e9b1c5-753c-4d94-8239-a23fadbc6f28',
                'user': '44b2cd26-21f2-4480-a013-e4bce0e2ba22',
                'jersey_number': 23,
                'position': 'Forward',
                'date_of_birth': '1990-05-15',
                'joined_date': '2024-01-10'
            },
            request_only=True,
            summary="Create a player with an existing user"
        )
    ]
)
class PlayerCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for adding a player to a team.
    A player can only be created with an existing user who has the role 'player'.
    The player's first and last name are taken from the user's data.
    """
    class Meta:
        model = Player
        fields = [
            'team', 'user', 'jersey_number', 'position', 
            'date_of_birth', 'joined_date', 'is_active', 'notes'
        ]
    
    def validate_user(self, value):
        """Check that the user has the role 'player'"""
        if not value:
            raise serializers.ValidationError(_('User is required.'))
        
        if value.role != 'player':
            raise serializers.ValidationError(_(
                'User must have the role "player". Current role is "{0}".'.format(value.role)
            ))
        
        return value
    
    def validate(self, attrs):
        # Check that jersey_number is unique within the team
        team = attrs.get('team')
        jersey_number = attrs.get('jersey_number')
        
        # Check for unique jersey number within the team
        if Player.objects.filter(team=team, jersey_number=jersey_number).exists():
            raise serializers.ValidationError({
                'error': _('This jersey number is already in use by another player in this team.')
            })
        
        # Check that the user is not already associated with another player in this team
        user = attrs.get('user')
        if Player.objects.filter(team=team, user=user).exists():
            raise serializers.ValidationError({
                'error': _('This user is already registered as a player in this team.')
            })
        
        # Check if request exists and user is authenticated
        request = self.context.get('request')
        if not request or not request.user or not request.user.is_authenticated:
            raise serializers.ValidationError({
                'error': _('Authentication required to create a player.')
            })
        
        # Check access rights (only after confirming user is authenticated)
        request_user = request.user
        if not hasattr(request_user, 'role') or (request_user.role != 'admin' and team.manager.id != request_user.id):
            raise serializers.ValidationError({
                'error': _('Only the team manager or administrators can add players to this team.')
            })
        
        return attrs

    def create(self, validated_data):
        user = validated_data.get('user')
        validated_data['first_name'] = user.first_name
        validated_data['last_name'] = user.last_name
            
        return super().create(validated_data)


class PlayerUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating an existing player.
    """
    class Meta:
        model = Player
        fields = [
            'first_name', 'last_name', 'jersey_number', 
            'position', 'is_captain', 'date_of_birth', 'photo',
            'is_active', 'notes'
        ]
    
    def validate(self, attrs):
        # Check if jersey number is unique within the team if changed
        if 'jersey_number' in attrs and attrs['jersey_number'] != self.instance.jersey_number:
            team = self.instance.team
            jersey_number = attrs['jersey_number']
            
            if Player.objects.filter(team=team, jersey_number=jersey_number).exists():
                raise serializers.ValidationError({
                    'error': _('This jersey number is already in use by another player in this team.')
                })
        
        # Check if request exists and user is authenticated
        request = self.context.get('request')
        if not request or not request.user or not request.user.is_authenticated:
            raise serializers.ValidationError({
                'error': _('Authentication required to update a player.')
            })
        
        # Ensure the current user is the team manager or an admin (only after confirming user is authenticated)
        request_user = request.user
        if not hasattr(request_user, 'role') or (request_user.role != 'admin' and self.instance.team.manager.id != request_user.id):
            raise serializers.ValidationError({
                'error': _('Only the team manager or administrators can update this player.')
            })
        
        # Additional check: only the team manager or admin can designate the captain
        if 'is_captain' in attrs and attrs['is_captain']:
            if not hasattr(request_user, 'role') or (request_user.role != 'admin' and self.instance.team.manager.id != request_user.id):
                raise serializers.ValidationError({
                    'error': _('Only the team manager or administrators can designate team captains.')
                })
        
        return attrs
    

class TeamCaptainSerializer(serializers.Serializer):
    """
    Simple serializer for setting a player as team captain.
    No fields are required as the player ID is taken from the URL.
    """
    class Meta:
        model = Player
        fields = []
        
