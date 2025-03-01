# players/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from teams.permissions import IsPlayerTeamCaptainOrAdmin

from teams.models import Player
from teams.serializers import PlayerSerializer, PlayerCreateSerializer, PlayerUpdateSerializer


class PlayersViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing players within a team.
    Only the team captain or administrators can add or modify players.
    Authenticated users can view player details.
    """
    queryset = Player.objects.all().order_by('team__name', 'last_name')
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['team', 'is_active']
    search_fields = ['first_name', 'last_name', 'team__name']
    ordering_fields = ['first_name', 'last_name', 'team__name']

    def get_serializer_class(self):
        """
        Return different serializers based on the action.
        """
        if self.action == 'create':
            return PlayerCreateSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return PlayerUpdateSerializer
        return PlayerSerializer

    def get_permissions(self):
        """
        Assign permissions based on the action being performed.
        """
        if self.action == 'create':
            return [IsAuthenticated(), IsPlayerTeamCaptainOrAdmin()]
        elif self.action == 'update' or self.action == 'partial_update':
            return [IsAuthenticated(), IsPlayerTeamCaptainOrAdmin()]
        elif self.action == 'destroy':
            return [IsAuthenticated(), IsPlayerTeamCaptainOrAdmin()]
        return [IsAuthenticated(), IsPlayerTeamCaptainOrAdmin()]

    @extend_schema(
        summary="List all players",
        description="Returns a list of all players in the system. Requires authentication.",
        responses={200: PlayerSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """
        List players with optional filtering, searching, and ordering.
        """
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new player",
        description="Create a new player. Only the team captain or administrators can add players to a team.",
        request=PlayerCreateSerializer,
        responses={201: PlayerSerializer}
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new player for a specific team.
        Only the team captain or an admin can add players to the team.
        """
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a player",
        description="Get details of a specific player. Requires authentication.",
        responses={200: PlayerSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve the details of a specific player.
        """
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update a player",
        description="Fully update a specific player's information. Only the team captain or administrators can update a player.",
        request=PlayerUpdateSerializer,
        responses={200: PlayerSerializer}
    )
    def update(self, request, *args, **kwargs):
        """
        Fully update the details of an existing player.
        """
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a player",
        description="Delete a specific player. Only administrators can delete players.",
        responses={204: None}
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete a player from the system. Only admins can delete players.
        """
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update a player",
        description="Partially update the details of an existing player. Only the team captain or administrators can update a player.",
        request=PlayerUpdateSerializer,
        responses={200: PlayerSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a player's information (e.g., jersey number, active status).
        """
        return super().partial_update(request, *args, **kwargs)
