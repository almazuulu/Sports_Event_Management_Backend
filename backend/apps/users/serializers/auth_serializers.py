from django.db.models import Q
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from ..models.user import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer to support login with either username or email.
    Uses security-enhanced error messages that don't reveal specific details.
    """
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(style={'input_type': 'password'})
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make username optional
        self.fields['username'].required = False
        # Add email field
        self.fields['email'] = serializers.EmailField(required=False)
    
    def validate(self, attrs):
        # Extract credentials from attrs
        email = attrs.get('email')
        username = attrs.get('username')
        password = attrs.get('password')
        
        # Generic error message for security
        GENERIC_ERROR_MESSAGE = "Username, email, or password is incorrect."
        
        # We need at least one identifier field
        if not any([email, username]):
            raise serializers.ValidationError({
                "error": "Please provide either email or username."
            })
        
        # Determine which identifier was provided
        identifier = email if email else username
        
        # Try to find user by email or username
        try:
            user = User.objects.get(
                Q(email=identifier) | Q(username=identifier)
            )
                
            # Check the password but use a generic error message
            if not user.check_password(password):
                raise serializers.ValidationError({
                    "error": GENERIC_ERROR_MESSAGE
                })
                
            # User exists and password is correct
            # Make sure the USERNAME_FIELD is properly set for SimpleJWT
            if self.username_field not in attrs:
                attrs[self.username_field] = user.email  # Use the user's actual email
                
        except User.DoesNotExist:
            # Use the same generic error for non-existent users
            raise serializers.ValidationError({
                "error": GENERIC_ERROR_MESSAGE
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