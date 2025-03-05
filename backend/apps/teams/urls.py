from django.urls import path, include
from rest_framework.routers import DefaultRouter
from teams.views import TeamsViewSet, PlayersViewSet,TeamRegistrationViewSet, PublicTeamListView, PublicTeamDetailView, TeamPlayerViewSet, TeamPlayerCreateViewSet, SportEventRegistrationViewSet, SportEventRegistrationCreateViewSet, AdminTeamRegistrationListView
from . import views

app_name = 'teams'

router = DefaultRouter()
router.register(r'teams', TeamsViewSet, basename='team')
router.register(r'players', PlayersViewSet, basename='player')
router.register(r'registrations', TeamRegistrationViewSet, basename='registration')

urlpatterns = [
    path('', include(router.urls)),
    path('public/teams/', PublicTeamListView.as_view(), name='public-team-list'),
    path('public/teams/<uuid:id>/', PublicTeamDetailView.as_view(), name='public-team-detail'),
    path('admin/registrations/', AdminTeamRegistrationListView.as_view(), name='admin-team-registrations')
]
