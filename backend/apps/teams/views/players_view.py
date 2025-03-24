from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from django.utils.translation import gettext_lazy as _

from teams.models import Player
from teams.serializers import (
    PlayerSerializer,
    PlayerCreateSerializer,
    PlayerUpdateSerializer,
    TeamCaptainSerializer
)
from teams.permissions import (
    IsPlayerTeamManagerOrAdmin,
    IsTeamOwnerOrAdmin
)


class PlayersViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing players across all teams.
    
    Team managers can manage their own team's players.
    Admins can manage all players.
    """
    queryset = Player.objects.all()  
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['team', 'is_active', 'is_captain']
    search_fields = ['first_name', 'last_name', 'position']
    ordering_fields = ['team', 'last_name', 'first_name', 'jersey_number']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PlayerCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return PlayerUpdateSerializer
        elif self.action == 'set_as_captain':
            return TeamCaptainSerializer
        return PlayerSerializer
    
    def get_queryset(self):
        """
        Filter players based on user role:
        - Admin sees all players
        - Team Manager sees players on their team
        - Player sees players on their team
        - Scorekeeper sees players in games they're assigned to
        - Public sees all players (as before)
        """
        queryset = self.queryset
        user = self.request.user
        
        if not user.is_authenticated:
            return queryset  # Public user sees all
            
        if user.role == 'admin':
            return queryset  # Admin sees all
            
        if user.role == 'team_manager':
            # Team manager sees players on their team
            return queryset.filter(team__manager=user)
            
        if user.role == 'player':
            # Player sees players on their team
            player_profiles = user.player_profiles.all()
            if player_profiles.exists():
                team_ids = player_profiles.values_list('team_id', flat=True)
                return queryset.filter(team_id__in=team_ids)
            return queryset.none()
            
        if user.role == 'scorekeeper':
            # Scorekeeper sees players in games they're assigned to
            return queryset.filter(
                game_selections__game_team__game__scorekeeper=user
            ).distinct()
            
        return queryset
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # Allow anyone to view player lists and details
            return []
        elif self.action in ['update', 'partial_update', 'destroy', 'set_as_captain']:
            permission_classes = [IsPlayerTeamManagerOrAdmin()]
        else:
            permission_classes = [IsTeamOwnerOrAdmin()]
        return permission_classes
    
    @extend_schema(
        summary="List players",
        description="Returns a list of all players across all teams. Supports filtering and searching.",
        parameters=[
            OpenApiParameter(name="team", description="Filter by team ID", required=False, type=str),
            OpenApiParameter(name="is_active", description="Filter by active status (true/false)", required=False, type=bool),
            OpenApiParameter(name="is_captain", description="Filter by captain status (true/false)", required=False, type=bool),
            OpenApiParameter(name="search", description="Search by name or position", required=False, type=str),
            OpenApiParameter(name="ordering", description="Order results by field (e.g., last_name, jersey_number)", required=False, type=str),
        ],
        responses={
            200: PlayerSerializer(many=True),
            401: OpenApiResponse(description="Authentication credentials were not provided")
        }
    )
    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of all players across all teams.
        
        Returns a paginated list of players with detailed information.
        Supports filtering by team, active status, and captain status.
        """
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve player",
        description="Get detailed information about a specific player.",
        parameters=[
            OpenApiParameter(name="id", location=OpenApiParameter.PATH, description="Player ID (UUID)", required=True, type=str),
        ],
        responses={
            200: PlayerSerializer,
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            404: OpenApiResponse(description="Player not found")
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve detailed information about a specific player.
        
        Returns complete player information including team details.
        """
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
    summary="Create player",
    description="Create a new player for any team with mandatory user association.",
    request=PlayerCreateSerializer,
    responses={
        201: PlayerSerializer,
        400: OpenApiResponse(description="Invalid input data"),
        401: OpenApiResponse(description="Authentication credentials were not provided"),
        403: OpenApiResponse(description="Permission denied - not team manager or admin"),
    }
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new player.
        
        Creates a player for a specified team with mandatory association to an existing user with role 'player'.
        The team must be included in the request data.
        The player's name and surname will be automatically taken from the user's account.
        
        Required fields:
        - team: The team ID this player belongs to
        - user: The user ID (must have role 'player')
        - jersey_number: Unique number within the team
        - date_of_birth: Player's date of birth
        - joined_date: When the player joined the team
        
        Optional fields:
        - position: Player's position
        - is_active: Whether the player is active
        - notes: Additional notes about the player
        
        Only the team manager of the specified team or administrators can create players.
        Jersey numbers must be unique within each team.
        A user can only be associated with one player per team.
        """
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Update player",
        description="Fully update a player. Only the team manager or administrators can perform this action.",
        parameters=[
            OpenApiParameter(name="id", location=OpenApiParameter.PATH, description="Player ID (UUID)", required=True, type=str),
        ],
        request=PlayerUpdateSerializer,
        responses={
            200: PlayerSerializer,
            400: OpenApiResponse(description="Invalid input data"),
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            403: OpenApiResponse(description="Permission denied - not team manager or admin"),
            404: OpenApiResponse(description="Player not found")
        }
    )
    def update(self, request, *args, **kwargs):
        """
        Completely update a player.
        
        Requires all mandatory fields. Only the team manager or administrators can update a player.
        """
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partial update player",
        description="Partially update a player. Only the team manager or administrators can perform this action.",
        parameters=[
            OpenApiParameter(name="id", location=OpenApiParameter.PATH, description="Player ID (UUID)", required=True, type=str),
        ],
        request=PlayerUpdateSerializer,
        responses={
            200: PlayerSerializer,
            400: OpenApiResponse(description="Invalid input data"),
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            403: OpenApiResponse(description="Permission denied - not team manager or admin"),
            404: OpenApiResponse(description="Player not found")
        }
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a player.
        
        Update only specified fields. Only the team manager or administrators can update a player.
        """
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete player",
        description="Remove a player from the system. Only the team manager or administrators can perform this action.",
        parameters=[
            OpenApiParameter(name="id", location=OpenApiParameter.PATH, description="Player ID (UUID)", required=True, type=str),
        ],
        responses={
            204: OpenApiResponse(description="Player successfully deleted"),
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            403: OpenApiResponse(description="Permission denied - not team manager or admin"),
            404: OpenApiResponse(description="Player not found")
        }
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete a player.
        
        This operation permanently removes the player from the system.
        Only the team manager or administrators can delete a player.
        """
        return super().destroy(request, *args, **kwargs)