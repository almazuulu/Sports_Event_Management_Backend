from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from ..models import Player, Team


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
            'position', 'date_of_birth', 'photo',
            'is_active', 'joined_date', 'notes'
        ]
        read_only_fields = ['id']

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Player Create Example',
            value={
                'team': '3fa85f64-5717-4562-b3fc-2c963f66afa7',
                'first_name': 'Michael',
                'last_name': 'Johnson',
                'jersey_number': 23,
                'position': 'Forward',
                'date_of_birth': '1990-05-15',
                'joined_date': '2024-01-10',
                'user': '3fa85f64-5717-4562-b3fc-2c963f66afa8'  # Optional
            },
            request_only=True,
        )
    ]
)
class PlayerCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for adding a new player to a team.
    """
    class Meta:
        model = Player
        fields = [
            'team', 'user', 'first_name', 'last_name', 
            'jersey_number', 'position', 'date_of_birth', 
            'photo', 'is_active', 'joined_date', 'notes'
        ]
    
    def validate(self, attrs):
        # Check if jersey number is unique within the team
        team = attrs.get('team')
        jersey_number = attrs.get('jersey_number')
        
        if Player.objects.filter(team=team, jersey_number=jersey_number).exists():
            raise serializers.ValidationError({
                'jersey_number': _('This jersey number is already in use by another player in this team.')
            })
        
        # Ensure the current user is the team captain or an admin
        request_user = self.context['request'].user
        if request_user.role != 'admin' and team.captain.id != request_user.id:
            raise serializers.ValidationError({
                'team': _('Only the team captain or administrators can add players to this team.')
            })
        
        return attrs

class PlayerUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating an existing player.
    """
    class Meta:
        model = Player
        fields = [
            'first_name', 'last_name', 'jersey_number', 
            'position', 'date_of_birth', 'photo',
            'is_active', 'notes'
        ]
    
    def validate(self, attrs):
        # Check if jersey number is unique within the team if changed
        if 'jersey_number' in attrs and attrs['jersey_number'] != self.instance.jersey_number:
            team = self.instance.team
            jersey_number = attrs['jersey_number']
            
            if Player.objects.filter(team=team, jersey_number=jersey_number).exists():
                raise serializers.ValidationError({
                    'jersey_number': _('This jersey number is already in use by another player in this team.')
                })
        
        # Ensure the current user is the team captain or an admin
        request_user = self.context['request'].user
        if request_user.role != 'admin' and self.instance.team.captain.id != request_user.id:
            raise serializers.ValidationError({
                'detail': _('Only the team captain or administrators can update this player.')
            })
        
        return attrs