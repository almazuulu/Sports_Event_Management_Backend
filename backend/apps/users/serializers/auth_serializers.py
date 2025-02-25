from django.db.models import Q
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from ..models.user import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer to support login with either username or email
    """
    login = serializers.CharField(write_only=True)
    def init(self, args, **kwargs):
        super().init(args, **kwargs)
        # Remove default username field
        self.fields.pop('username', None)
        # Add custom login field
        self.fields['login'] = serializers.CharField(required=True)
    def validate(self, attrs):
        # Get login credentials
        login = attrs.pop('login')
       
        # Try to find user by email or username
        try:
            user = User.objects.get(
                Q(email=login) | Q(username=login)
            )
            # Set username for SimpleJWT validation
            attrs['username'] = user.username
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "login": "Invalid login credentials"
            })
       
        return super().validate(attrs)
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to use the custom token obtain pair serializer
    """
    serializer_class = CustomTokenObtainPairSerializer
   
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    new_password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    new_password_confirm = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
   
    def validate(self, attrs):
        if attrs.get('new_password') != attrs.get('new_password_confirm'):
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs