from django.urls import path
from . import views

app_name = 'leaderboards'

urlpatterns = [
    # Will contain leaderboard-related endpoints like:
    # path('', views.LeaderboardView.as_view(), name='overall-leaderboard'),
    # path('<int:event_id>/', views.EventLeaderboardView.as_view(), name='event-leaderboard'),
]