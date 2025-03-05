from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from ..models import TeamRegistration, Team


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Team Registration Example',
            value={
                'id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                'team': '3fa85f64-5717-4562-b3fc-2c963f66afa7',
                'team_name': 'Thunderbolts',
                'sport_event': '3fa85f64-5717-4562-b3fc-2c963f66afa8',
                'sport_event_name': 'Annual Basketball Tournament 2025',
                'registration_date': '2025-01-15T12:00:00Z',
                'status': 'pending',
                'notes': 'First time participating'
            },
            response_only=True,
        )
    ]
)
class TeamRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for the TeamRegistration model with detailed information.
    """
    team_name = serializers.CharField(source='team.name', read_only=True)
    sport_event_name = serializers.CharField(source='sport_event.name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True, allow_null=True)
    
    class Meta:
        model = TeamRegistration
        fields = [
            'id', 'team', 'team_name', 'sport_event', 
            'sport_event_name', 'registration_date', 'status', 
            'notes', 'approved_by', 'approved_by_name', 'approval_date'
        ]
        read_only_fields = ['id', 'registration_date', 'approved_by', 'approval_date']

class TeamRegistrationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new team registration for a sport event.
    """
    class Meta:
        model = TeamRegistration
        fields = ['team', 'sport_event', 'notes']
    
    def validate(self, attrs):
        # Check if the team is already registered for this sport event
        team = attrs.get('team')
        sport_event = attrs.get('sport_event')
        
        if TeamRegistration.objects.filter(team=team, sport_event=sport_event).exists():
            raise serializers.ValidationError({
                'sport_event': _('This team is already registered for this sport event.')
            })
        
        # Check if registration is still open for this sport event
        if sport_event.registration_deadline and sport_event.registration_deadline < timezone.now():
            raise serializers.ValidationError({
                'sport_event': _('Registration deadline for this sport event has passed.')
            })
        
        # Ensure the current user is the team manager
        request_user = self.context['request'].user
        if team.manager.id != request_user.id:
            raise serializers.ValidationError({
                'team': _('Only the team manager can register a team for a sport event.')
            })
        
        # Check if maximum teams limit has been reached
        if sport_event.max_teams > 0:
            current_team_count = TeamRegistration.objects.filter(
                sport_event=sport_event, 
                status='approved'
            ).count()
            
            if current_team_count >= sport_event.max_teams:
                raise serializers.ValidationError({
                    'sport_event': _('This sport event has reached its maximum team capacity.')
                })
        
        return attrs

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Team Registration Approval Example',
            value={
                'status': 'approved',
                'notes': 'All requirements met'
            },
            request_only=True,
        )
    ]
)
class TeamRegistrationApprovalSerializer(serializers.ModelSerializer):
    """
    Serializer for approving or rejecting a team registration.
    Only admins can approve or reject team registrations.
    """
    class Meta:
        model = TeamRegistration
        fields = ['status', 'notes']
    
    def validate_status(self, value):
        if value not in ['approved', 'rejected']:
            raise serializers.ValidationError(_('Status must be either approved or rejected.'))
        return value
    
    def update(self, instance, validated_data):
        # Only admins can approve/reject registrations
        request_user = self.context['request'].user
        if request_user.role != 'admin':
            raise serializers.ValidationError({
                'detail': _('Only administrators can approve or reject team registrations.')
            })
        
        # Set approval information
        if validated_data.get('status') == 'approved':
            validated_data['approved_by'] = request_user
            validated_data['approval_date'] = timezone.now()
        
        instance.status = validated_data.get('status', instance.status)
        instance.notes = validated_data.get('notes', instance.notes)
        
        if validated_data.get('status') == 'approved':
            instance.approved_by = request_user
            instance.approval_date = timezone.now()
        
        instance.save()
        return instance