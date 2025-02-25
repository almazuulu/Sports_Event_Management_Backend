from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import User

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to find user by either username or email
            user = User.objects.get(
                Q(username=username) | Q(email=username)
            )
            
            # Verify password
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None