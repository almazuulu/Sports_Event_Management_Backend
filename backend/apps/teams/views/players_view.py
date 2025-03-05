from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from django.utils.translation import gettext_lazy as _

from teams.models import Player, Team
from teams.serializers import (
    PlayerSerializer, PlayerCreateSerializer, PlayerUpdateSerializer
)
from teams.permissions import (
    IsPlayerTeamManagerOrAdmin, IsTeamOwnerOrAdmin
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
        if self.action in ['update', 'partial_update']:
            return PlayerUpdateSerializer
        return PlayerSerializer
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsPlayerTeamManagerOrAdmin()]
        return [IsTeamOwnerOrAdmin()]
    
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
        description="Create a new player for any team. Only team managers can create players for their teams.",
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
        
        Creates a player for a specified team. The team must be included in the request data.
        Only the team manager of the specified team or administrators can create players.
        Jersey numbers must be unique within each team.
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
    
    @extend_schema(
        summary="Set player as team captain",
        description="Designate a player as the team captain. Only team managers and admins can do this.",
        parameters=[
            OpenApiParameter(name="id", location=OpenApiParameter.PATH, description="Player ID (UUID)", required=True, type=str),
        ],
        responses={
            200: PlayerSerializer,
            400: OpenApiResponse(description="Bad request - player is not active"),
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            403: OpenApiResponse(description="Forbidden - insufficient permissions"),
            404: OpenApiResponse(description="Player not found")
        }
    )
    @action(detail=True, methods=['patch'], url_path='set-as-captain',
            permission_classes=[IsPlayerTeamManagerOrAdmin])
    def set_as_captain(self, request, pk=None):
        """
        Designate a player as the team captain.
        
        This action sets the player as the captain of their team, which automatically
        removes captain status from any other player in the same team.
        Only active players can be designated as team captains.
        Only the team manager or administrators can set team captains.
        """
        player = self.get_object()
        
        # Check if player is active
        if not player.is_active:
            return Response(
                {"detail": _("Only active players can be designated as team captain.")},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Set as captain
        player.is_captain = True
        player.save()
        
        serializer = self.get_serializer(player)
        return Response(serializer.data)


class TeamPlayerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for listing players of a specific team.
    Read-only viewset that provides 'list' and 'retrieve' actions.
    """
    serializer_class = PlayerSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'position']
    ordering_fields = ['last_name', 'first_name', 'jersey_number']
    
    def get_queryset(self):
        """
        Filter players by team ID from URL.
        """
        team_id = self.kwargs['team_pk']
        return Player.objects.filter(team__id=team_id)
    
    @extend_schema(
        summary="List team players",
        description="Retrieve all players for a specific team.",
        parameters=[
            OpenApiParameter(name="team_pk", location=OpenApiParameter.PATH, description="Team ID (UUID)", required=True, type=str),
            OpenApiParameter(name="search", description="Search by name or position", required=False, type=str),
            OpenApiParameter(name="ordering", description="Order results by field (e.g., last_name, jersey_number)", required=False, type=str),
        ],
        responses={
            200: PlayerSerializer(many=True),
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            404: OpenApiResponse(description="Team not found")
        }
    )
    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of all players for a specific team.
        
        Returns a paginated list of players that belong to the specified team.
        """
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve team player",
        description="Get detailed information about a specific player in a team.",
        parameters=[
            OpenApiParameter(name="team_pk", location=OpenApiParameter.PATH, description="Team ID (UUID)", required=True, type=str),
            OpenApiParameter(name="pk", location=OpenApiParameter.PATH, description="Player ID (UUID)", required=True, type=str),
        ],
        responses={
            200: PlayerSerializer,
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            404: OpenApiResponse(description="Player not found in team")
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve detailed information about a specific player in a team.
        
        Returns complete player information for a player that belongs to the specified team.
        """
        return super().retrieve(request, *args, **kwargs)


class TeamPlayerCreateViewSet(viewsets.ModelViewSet):
    """
    API endpoint for adding, updating, and removing players for a specific team.
    """
    serializer_class = PlayerCreateSerializer
    http_method_names = ['post', 'put', 'patch', 'delete']
    permission_classes = [IsTeamOwnerOrAdmin]
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return PlayerUpdateSerializer
        return PlayerCreateSerializer
    
    def get_queryset(self):
        """
        Filter players by team ID from URL.
        """
        team_id = self.kwargs['team_pk']
        return Player.objects.filter(team__id=team_id)
    
    def perform_create(self, serializer):
        team_id = self.kwargs['team_pk']
        team = Team.objects.get(id=team_id)
        serializer.save(team=team)
    
    @extend_schema(
        summary="Create team player",
        description="Add a new player to a specific team. Only team managers and admins can do this.",
        parameters=[
            OpenApiParameter(name="team_pk", location=OpenApiParameter.PATH, description="Team ID (UUID)", required=True, type=str),
        ],
        request=PlayerCreateSerializer,
        responses={
            201: PlayerSerializer,
            400: OpenApiResponse(description="Invalid input data"),
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            403: OpenApiResponse(description="Permission denied - not team manager or admin"),
            404: OpenApiResponse(description="Team not found")
        }
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new player for the team.
        
        Adds a player to the specified team. The team is automatically set from the URL.
        Only the team manager or administrators can add players to a team.
        """
        team_id = self.kwargs['team_pk']
        
        # Set the team in the request data
        mutable_data = request.data.copy()
        mutable_data['team'] = team_id
        
        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )
    
    @extend_schema(
        summary="Update team player",
        description="Fully update a player in a specific team. Only team managers and admins can do this.",
        parameters=[
            OpenApiParameter(name="team_pk", location=OpenApiParameter.PATH, description="Team ID (UUID)", required=True, type=str),
            OpenApiParameter(name="pk", location=OpenApiParameter.PATH, description="Player ID (UUID)", required=True, type=str),
        ],
        request=PlayerUpdateSerializer,
        responses={
            200: PlayerSerializer,
            400: OpenApiResponse(description="Invalid input data"),
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            403: OpenApiResponse(description="Permission denied - not team manager or admin"),
            404: OpenApiResponse(description="Player not found in team")
        }
    )
    def update(self, request, *args, **kwargs):
        """
        Completely update a player in a specific team.
        
        Requires all mandatory fields. Only the team manager or administrators can update a player.
        """
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partial update team player",
        description="Partially update a player in a specific team. Only team managers and admins can do this.",
        parameters=[
            OpenApiParameter(name="team_pk", location=OpenApiParameter.PATH, description="Team ID (UUID)", required=True, type=str),
            OpenApiParameter(name="pk", location=OpenApiParameter.PATH, description="Player ID (UUID)", required=True, type=str),
        ],
        request=PlayerUpdateSerializer,
        responses={
            200: PlayerSerializer,
            400: OpenApiResponse(description="Invalid input data"),
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            403: OpenApiResponse(description="Permission denied - not team manager or admin"),
            404: OpenApiResponse(description="Player not found in team")
        }
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a player in a specific team.
        
        Update only specified fields. Only the team manager or administrators can update a player.
        """
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete team player",
        description="Remove a player from a specific team. Only team managers and admins can do this.",
        parameters=[
            OpenApiParameter(name="team_pk", location=OpenApiParameter.PATH, description="Team ID (UUID)", required=True, type=str),
            OpenApiParameter(name="pk", location=OpenApiParameter.PATH, description="Player ID (UUID)", required=True, type=str),
        ],
        responses={
            204: OpenApiResponse(description="Player successfully deleted"),
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            403: OpenApiResponse(description="Permission denied - not team manager or admin"),
            404: OpenApiResponse(description="Player not found in team")
        }
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete a player from a specific team.
        
        This operation permanently removes the player from the system.
        Only the team manager or administrators can delete a player.
        """
        return super().destroy(request, *args, **kwargs)