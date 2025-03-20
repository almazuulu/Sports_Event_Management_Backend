from django.apps import AppConfig


class LeaderboardsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "leaderboards"
    verbose_name = "Leaderboards"
    
    def ready(self):
        """
        Import signal handlers when the app is ready.
        """
        import leaderboards.signals