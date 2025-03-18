from django.db.models import Q, Count, Prefetch
from rest_framework import viewsets, filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from django.conf import settings
from datetime import datetime, timedelta
import pytz

from users.models import User
from users.permissions import IsAdminUser
from ..models import Game
from ..serializers import (
    GameSerializer,
    GameCreateSerializer,
    GameUpdateSerializer,
    GameStatusUpdateSerializer,
    GameDetailSerializer,
    GameListSerializer,
    UpcomingGamesSerializer,
)
from ..permissions import CanViewGame, CanManageGame, CanUpdateGameStatus


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all().order_by("-start_datetime")
    authentication_classes = [JWTAuthentication]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["sport_event", "status", "game_teams__team"]
    search_fields = ["name", "description", "location"]
    ordering_fields = ["start_datetime", "name"]


    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]

        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [CanManageGame()]
        elif self.action == "update_status":
            return [CanUpdateGameStatus()]
        else:
            return [CanViewGame()]
        
    def get_queryset(self):
        """
        Filter games based on user role:
        - Admin sees all games
        - Team Manager sees games with their team
        - Player sees games they participate in
        - Scorekeeper sees games they're assigned to
        - Public sees all games (as before)
        """
        queryset = super().get_queryset()
        user = self.request.user
        
        if not user.is_authenticated:
            return queryset  # Public user sees all
            
        if user.role == 'admin':
            return queryset  # Admin sees all
            
        if user.role == 'team_manager':
            # Team manager sees games with their team
            return queryset.filter(game_teams__team__manager=user).distinct()
            
        if user.role == 'player':
            # Player sees games they participate in
            player_profiles = user.player_profiles.all()
            if player_profiles.exists():
                # Get player's teams
                team_ids = player_profiles.values_list('team_id', flat=True)
                return queryset.filter(game_teams__team_id__in=team_ids).distinct()
            return queryset.none()
            
        if user.role == 'scorekeeper':
            # Scorekeeper sees games they're assigned to
            return queryset.filter(scorekeeper=user)
            
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return GameListSerializer
        elif self.action == "create":
            return GameCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return GameUpdateSerializer
        elif self.action == "update_status":
            return GameStatusUpdateSerializer
        elif self.action == "retrieve":
            return GameDetailSerializer
        elif self.action == "upcoming_games":
            return UpcomingGamesSerializer
        return GameSerializer

    @extend_schema(
        summary="List all games",
        description="Get a list of all games that the user has permission to view",
        parameters=[
            OpenApiParameter(
                name="sport_event",
                description="Filter by sport event ID",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="status",
                description="Filter by game status",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="search",
                description="Search in name, description, and location",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="ordering",
                description="Order by field (e.g. start_datetime, -start_datetime)",
                required=False,
                type=str,
            ),
        ],
        responses={200: GameListSerializer(many=True)},
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
            400: OpenApiResponse(description="Bad request - invalid data"),
        },
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
            404: OpenApiResponse(
                description="Not found - game does not exist or user doesn't have permission"
            ),
        },
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
            404: OpenApiResponse(
                description="Not found - game does not exist or user doesn't have permission"
            ),
        },
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
            404: OpenApiResponse(
                description="Not found - game does not exist or user doesn't have permission"
            ),
        },
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
            404: OpenApiResponse(
                description="Not found - game does not exist or user doesn't have permission"
            ),
        },
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
        summary="Upcoming games for current week",
        description="Get a list of upcoming games for the current week for dashboard or homepage",
    )
    @action(detail=False, methods=["get"], url_path="upcoming")
    def upcoming_games(self, request):
        """
        Get a list of upcoming games for the current week.
        - Admin and public (unauthenticated) users see all upcoming games
        - Team managers see only games with their teams
        - Players see only games with teams they belong to
        - Scorekeepers see only games they're assigned to
        """
        from datetime import datetime, timedelta
        import pytz
        
        today = datetime.now(pytz.timezone(settings.TIME_ZONE))
        
        # Calculate start of week (Monday)
        start_of_week = today - timedelta(days=today.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Calculate end of week (Sunday)
        end_of_week = start_of_week + timedelta(days=6)
        end_of_week = end_of_week.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # Base queryset - filter by status and current week
        queryset = Game.objects.filter(
            status__in=["scheduled", "ongoing"],
            start_datetime__gte=start_of_week,
            start_datetime__lte=end_of_week
        )
        
        # Apply role-based filtering
        user = request.user
        
        if user.is_authenticated:
            if user.role == 'team_manager':
                # Team manager sees games with their teams
                queryset = queryset.filter(game_teams__team__manager=user).distinct()
            elif user.role == 'player':
                # Player sees games they participate in
                player_profiles = user.player_profiles.all()
                if player_profiles.exists():
                    team_ids = player_profiles.values_list('team_id', flat=True)
                    queryset = queryset.filter(game_teams__team_id__in=team_ids).distinct()
                else:
                    queryset = queryset.none()  # No teams = no games
            elif user.role == 'scorekeeper':
                # Scorekeeper sees games they're assigned to
                queryset = queryset.filter(scorekeeper=user)
            # Admin sees all (no additional filtering)
        
        # Apply additional filters from query params
        sport_event = request.query_params.get("sport_event")
        if sport_event:
            queryset = queryset.filter(sport_event_id=sport_event)

        team = request.query_params.get("team")
        if team:
            queryset = queryset.filter(game_teams__team=team)
        
        # Paginate and return results
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
            403: OpenApiResponse(
                description="Forbidden - user does not have permission"
            ),
        },
    )
    @action(
        detail=True,
        methods=["patch"],
        url_path="update-status",
        permission_classes=[CanUpdateGameStatus],
    )
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


@extend_schema(
    summary="List available scorekeepers",
    description="Returns a list of users with the 'scorekeeper' role, checking for time conflicts with existing games.",
    parameters=[
        OpenApiParameter(
            name="game_date",
            description="Date to check availability (YYYY-MM-DD)",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="start_time",
            description="Start time of the game (HH:MM)",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="end_time",
            description="End time of the game (HH:MM)",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="search",
            description="Search by name or email",
            required=False,
            type=str,
        ),
    ],
    responses={
        200: OpenApiResponse(
            description="List of scorekeepers with their details and availability status"
        ),
        400: OpenApiResponse(description="Bad request - invalid date or time format"),
        401: OpenApiResponse(
            description="Authentication credentials were not provided"
        ),
        403: OpenApiResponse(description="Permission denied - admin access required"),
    },
)
@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def scorekeepers_list(request):
    """
    Get a list of available scorekeepers.

    Returns a list of all users with the 'scorekeeper' role.
    When date and time parameters are provided, checks if scorekeepers
    are available during that specific time slot.

    Query Parameters:
    - game_date: Date to check availability (YYYY-MM-DD)
    - start_time: Start time of the game (HH:MM)
    - end_time: End time of the game (HH:MM)
    - search: Filter scorekeepers by name or email

    Accessible only by administrators.
    """
    # Get query parameters
    game_date = request.query_params.get("game_date", None)
    start_time = request.query_params.get("start_time", None)
    end_time = request.query_params.get("end_time", None)
    search_query = request.query_params.get("search", "")

    # Validate and parse date/time parameters if provided
    has_time_params = all([game_date, start_time, end_time])

    if has_time_params:
        try:
            import pytz

            # Parse the date and times
            date_obj = datetime.strptime(game_date, "%Y-%m-%d").date()
            start_time_obj = datetime.strptime(start_time, "%H:%M").time()
            end_time_obj = datetime.strptime(end_time, "%H:%M").time()

            # Create datetime objects for the proposed game
            start_datetime = datetime.combine(date_obj, start_time_obj)
            end_datetime = datetime.combine(date_obj, end_time_obj)

            # Add timezone info if your project uses timezone-aware datetimes
            if settings.USE_TZ:
                tz = pytz.timezone(settings.TIME_ZONE)
                start_datetime = tz.localize(start_datetime)
                end_datetime = tz.localize(end_datetime)

        except ValueError:
            return Response(
                {
                    "error": "Invalid date or time format. Use YYYY-MM-DD for date and HH:MM for times."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    # Base query for scorekeepers
    scorekeepers_query = User.objects.filter(role="scorekeeper")

    # Apply search if provided
    if search_query:
        scorekeepers_query = scorekeepers_query.filter(
            Q(first_name__icontains=search_query)
            | Q(last_name__icontains=search_query)
            | Q(email__icontains=search_query)
            | Q(username__icontains=search_query)
        )

    # Prefetch related assigned games for efficiency
    scorekeepers = scorekeepers_query.prefetch_related(
        Prefetch(
            "assigned_games",
            queryset=Game.objects.filter(status__in=["scheduled", "ongoing"]),
        )
    )

    # Build response data
    result = []
    for scorekeeper in scorekeepers:
        # Get current assignments
        current_assignments = []
        is_available = True
        conflicts = []

        for game in scorekeeper.assigned_games.all():
            if game.status in ["scheduled", "ongoing"]:
                # Format for display
                assignment = {
                    "game_id": game.id,
                    "game_name": game.name,
                    "sport_event": game.sport_event.name,
                    "start_datetime": game.start_datetime,
                    "end_datetime": game.end_datetime,
                    "status": game.get_status_display(),
                }
                current_assignments.append(assignment)

                # Check for time conflicts if we have proposed game time parameters
                if has_time_params:
                    # Game times would overlap if:
                    # (new_start < existing_end) AND (new_end > existing_start)
                    if (
                        start_datetime < game.end_datetime
                        and end_datetime > game.start_datetime
                    ):
                        is_available = False
                        conflicts.append(assignment)

        # Create scorekeeper data object
        scorekeeper_data = {
            "id": scorekeeper.id,
            "username": scorekeeper.username,
            "email": scorekeeper.email,
            "first_name": scorekeeper.first_name,
            "last_name": scorekeeper.last_name,
            "full_name": scorekeeper.get_full_name(),
            "available": is_available,
            "current_assignments": current_assignments,
        }

        # Add conflict info if time parameters were provided
        if has_time_params:
            scorekeeper_data["has_time_conflicts"] = not is_available
            if not is_available:
                scorekeeper_data["conflicts"] = conflicts

        result.append(scorekeeper_data)

    # Sort result with available scorekeepers first
    result = sorted(result, key=lambda x: (not x["available"], x["full_name"]))

    return Response(result)
