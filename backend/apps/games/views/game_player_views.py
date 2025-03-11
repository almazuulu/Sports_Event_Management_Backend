from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

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
    """
    queryset = GamePlayer.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [CanManageGamePlayers]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['game_team', 'player', 'is_captain_for_game']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        
        return [CanManageGamePlayers()]
    
    def get_serializer_class(self):
        if self.action == 'create' and isinstance(self.request.data, list):
            return GamePlayerBulkCreateSerializer
        elif self.action in ['create']:
            return GamePlayerCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return GamePlayerUpdateSerializer
        return GamePlayerSerializer

    @extend_schema(
        summary="List all game players",
        description="Get a list of all game players with filtering options",
        parameters=[
            OpenApiParameter(name="game_team", description="Filter by game team ID", required=False, type=int),
            OpenApiParameter(name="player", description="Filter by player ID", required=False, type=int),
            OpenApiParameter(name="is_captain_for_game", description="Filter by captain status", required=False, type=bool)
        ],
        responses={200: GamePlayerSerializer(many=True)}
    )
    @method_decorator(cache_page(60*15))
    def list(self, request):
        """
        List all game players.
        Supports filtering by game_team, player, and captain status.
        Users need game player management permissions to access this endpoint.
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create a new game player",
        description="Add a player to a game team",
        request=GamePlayerCreateSerializer,
        responses={
            201: GamePlayerSerializer,
            400: OpenApiResponse(description="Bad request - invalid data")
        }
    )
    def create(self, request):
        """
        Create a new game player association.
        Adds a player to a specific game team.
        Handles both single player addition and bulk creation based on request data.
        Users need game player management permissions to create associations.
        """
        # Handle both single and bulk creation
        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @extend_schema(
        summary="Retrieve game player details",
        description="Get detailed information about a specific game player",
        responses={
            200: GamePlayerSerializer,
            404: OpenApiResponse(description="Not found - game player does not exist")
        }
    )
    def retrieve(self, request, pk=None):
        """
        Retrieve detailed information about a specific game player.
        Users need game player management permissions to access this endpoint.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema(
        summary="Update game player",
        description="Update all details of a game player (full update)",
        request=GamePlayerUpdateSerializer,
        responses={
            200: GamePlayerSerializer,
            400: OpenApiResponse(description="Bad request - invalid data"),
            404: OpenApiResponse(description="Not found - game player does not exist")
        }
    )
    def update(self, request, pk=None):
        """
        Update all details of an existing game player (full update).
        Can modify player status, position, etc.
        Users need game player management permissions to update associations.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @extend_schema(
        summary="Partially update game player",
        description="Update specific fields of a game player",
        request=GamePlayerUpdateSerializer,
        responses={
            200: GamePlayerSerializer,
            400: OpenApiResponse(description="Bad request - invalid data"),
            404: OpenApiResponse(description="Not found - game player does not exist")
        }
    )
    def partial_update(self, request, pk=None):
        """
        Update specific fields of an existing game player (partial update).
        Can modify individual properties like captain status without providing all fields.
        Users need game player management permissions to update associations.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @extend_schema(
        summary="Delete game player",
        description="Remove a player from a game team",
        responses={
            204: OpenApiResponse(description="No content - game player successfully deleted"),
            404: OpenApiResponse(description="Not found - game player does not exist")
        }
    )
    def destroy(self, request, pk=None):
        """
        Delete a game player association from the system.
        Removes a player from a game team.
        Users need game player management permissions to delete associations.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        summary="Bulk create players for a game team",
        description="Add multiple players to a game team in a single request",
        request=GamePlayerCreateSerializer(many=True),
        responses={
            201: GamePlayerSerializer(many=True),
            400: OpenApiResponse(description="Bad request - invalid data")
        }
    )
    @action(detail=False, methods=['post'], url_path='bulk-create')
    def bulk_create(self, request):
        """
        Bulk create multiple game player associations.
        Efficiently add multiple players to a game team in a single API call.
        Useful for team roster management.
        Users need game player management permissions to create associations.
        """
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)