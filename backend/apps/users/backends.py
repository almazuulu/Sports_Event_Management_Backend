from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import User

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Authentication backend that allows users to log in with either email or username.
    This backend is used both by the Django admin interface and by the REST API.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('email', '')
            
        if username == '':
            return None
            
        try:
            # Try to find user by either username or email
            user = User.objects.get(
                Q(username=username) | Q(email=username)
            )
            
            # Verify password
            if user.check_password(password):
                return user
                
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user.
            User().set_password(password)
            return None