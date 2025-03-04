from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from ..models import GamePlayer
from ..serializers import (
    GamePlayerSerializer,
    GamePlayerCreateSerializer,
    GamePlayerUpdateSerializer,
    GamePlayerBulkCreateSerializer
)
from ..permissions import CanManageGamePlayers


class GamePlayerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Game Player management.
    Provides CRUD operations with appropriate permissions.
    """
    queryset = GamePlayer.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [CanManageGamePlayers]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['game_team', 'player', 'is_captain_for_game']

    def get_serializer_class(self):
        if self.action == 'create' and isinstance(self.request.data, list):
            return GamePlayerBulkCreateSerializer
        elif self.action in ['create']:
            return GamePlayerCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return GamePlayerUpdateSerializer
        return GamePlayerSerializer

    @extend_schema(
        summary="Bulk create players for a game team",
        description="Add multiple players to a game team in a single request",
        request=GamePlayerCreateSerializer(many=True),
        responses={201: GamePlayerSerializer(many=True)}
    )
    def bulk_create(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)