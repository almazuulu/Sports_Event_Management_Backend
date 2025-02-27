from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from events.models import SportEvent
from .event_serializers import UserSerializer


class SportEventSerializer(serializers.ModelSerializer):
    """
    Serializer for SportEvent model (used for list and retrieve)
    """
    event_name = serializers.CharField(source='event.name', read_only=True)
    sport_type_display = serializers.CharField(source='get_sport_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    
    class Meta:
        model = SportEvent
        fields = [
            'id', 'event', 'event_name', 'sport_type', 'sport_type_display',
            'name', 'description', 'start_date', 'end_date', 'max_teams',
            'registration_deadline', 'rules', 'scoring_system', 'status',
            'status_display', 'created_by', 'created_at', 'updated_by', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_by', 'updated_at']


class SportEventCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating SportEvents.
    Only administrators can create or modify sport events.
    """
    class Meta:
        model = SportEvent
        fields = [
            'event', 'sport_type', 'name', 'description', 'start_date', 
            'end_date', 'max_teams', 'registration_deadline', 'rules', 
            'scoring_system', 'status'
        ]
    
    def validate(self, data):
        """
        Perform validation:
        1. Ensure end_date is after start_date
        2. Ensure dates are within parent event dates
        3. Ensure registration_deadline is before start_date
        """
        if 'start_date' in data and 'end_date' in data:
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError(
                    {"end_date": "End date must be after start date."}
                )
        
        event = data.get('event')
        if not event and self.instance:
            event = self.instance.event
            
        if event:
            start_date = data.get('start_date', self.instance.start_date if self.instance else None)
            end_date = data.get('end_date', self.instance.end_date if self.instance else None)
            
            if start_date and start_date < event.start_date:
                raise serializers.ValidationError(
                    {"start_date": "Sport event cannot start before the main event."}
                )
            
            if end_date and end_date > event.end_date:
                raise serializers.ValidationError(
                    {"end_date": "Sport event cannot end after the main event."}
                )
        
        registration_deadline = data.get('registration_deadline')
        start_date = data.get('start_date')
        
        if registration_deadline and start_date and registration_deadline > start_date:
            raise serializers.ValidationError(
                {"registration_deadline": "Registration deadline must be before the start date."}
            )
            
        return data
    
    def validate_user_is_admin(self, user):
        """
        Validate that the user has admin role
        """
        if user.role != 'admin':
            raise PermissionDenied("Only administrators can create or modify sport events.")
        return True
    
    def create(self, validated_data):
        """
        Set the created_by field to the current user and ensure they are an admin
        """
        user = self.context['request'].user
        self.validate_user_is_admin(user)
        
        validated_data['created_by'] = user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """
        Set the updated_by field to the current user and ensure they are an admin
        """
        user = self.context['request'].user
        self.validate_user_is_admin(user)
        
        validated_data['updated_by'] = user
        return super().update(instance, validated_data)


class SportEventPublicSerializer(serializers.ModelSerializer):
    """
    Serializer for public (unauthenticated) access to sport events.
    Returns limited information.
    """
    event_name = serializers.CharField(source='event.name', read_only=True)
    sport_type_display = serializers.CharField(source='get_sport_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = SportEvent
        fields = [
            'id', 'event', 'event_name', 'sport_type', 'sport_type_display',
            'name', 'start_date', 'end_date', 'status', 'status_display'
        ]
        read_only_fields = fields