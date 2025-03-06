from rest_framework import viewsets, status, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from django.utils.translation import gettext_lazy as _

from teams.models import Team, Player, TeamRegistration
from teams.serializers import (
    TeamSerializer, TeamCreateSerializer, TeamUpdateSerializer, 
    TeamDetailSerializer, PlayerSerializer, TeamRegistrationSerializer,
    SetTeamCaptainSerializer
)
from teams.permissions import (
    IsTeamManagerOrAdmin, IsTeamOwnerOrAdmin, IsPlayerTeamManagerOrAdmin,
    IsTeamCaptain, IsTeamManagerOrCaptain, PublicReadOnly
)


class TeamsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing teams.
    
    Team managers can create and manage their own teams.
    Admins can manage all teams.
    """
    queryset = Team.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TeamCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TeamUpdateSerializer
        elif self.action == 'retrieve':
            return TeamDetailSerializer
        return TeamSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'team_players']:
            # Public access for GET methods of main resources
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, IsTeamManagerOrAdmin]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsTeamOwnerOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save()

    @extend_schema(
        summary="List teams",
        description="Returns a list of all teams. Supports filtering by status and searching by name/description.",
        parameters=[
            OpenApiParameter(name="status", description="Filter by team status (active, inactive, suspended)", required=False, type=str),
            OpenApiParameter(name="search", description="Search teams by name or description", required=False, type=str),
            OpenApiParameter(name="ordering", description="Order results by field (e.g., name, created_at)", required=False, type=str),
        ],
        responses={
            200: TeamSerializer(many=True),
            401: OpenApiResponse(description="Authentication credentials were not provided")
        }
    )
    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of all teams.
        
        Returns a paginated list of teams with basic information.
        """
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Create team",
        description="Create a new team. The authenticated user will be set as the team manager.",
        request=TeamCreateSerializer,
        responses={
            201: TeamSerializer,
            400: OpenApiResponse(description="Invalid input data"),
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            403: OpenApiResponse(description="Permission denied - user does not have team_manager role")
        }
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new team.
        
        The authenticated user must have the team_manager role.
        The user will automatically be assigned as the team manager.
        """
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve team",
        description="Get detailed information about a specific team, including players and registrations.",
        parameters=[
            OpenApiParameter(name="id", location=OpenApiParameter.PATH, description="Team ID (UUID)", required=True, type=str),
        ],
        responses={
            200: TeamDetailSerializer,
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            404: OpenApiResponse(description="Team not found")
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve detailed information about a specific team.
        
        Returns complete team information including players and event registrations.
        """
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update team",
        description="Fully update a team. Only the team manager or administrators can perform this action.",
        parameters=[
            OpenApiParameter(name="id", location=OpenApiParameter.PATH, description="Team ID (UUID)", required=True, type=str),
        ],
        request=TeamUpdateSerializer,
        responses={
            200: TeamSerializer,
            400: OpenApiResponse(description="Invalid input data"),
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            403: OpenApiResponse(description="Permission denied - not team manager or admin"),
            404: OpenApiResponse(description="Team not found")
        }
    )
    def update(self, request, *args, **kwargs):
        """
        Completely update a team.
        
        Requires all mandatory fields. Only the team manager or administrators can update a team.
        """
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partial update team",
        description="Partially update a team. Only the team manager or administrators can perform this action.",
        parameters=[
            OpenApiParameter(name="id", location=OpenApiParameter.PATH, description="Team ID (UUID)", required=True, type=str),
        ],
        request=TeamUpdateSerializer,
        responses={
            200: TeamSerializer,
            400: OpenApiResponse(description="Invalid input data"),
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            403: OpenApiResponse(description="Permission denied - not team manager or admin"),
            404: OpenApiResponse(description="Team not found")
        }
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a team.
        
        Update only specified fields. Only the team manager or administrators can update a team.
        """
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete team",
        description="Delete a team. This operation will also remove all associated players and registrations.",
        parameters=[
            OpenApiParameter(name="id", location=OpenApiParameter.PATH, description="Team ID (UUID)", required=True, type=str),
        ],
        responses={
            204: OpenApiResponse(description="Team successfully deleted"),
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            403: OpenApiResponse(description="Permission denied - not team manager or admin"),
            404: OpenApiResponse(description="Team not found")
        }
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete a team.
        
        This operation permanently removes the team and all associated data.
        Only the team manager or administrators can delete a team.
        """
        return super().destroy(request, *args, **kwargs)
    
    @extend_schema(
        summary="List team players",
        description="Retrieve all players for a specific team.",
        parameters=[
            OpenApiParameter(name="id", location=OpenApiParameter.PATH, description="Team ID (UUID)", required=True, type=str),
            OpenApiParameter(name="is_active", description="Filter by active status (true/false)", required=False, type=bool),
        ],
        responses={
            200: PlayerSerializer(many=True),
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            404: OpenApiResponse(description="Team not found")
        }
    )
    @action(detail=True, methods=['get'], url_path='players')
    def team_players(self, request, pk=None):
        """
        Get a list of all players for a specific team.
        
        Returns detailed information about all players in the specified team.
        Optional filtering by active status.
        """
        team = self.get_object()
        players = team.players.all()
        
        # Apply filters if provided
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            players = players.filter(is_active=is_active)
        
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="List team registrations",
        description="Retrieve all sport event registrations for a specific team.",
        parameters=[
            OpenApiParameter(name="id", location=OpenApiParameter.PATH, description="Team ID (UUID)", required=True, type=str),
            OpenApiParameter(name="status", description="Filter by registration status (pending, approved, rejected)", required=False, type=str),
        ],
        responses={
            200: TeamRegistrationSerializer(many=True),
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            403: OpenApiResponse(description="Permission denied - not team manager or admin"),
            404: OpenApiResponse(description="Team not found")
        }
    )
    @action(detail=True, methods=['get'], url_path='registrations', permission_classes=[IsTeamOwnerOrAdmin])
    def team_registrations(self, request, pk=None):
        """
        Get a list of all sport event registrations for a specific team.
        
        Returns information about all events the team has registered for.
        Only accessible by the team manager or administrators.
        Optional filtering by registration status.
        """
        team = self.get_object()
        registrations = team.event_registrations.all()
        
        # Apply filters if provided
        status_filter = request.query_params.get('status')
        if status_filter:
            registrations = registrations.filter(status=status_filter)
        
        serializer = TeamRegistrationSerializer(registrations, many=True)
        return Response(serializer.data)
    
    @extend_schema(
    summary="Set team captain",
    description="Set a player as the captain of a team. Only team managers and admins can do this.",
    parameters=[
        OpenApiParameter(name="id", location=OpenApiParameter.PATH, description="Team ID (UUID)", required=True, type=str),
        ],
        request=SetTeamCaptainSerializer,
        responses={
            200: TeamSerializer,
            400: OpenApiResponse(description="Bad request - player not found or not active"),
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            403: OpenApiResponse(description="Forbidden - insufficient permissions"),
            404: OpenApiResponse(description="Team not found")
        }
    )
    @action(detail=True, methods=['patch'], url_path='set-captain',
            permission_classes=[IsTeamOwnerOrAdmin])
    def set_captain(self, request, pk=None):
        """
        Set a player as the captain of a team.
        
        Takes a player_id in the request and sets that player as the team captain.
        Automatically removes captain status from any other player in the team.
        Only active players can be designated as team captains.
        Only the team manager or administrators can set team captains.
        """
        team = self.get_object()
        serializer = SetTeamCaptainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        player_id = serializer.validated_data['player_id']
        
        try:
            player = Player.objects.get(id=player_id, team=team)
        except Player.DoesNotExist:
            return Response(
                {"detail": _("Player not found in this team.")},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if player is active
        if not player.is_active:
            return Response(
                {"detail": _("Only active players can be designated as team captain.")},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Reset captain status for all other players in the team
        Player.objects.filter(team=team, is_captain=True).exclude(id=player.id).update(is_captain=False)
        
        # Set this player as captain
        player.is_captain = True
        player.save()
        
        # Update team_captain field in Team model
        team.team_captain = player
        team.save()
        
        # Return updated team information
        serializer = self.get_serializer(team)
        return Response(serializer.data)