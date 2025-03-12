from django.urls import path, include
from rest_framework.routers import DefaultRouter

from games.views import GameViewSet, GameTeamViewSet, GamePlayerViewSet, scorekeepers_list

router = DefaultRouter()
router.register(r'games', GameViewSet, basename='game')
router.register(r'game-teams', GameTeamViewSet, basename='game-team')
router.register(r'game-players', GamePlayerViewSet, basename='game-player')

urlpatterns = [
    path('', include(router.urls)),
    
    # Custom bulk create endpoint for game players
    path('game-players/bulk-create/', 
         GamePlayerViewSet.as_view({'post': 'bulk_create'}), 
         name='game-player-bulk-create'),
    
    path('scorekeepers/', scorekeepers_list, name='scorekeepers-list'),
]