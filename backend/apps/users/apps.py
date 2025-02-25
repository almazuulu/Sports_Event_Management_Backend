from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    
    def ready(self):
        import users.signals
        
    # Configure drf-spectacular enum choices
        try:
            from drf_spectacular.settings import spectacular_settings
            from users.models import User
            
            # Update enum overrides
            if hasattr(spectacular_settings, 'ENUM_NAME_OVERRIDES'):
                spectacular_settings.ENUM_NAME_OVERRIDES['UserRoleEnum'] = User.ROLE_CHOICES
        except (ImportError, AttributeError):
            # Handle gracefully if spectacular or model isn't available
            pass
