from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import User


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to perform actions when a user is created
    
    Args:
        sender: The model class that sent the signal (User)
        instance: The actual instance being saved
        created: Boolean; True if a new record was created
    """
    if created:
        # This runs only when a new user is created, not when a user is updated
        pass
        # Example actions you could take:
        # - Create a UserProfile if you have a separate profile model
        # - Assign default permissions based on user.role
        # - Send a welcome email