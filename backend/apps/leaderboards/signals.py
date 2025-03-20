from django.db.models.signals import post_save
from django.dispatch import receiver
from scores.models import Score
from .models import Leaderboard


@receiver(post_save, sender=Score)
def update_leaderboard_on_score_change(sender, instance, **kwargs):
    """
    Signal handler to update leaderboards when a score is updated.
    
    When a score is updated and verified, flag the corresponding leaderboard
    to be recalculated. This is a lightweight approach that avoids expensive
    calculations on every save, but ensures the leaderboard is marked for update.
    """
    # Only respond when score is completed and verified
    if instance.status == 'completed' and instance.verification_status == 'verified':
        # Get the sport event from the game
        sport_event = instance.game.sport_event
        
        # Get or create the leaderboard
        leaderboard, created = Leaderboard.objects.get_or_create(
            sport_event=sport_event
        )
        
        # Just update the last_updated timestamp to indicate it needs recalculation
        leaderboard.save(update_fields=['last_updated'] if not created else None)