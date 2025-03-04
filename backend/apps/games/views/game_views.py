from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

from ..models import Game
from ..serializers import (
    GameSerializer, 
    GameCreateSerializer, 
    GameUpdateSerializer, 
    GameStatusUpdateSerializer, 
    GameDetailSerializer,
    GameListSerializer,
    PublicGameListSerializer,
    PublicGameDetailSerializer,
    UpcomingGamesSerializer
)
from ..permissions import (
    CanViewGame, 
    CanManageGame, 
    CanUpdateGameStatus
)


class GameViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Game management.
    """
    queryset = Game.objects.all().order_by('-start_datetime')
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sport_event', 'status']
    search_fields = ['name', 'description', 'location']
    ordering_fields = ['start_datetime', 'name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [CanManageGame()]
        elif self.action in ['public_list', 'public_detail']:
            return [AllowAny()]
        return [CanViewGame()]

    def get_serializer_class(self):
        if self.action in ['list']:
            return GameListSerializer
        elif self.action in ['create']:
            return GameCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return GameUpdateSerializer
        elif self.action == 'update_status':
            return GameStatusUpdateSerializer
        elif self.action in ['retrieve']:
            return GameDetailSerializer
        elif self.action == 'public_list':
            return PublicGameListSerializer
        elif self.action == 'public_detail':
            return PublicGameDetailSerializer
        elif self.action == 'upcoming_games':
            return UpcomingGamesSerializer
        return GameSerializer

    @extend_schema(
        summary="List all games",
        description="Get a list of all games that the user has permission to view",
        parameters=[
            OpenApiParameter(name="sport_event", description="Filter by sport event ID", required=False, type=str),
            OpenApiParameter(name="status", description="Filter by game status", required=False, type=str),
            OpenApiParameter(name="search", description="Search in name, description, and location", required=False, type=str),
            OpenApiParameter(name="ordering", description="Order by field (e.g. start_datetime, -start_datetime)", required=False, type=str)
        ],
        responses={200: GameListSerializer(many=True)}
    )
    def list(self, request):
        """
        List all games that the user has permission to view.
        Supports filtering by sport_event and status, searching, and ordering.
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create a new game",
        description="Create a new game with all required information",
        request=GameCreateSerializer,
        responses={
            201: GameSerializer,
            400: OpenApiResponse(description="Bad request - invalid data")
        }
    )
    def create(self, request):
        """
        Create a new game.
        Only users with game management permissions can create games.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    @extend_schema(
        summary="Retrieve game details",
        description="Get detailed information about a specific game",
        responses={
            200: GameDetailSerializer,
            404: OpenApiResponse(description="Not found - game does not exist or user doesn't have permission")
        }
    )
    def retrieve(self, request, pk=None):
        """
        Retrieve detailed information about a specific game.
        User must have permission to view the game.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema(
        summary="Update game details",
        description="Update details of an existing game (full update)",
        request=GameUpdateSerializer,
        responses={
            200: GameSerializer,
            400: OpenApiResponse(description="Bad request - invalid data"),
            404: OpenApiResponse(description="Not found - game does not exist or user doesn't have permission")
        }
    )
    def update(self, request, pk=None):
        """
        Update all details of an existing game (full update).
        Only users with game management permissions can update games.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @extend_schema(
        summary="Partially update game",
        description="Update specific fields of an existing game",
        request=GameUpdateSerializer,
        responses={
            200: GameSerializer,
            400: OpenApiResponse(description="Bad request - invalid data"),
            404: OpenApiResponse(description="Not found - game does not exist or user doesn't have permission")
        }
    )
    def partial_update(self, request, pk=None):
        """
        Update specific fields of an existing game (partial update).
        Only users with game management permissions can update games.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @extend_schema(
        summary="Delete game",
        description="Remove a game from the system",
        responses={
            204: OpenApiResponse(description="No content - game successfully deleted"),
            404: OpenApiResponse(description="Not found - game does not exist or user doesn't have permission")
        }
    )
    def destroy(self, request, pk=None):
        """
        Delete a game from the system.
        Only users with game management permissions can delete games.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)

    @extend_schema(
        summary="Public games listing",
        description="Get a list of public games with limited information",
        parameters=[
            OpenApiParameter(name="sport_event", description="Filter by sport event ID", required=False, type=str),
            OpenApiParameter(name="status", description="Filter by game status", required=False, type=str)
        ],
        responses={200: PublicGameListSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='public', authentication_classes=[])
    def public_list(self, request):
        """
        List all public games with limited information.
        Open to everyone without authentication.
        Only shows scheduled and ongoing games.
        """
        queryset = Game.objects.filter(status__in=['scheduled', 'ongoing'])
        
        # Optional filtering
        sport_event = request.query_params.get('sport_event')
        if sport_event:
            queryset = queryset.filter(sport_event_id=sport_event)
        
        status_param = request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Public game details",
        description="Get public details of a specific game",
        responses={200: PublicGameDetailSerializer}
    )
    @action(detail=True, methods=['get'], url_path='public', authentication_classes=[])
    def public_detail(self, request, pk=None):
        """
        Retrieve public details of a specific game.
        Open to everyone without authentication.
        """
        game = self.get_object()
        serializer = self.get_serializer(game)
        return Response(serializer.data)

    @extend_schema(
        summary="Upcoming games",
        description="Get a list of upcoming games for dashboard or homepage",
        parameters=[
            OpenApiParameter(name="sport_event", description="Filter by sport event ID", required=False, type=str)
        ],
        responses={200: UpcomingGamesSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='upcoming')
    def upcoming_games(self, request):
        """
        Get a list of upcoming games for dashboard or homepage.
        Only shows scheduled and ongoing games.
        User must have permission to view games.
        """
        queryset = Game.objects.filter(status__in=['scheduled', 'ongoing'])
        
        sport_event = request.query_params.get('sport_event')
        if sport_event:
            queryset = queryset.filter(sport_event_id=sport_event)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Update game status",
        description="Update the status of a game by admin or assigned scorekeeper",
        request=GameStatusUpdateSerializer,
        responses={
            200: GameSerializer,
            400: OpenApiResponse(description="Bad request - invalid status transition"),
            403: OpenApiResponse(description="Forbidden - user does not have permission")
        }
    )
    @action(detail=True, methods=['patch'], url_path='update-status', permission_classes=[CanUpdateGameStatus])
    def update_status(self, request, pk=None):
        """
        Update the status of a game (e.g., from scheduled to ongoing, or from ongoing to completed).
        Only admins or assigned scorekeepers can update game status.
        """
        game = self.get_object()
        serializer = self.get_serializer(game, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # Return the updated game details
        return_serializer = GameSerializer(game)
        return Response(return_serializer.data)