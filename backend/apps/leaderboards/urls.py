from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeaderboardViewSet, LeaderboardEntryViewSet

router = DefaultRouter()
router.register(r'', LeaderboardViewSet, basename='leaderboard')
router.register(r'entries', LeaderboardEntryViewSet, basename='leaderboard-entry')

app_name = 'leaderboards'

urlpatterns = [
    # Main router URLs
    path('', include(router.urls)),
]