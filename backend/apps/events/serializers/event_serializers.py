from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from events.models import Event, SportEvent
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Simple User serializer for nested representation
    """
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name']
        read_only_fields = fields
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class SportEventListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for SportEvent model used in nested representation
    """
    sport_type_display = serializers.CharField(source='get_sport_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = SportEvent
        fields = [
            'id', 'name', 'sport_type', 'sport_type_display', 
            'start_date', 'end_date', 'status', 'status_display'
        ]
        read_only_fields = fields


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for Event model (used for list and retrieve)
    """
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    sport_events_count = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    sport_events = SportEventListSerializer(many=True, read_only=True)
    
    class Meta:
        model = Event
        fields = [
            'id', 'name', 'description', 'start_date', 'end_date', 
            'location', 'status', 'status_display', 'created_by', 'created_at', 
            'updated_by', 'updated_at', 'sport_events_count', 'sport_events'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_by', 'updated_at']
    
    def get_sport_events_count(self, obj):
        return obj.sport_events.count()


class EventCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating Events. 
    Only administrators can create or modify events.
    """
    class Meta:
        model = Event
        fields = [
            'name', 'description', 'start_date', 'end_date', 
            'location', 'status'
        ]
    
    def validate(self, data):
        """
        Validate that end_date is after start_date
        """
        if 'start_date' in data and 'end_date' in data:
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError(
                    {"end_date": "End date must be after start date."}
                )
        return data
    
    def validate_user_is_admin(self, user):
        """
        Validate that the user has admin role
        """
        if user.role != 'admin':
            raise PermissionDenied("Only administrators can create or modify events.")
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


class EventPublicSerializer(serializers.ModelSerializer):
    """
    Serializer for public (unauthenticated) access to events.
    Returns limited information.
    """
    sport_events_count = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Event
        fields = [
            'id', 'name', 'start_date', 'end_date', 
            'location', 'status', 'status_display', 'sport_events_count'
        ]
        read_only_fields = fields
    
    def get_sport_events_count(self, obj):
        return obj.sport_events.count()


