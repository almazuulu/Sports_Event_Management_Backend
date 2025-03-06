from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from teams.views import (
    TeamsViewSet, PlayersViewSet, 
    TeamRegistrationViewSet,
    SportEventRegistrationViewSet
)

# Main routers
teams_router = DefaultRouter()
teams_router.register(r'teams', TeamsViewSet, basename='teams')

players_router = DefaultRouter()
players_router.register(r'players', PlayersViewSet, basename='players')

registrations_router = DefaultRouter()
registrations_router.register(r'registrations', TeamRegistrationViewSet, basename='registrations')

# Nested routers
team_players_router = NestedSimpleRouter(teams_router, r'teams', lookup='team')

sport_event_registration_router = DefaultRouter()
sport_event_registration_router.register(
    r'events/(?P<sport_event_id>[^/.]+)/registrations',
    SportEventRegistrationViewSet,
    basename='sport-event-registrations'
)

sport_event_registration_create_router = DefaultRouter()


urlpatterns = [
    # Main routes
    path('', include(teams_router.urls)),
    path('', include(team_players_router.urls)),
    path('', include(players_router.urls)),
    path('', include(registrations_router.urls)),
    
    # Routes for sport event registrations
    path('', include(sport_event_registration_router.urls)),
    path('', include(sport_event_registration_create_router.urls)),
]