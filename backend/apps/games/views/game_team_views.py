from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from ..models import GameTeam
from ..serializers import (
    GameTeamSerializer,
    GameTeamCreateSerializer,
    GameTeamUpdateSerializer,
    GameTeamDetailSerializer
)
from ..permissions import CanManageGameTeams


class GameTeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Game Team management.
    Provides CRUD operations with appropriate permissions.
    """
    queryset = GameTeam.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [CanManageGameTeams]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['game', 'team', 'designation']

    def get_serializer_class(self):
        if self.action in ['create']:
            return GameTeamCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return GameTeamUpdateSerializer
        elif self.action in ['retrieve']:
            return GameTeamDetailSerializer
        return GameTeamSerializer