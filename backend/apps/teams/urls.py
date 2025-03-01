from django.urls import path, include
from rest_framework.routers import DefaultRouter
from teams.views import TeamsViewSet, PlayersViewSet, TeamRegistrationViewSet, PublicTeamListView, PublicTeamDetailView
from . import views

app_name = 'teams'

router = DefaultRouter()
router.register(r'team', TeamsViewSet, basename='team')
router.register(r'player', PlayersViewSet, basename='player')
router.register(r'registration', TeamRegistrationViewSet, basename='registration')

urlpatterns = [
    path('', include(router.urls)),
    path('public/teams/', PublicTeamListView.as_view(), name='public-team-list'),
    path('public/teams/<uuid:id>/', PublicTeamDetailView.as_view(), name='public-team-detail'),
]
