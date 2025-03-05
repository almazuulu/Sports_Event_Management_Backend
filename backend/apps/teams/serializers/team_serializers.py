from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from ..models import Team
from users.serializers import UserSerializer


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Team Example',
            value={
                'id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                'name': 'Thunderbolts',
                'description': 'Local basketball team from New York',
                'manager': {
                    'id': '3fa85f64-5717-4562-b3fc-2c963f66afa7',
                    'email': 'manager@example.com',
                    'first_name': 'John',
                    'last_name': 'Smith'
                },
                'team_captain': {
                    'id': '3fa85f64-5717-4562-b3fc-2c963f66afa8',
                    'first_name': 'Michael',
                    'last_name': 'Jordan',
                },
                'contact_email': 'team@example.com',
                'contact_phone': '+1234567890',
                'status': 'active',
                'player_count': 12,
                'created_at': '2025-01-15T12:00:00Z'
            },
            response_only=True,
        )
    ]
)
class TeamSerializer(serializers.ModelSerializer):
    """
    Serializer for the Team model with detailed information.
    """
    manager = UserSerializer(read_only=True)
    team_captain = serializers.SerializerMethodField()
    player_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Team
        fields = [
            'id', 'name', 'logo', 'description', 'manager',
            'team_captain', 'contact_email', 'contact_phone', 'status', 
            'player_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_team_captain(self, obj):
        if obj.team_captain:
            from ..serializers.player_serializers import PlayerSerializer
            return PlayerSerializer(obj.team_captain).data
        return None


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Team Create Example',
            value={
                'name': 'Thunderbolts',
                'description': 'Local basketball team from New York',
                'contact_email': 'team@example.com',
                'contact_phone': '+1234567890'
            },
            request_only=True,
        )
    ]
)
class TeamCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new team.
    The manager is automatically set to the current user.
    """
    class Meta:
        model = Team
        fields = ['name', 'logo', 'description', 'contact_email', 'contact_phone']
    
    def create(self, validated_data):
        # Set the current user as the team manager
        user = self.context['request'].user
        
        # Ensure the user has the team_manager role
        if user.role != 'team_manager':
            raise serializers.ValidationError({
                'manager': _('Only users with the Team Manager role can create teams.')
            })
        
        team = Team.objects.create(
            manager=user,
            **validated_data
        )
        return team


class TeamUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating an existing team.
    """
    class Meta:
        model = Team
        fields = ['name', 'logo', 'description', 'contact_email', 'contact_phone', 'status']
        read_only_fields = []
        
    def validate(self, attrs):
        # Ensure the current user is the team manager or an admin
        request_user = self.context['request'].user
        if request_user.role != 'admin' and self.instance.manager.id != request_user.id:
            raise serializers.ValidationError({
                'detail': _('Only the team manager or administrators can update this team.')
            })
        
        return attrs

class TeamDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed team information including players and registrations.
    """
    manager = UserSerializer(read_only=True)
    team_captain = serializers.SerializerMethodField()
    player_count = serializers.IntegerField(read_only=True)
    players = serializers.SerializerMethodField()
    registrations = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = [
            'id', 'name', 'logo', 'description', 'manager',
            'team_captain', 'contact_email', 'contact_phone', 'status', 
            'player_count', 'players', 'registrations',
            'created_at', 'updated_at'
        ]
        read_only_fields = fields
    
    def get_team_captain(self, obj):
        if obj.team_captain:
            from ..serializers.player_serializers import PlayerSerializer
            return PlayerSerializer(obj.team_captain).data
        return None
    
    def get_players(self, obj):
        # Import here to avoid circular imports
        from ..serializers.player_serializers import PlayerSerializer
        return PlayerSerializer(obj.players.filter(is_active=True), many=True).data
    
    def get_registrations(self, obj):
        # Import here to avoid circular imports
        from ..serializers.registration_serializers import TeamRegistrationSerializer
        return TeamRegistrationSerializer(obj.event_registrations.all(), many=True).data