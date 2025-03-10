from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

from ..models import GameTeam
from ..serializers import (
    GameTeamSerializer,
    GameTeamCreateSerializer,
    GameTeamUpdateSerializer,
    GameTeamDetailSerializer
)
from ..permissions import CanManageGameTeams


class GameTeamViewSet(viewsets.ModelViewSet):
    queryset = GameTeam.objects.all()
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['game', 'team', 'designation']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        
        return [CanManageGameTeams()]

    def get_serializer_class(self):
        if self.action in ['create']:
            return GameTeamCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return GameTeamUpdateSerializer
        elif self.action in ['retrieve']:
            return GameTeamDetailSerializer
        return GameTeamSerializer

    @extend_schema(
        summary="List all game teams",
        description="Get a list of all game teams with filtering options",
        parameters=[
            OpenApiParameter(name="game", description="Filter by game ID", required=False, type=int),
            OpenApiParameter(name="team", description="Filter by team ID", required=False, type=int),
            OpenApiParameter(name="designation", description="Filter by team designation (home/away)", required=False, type=str)
        ],
        responses={200: GameTeamSerializer(many=True)}
    )
    @method_decorator(cache_page(60*15))
    def list(self, request):
        """
        List all game teams.
        Supports filtering by game, team, and designation.
        Users need game team management permissions to access this endpoint.
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create a new game team",
        description="Associate a team with a game, defining its role (home/away)",
        request=GameTeamCreateSerializer,
        responses={
            201: GameTeamSerializer,
            400: OpenApiResponse(description="Bad request - invalid data")
        }
    )
    def create(self, request):
        """
        Create a new game team association.
        Associates a team with a specific game and designates its role (home/away).
        Users need game team management permissions to create associations.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @extend_schema(
        summary="Retrieve game team details",
        description="Get detailed information about a specific game team association",
        responses={
            200: GameTeamDetailSerializer,
            404: OpenApiResponse(description="Not found - game team does not exist")
        }
    )
    def retrieve(self, request, pk=None):
        """
        Retrieve detailed information about a specific game team association.
        Includes related game and team details.
        Users need game team management permissions to access this endpoint.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema(
        summary="Update game team",
        description="Update all details of a game team association (full update)",
        request=GameTeamUpdateSerializer,
        responses={
            200: GameTeamSerializer,
            400: OpenApiResponse(description="Bad request - invalid data"),
            404: OpenApiResponse(description="Not found - game team does not exist")
        }
    )
    def update(self, request, pk=None):
        """
        Update all details of an existing game team association (full update).
        Can modify team designation or other properties.
        Users need game team management permissions to update associations.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @extend_schema(
        summary="Partially update game team",
        description="Update specific fields of a game team association",
        request=GameTeamUpdateSerializer,
        responses={
            200: GameTeamSerializer,
            400: OpenApiResponse(description="Bad request - invalid data"),
            404: OpenApiResponse(description="Not found - game team does not exist")
        }
    )
    def partial_update(self, request, pk=None):
        """
        Update specific fields of an existing game team association (partial update).
        Can modify individual properties like designation without providing all fields.
        Users need game team management permissions to update associations.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @extend_schema(
        summary="Delete game team",
        description="Remove a team from a game",
        responses={
            204: OpenApiResponse(description="No content - game team successfully deleted"),
            404: OpenApiResponse(description="Not found - game team does not exist")
        }
    )
    def destroy(self, request, pk=None):
        """
        Delete a game team association from the system.
        Removes the connection between a team and a game.
        Users need game team management permissions to delete associations.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)