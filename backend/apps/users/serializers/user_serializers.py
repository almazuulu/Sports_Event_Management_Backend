from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from ..models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'role']
        read_only_fields = ['id']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'username']


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'User Profile Example',
            value={
                'id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                'email': 'user@example.com',
                'username': 'john_doe',
                'first_name': 'John',
                'last_name': 'Doe',
                'role': 'team_manager'
            },
            response_only=True,
        ),
        OpenApiExample(
            'Full Profile Update Request',
            value={
                'email': 'updated@example.com',
                'username': 'updated_user',
                'first_name': 'Updated',
                'last_name': 'User'
            },
            request_only=True,
        ),
        OpenApiExample(
            'Partial Profile Update Request',
            value={
                'first_name': 'New',
                'last_name': 'Name'
            },
            request_only=True,
        )
    ]
)
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'role']
        read_only_fields = ['id', 'role']  # Role cannot be changed through the profile

    def validate_email(self, value):
        # Check for unique email
        users = User.objects.exclude(pk=self.instance.pk)
        if users.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        # Check for unique username
        users = User.objects.exclude(pk=self.instance.pk)
        if users.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'User Creation Request',
            value={
                'username': 'new_user',
                'email': 'new@example.com',
                'password': 'SecureP@ssw0rd',
                'password_confirm': 'SecureP@ssw0rd',
                'first_name': 'New',
                'last_name': 'User',
                'role': 'team_manager'  # Updated role example
            },
            request_only=True,
        ),
        OpenApiExample(
            'User Creation Response',
            value={
                'id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                'username': 'new_user',
                'email': 'new@example.com',
                'first_name': 'New',
                'last_name': 'User',
                'role': 'team_manager'
            },
            response_only=True,
        )
    ]
)
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    # Define role as a choice field explicitly
    role = serializers.ChoiceField(
        choices=User.ROLE_CHOICES,
        default='public',
        help_text='User role determines permissions in the system. Available options: admin, team_manager, player, scorekeeper, public'
    )
   
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'role']
        read_only_fields = ['id']
   
    def validate_password(self, value):
        # Use Django's built-in password validators
        validate_password(value)
        return value
   
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({"error": "Password fields didn't match."})
        return attrs
   
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data.get('role', 'public')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Roles Response',
            value=[
                {
                    "id": "admin",
                    "name": "Administrator",
                    "description": "Full system access with all permissions"
                },
                {
                    "id": "team_manager",
                    "name": "Team Manager",
                    "description": "Manager responsible for team operations and management"
                },
                {
                    "id": "player",
                    "name": "Player",
                    "description": "Player registered in a team"
                },
                {
                    "id": "scorekeeper",
                    "name": "Scorekeeper",
                    "description": "User responsible for recording scores and match results"
                },
                {
                    "id": "public",
                    "name": "Public User",
                    "description": "Regular user with basic access to the system"
                }
            ]
        )
    ]
)
class RoleSerializer(serializers.Serializer):
    """
    Serializer for user roles.
    This serializer provides information about available roles in the system.
    """
    id = serializers.CharField(
        help_text="Role identifier used in API requests",
        read_only=True
    )
    name = serializers.CharField(
        help_text="Human-readable name of the role",
        read_only=True
    )
    description = serializers.CharField(
        help_text="Description of the role's purpose",
        read_only=True
    )