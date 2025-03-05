from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from teams.views import TeamsViewSet, PlayersViewSet,TeamRegistrationViewSet, PublicTeamListView, PublicTeamDetailView, TeamPlayerViewSet, TeamPlayerCreateViewSet, SportEventRegistrationViewSet, SportEventRegistrationCreateViewSet

# Create a router for teams
router = DefaultRouter()
router.register(r'', TeamsViewSet, basename='teams')

# Create a nested router for team players
team_players_router = NestedSimpleRouter(router, r'', lookup='team')
team_players_router.register(r'players', TeamPlayerViewSet, basename='team-players')
team_players_router.register(r'add-players', TeamPlayerCreateViewSet, basename='team-add-players')

# Main level routers
players_router = DefaultRouter()
players_router.register(r'', PlayersViewSet, basename='players')

registrations_router = DefaultRouter()
registrations_router.register(r'', TeamRegistrationViewSet, basename='registrations')

# Public endpoints
public_urls = [
    path('public/', PublicTeamListView.as_view(), name='public-teams-list'),
    path('public/<uuid:pk>/', PublicTeamDetailView.as_view(), name='public-team-detail'),
]

urlpatterns = [
    # Teams endpoints
    path('', include(router.urls)),
    path('', include(team_players_router.urls)),
    
    # Players endpoints
    path('players/', include(players_router.urls)),
    
    # Registration endpoints
    path('registrations/', include(registrations_router.urls)),
    
    # Public endpoints
    path('', include(public_urls)),
]