from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    # Will contain team-related endpoints like:
    # path('', views.TeamListView.as_view(), name='team-list'),
    # path('<int:pk>/', views.TeamDetailView.as_view(), name='team-detail'),
    # path('<int:team_id>/players/', views.PlayerListView.as_view(), name='player-list'),
]