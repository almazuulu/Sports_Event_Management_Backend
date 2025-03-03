from django.urls import path, include
from rest_framework.routers import DefaultRouter
from teams.views import TeamsViewSet, PlayersViewSet,TeamRegistrationViewSet, PublicTeamListView, PublicTeamDetailView, TeamPlayerViewSet, TeamPlayerCreateViewSet, SportEventRegistrationViewSet, SportEventRegistrationCreateViewSet
from . import views

app_name = 'teams'

router = DefaultRouter()
router.register(r'teams', TeamsViewSet, basename='team')
router.register(r'players', PlayersViewSet, basename='player')
router.register(r'registrations', TeamRegistrationViewSet, basename='registration')
router.register(r'teams/(?P<team_id>[^/.]+)/players', TeamPlayerViewSet, basename='team-players')
router.register(r'teams/(?P<team_id>[^/.]+)/registrations', TeamRegistrationViewSet, basename='team-registrations')
router.register(r'teams/(?P<team_id>[^/.]+)/add-player', TeamPlayerCreateViewSet, basename='add-team-player')

# Add new endpoints for sport event registration
router.register(r'sport-events/(?P<sport_event_id>[^/.]+)/registrations', SportEventRegistrationViewSet, basename='sport-event-registrations')
router.register(r'sport-events/(?P<sport_event_id>[^/.]+)/register', SportEventRegistrationCreateViewSet, basename='sport-event-register')


urlpatterns = [
    path('', include(router.urls)),
    path('public/teams/', PublicTeamListView.as_view(), name='public-team-list'),
    path('public/teams/<uuid:id>/', PublicTeamDetailView.as_view(), name='public-team-detail'),
    path('my-teams/', TeamsViewSet.as_view({'get': 'list'}), name='my-teams')
]
