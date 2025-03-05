from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from django.utils.translation import gettext_lazy as _

from events.models import SportEvent
from teams.models import TeamRegistration, Team
from teams.serializers import (
    TeamRegistrationSerializer, TeamRegistrationCreateSerializer,
    TeamRegistrationApprovalSerializer
)
from teams.permissions import (
    IsTeamManagerOrAdmin, IsRegistrationTeamManagerOrAdmin, 
    CanManageRegistration, IsAdminUser
)
from users.permissions import IsAdminUser


class TeamRegistrationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing team registrations across all sport events.
    
    Admins can view and manage all registrations.
    Team managers can view their own team's registrations.
    """
    queryset = TeamRegistration.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['team', 'sport_event', 'status']
    ordering_fields = ['registration_date', 'status']
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return TeamRegistrationApprovalSerializer
        return TeamRegistrationSerializer
    
    def get_permissions(self):
        if self.action == 'list':
            return [IsAdminUser()]
        elif self.action in ['retrieve', 'destroy']:
            return [IsRegistrationTeamManagerOrAdmin()]
        elif self.action in ['update', 'partial_update']:
            return [IsAdminUser()]
        return [IsTeamManagerOrAdmin()]
    
    @extend_schema(
        summary="List team registrations",
        description="List all team registrations across sport events. Admin access only.",
        parameters=[
            OpenApiParameter(name="team", description="Filter by team ID", required=False, type=str),
            OpenApiParameter(name="sport_event", description="Filter by sport event ID", required=False, type=str),
            OpenApiParameter(name="status", description="Filter by status (pending, approved, rejected)", required=False, type=str),
            OpenApiParameter(name="ordering", description="Order results by field (e.g., registration_date, status)", required=False, type=str),
        ],
        responses={
            200: TeamRegistrationSerializer(many=True),
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            403: OpenApiResponse(description="Permission denied - admin access required")
        }
    )
    def list(self, request, *args, **kwargs):
        """
        List all team registrations across sport events.
        
        Returns a paginated list of all team registrations.
        Note: Only administrators can access this endpoint.
        """
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve team registration",
        description="Get details of a specific team registration.",
        parameters=[
            OpenApiParameter(name="id", location=OpenApiParameter.PATH, description="Registration ID (UUID)", required=True, type=str),
        ],
        responses={
            200: TeamRegistrationSerializer,
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            403: OpenApiResponse(description="Permission denied - not team manager or admin"),
            404: OpenApiResponse(description="Registration not found")
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve details of a specific team registration.
        
        Returns detailed information about a team's registration for a sport event.
        Accessible by team manager of the registered team or admins.
        """
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary="Create team registration",
        description="Register a team for a sport event. Only team managers can register their teams.",
        request=TeamRegistrationCreateSerializer,
        responses={
            201: TeamRegistrationSerializer,
            400: OpenApiResponse(description="Invalid input data or team already registered"),
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            403: OpenApiResponse(description="Permission denied - not team manager or admin")
        }
    )
    def create(self, request, *args, **kwargs):
        """
        Register a team for a sport event.
        
        Creates a new team registration for a specified sport event.
        The team and sport event must be included in the request data.
        Only the team manager of the specified team can create a registration.
        
        Validates that:
        - The team hasn't already registered for this event
        - The registration deadline hasn't passed
        - The event hasn't reached its maximum team capacity
        """
        return super().create(request, *args, **kwargs)
    
    
    @extend_schema(
        summary="Approve or reject registration",
        description="Approve or reject a team registration. Admin access only.",
        parameters=[
            OpenApiParameter(name="id", location=OpenApiParameter.PATH, description="Registration ID (UUID)", required=True, type=str),
        ],
        request=TeamRegistrationApprovalSerializer,
        responses={
            200: TeamRegistrationSerializer,
            400: OpenApiResponse(description="Invalid input data"),
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            403: OpenApiResponse(description="Permission denied - admin access required"),
            404: OpenApiResponse(description="Registration not found")
        }
    )
    def update(self, request, *args, **kwargs):
        """
        Approve or reject a team registration.
        
        This action can only be performed by administrators.
        Status must be set to either 'approved' or 'rejected'.
        """
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Partially update registration",
        description="Partially update a team registration. Admin access only.",
        parameters=[
            OpenApiParameter(name="id", location=OpenApiParameter.PATH, description="Registration ID (UUID)", required=True, type=str),
        ],
        request=TeamRegistrationApprovalSerializer,
        responses={
            200: TeamRegistrationSerializer,
            400: OpenApiResponse(description="Invalid input data"),
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            403: OpenApiResponse(description="Permission denied - admin access required"),
            404: OpenApiResponse(description="Registration not found")
        }
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a team registration.
        
        This action can only be performed by administrators.
        Status can be set to either 'approved' or 'rejected'.
        """
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Cancel registration",
        description="Cancel a pending team registration. Only pending registrations can be cancelled.",
        parameters=[
            OpenApiParameter(name="id", location=OpenApiParameter.PATH, description="Registration ID (UUID)", required=True, type=str),
        ],
        responses={
            204: OpenApiResponse(description="Registration successfully cancelled"),
            400: OpenApiResponse(description="Only pending registrations can be cancelled"),
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            403: OpenApiResponse(description="Permission denied - not team manager or admin"),
            404: OpenApiResponse(description="Registration not found")
        }
    )
    def destroy(self, request, *args, **kwargs):
        """
        Cancel a team registration.
        
        This action permanently removes the registration.
        Only pending registrations can be cancelled.
        This action can be performed by the team manager or administrators.
        """
        registration = self.get_object()
        
        if registration.status != 'pending':
            return Response(
                {"detail": _("Only pending registrations can be cancelled.")},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().destroy(request, *args, **kwargs)


class SportEventRegistrationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for listing team registrations for a specific sport event.
    Read-only viewset that provides 'list' and 'retrieve' actions.
    Only accessible by administrators.
    """
    serializer_class = TeamRegistrationSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['registration_date', 'status']
    
    def get_queryset(self):
        """
        Filter registrations by sport event ID from URL.
        """
        sport_event_id = self.kwargs['sport_event_pk']
        return TeamRegistration.objects.filter(sport_event__id=sport_event_id)
    
    @extend_schema(
        summary="List sport event registrations",
        description="List all team registrations for a specific sport event. Admin access only.",
        parameters=[
            OpenApiParameter(name="sport_event_pk", location=OpenApiParameter.PATH, description="Sport Event ID (UUID)", required=True, type=str),
            OpenApiParameter(name="ordering", description="Order results by field (e.g., registration_date, status)", required=False, type=str),
        ],
        responses={
            200: TeamRegistrationSerializer(many=True),
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            403: OpenApiResponse(description="Permission denied - admin access required"),
            404: OpenApiResponse(description="Sport event not found")
        }
    )
    def list(self, request, *args, **kwargs):
        """
        List all team registrations for a specific sport event.
        
        Returns a paginated list of team registrations for the specified sport event.
        Note: Only administrators can access this endpoint.
        """
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Retrieve sport event registration",
        description="Get details of a specific team registration for a sport event. Admin access only.",
        parameters=[
            OpenApiParameter(name="sport_event_pk", location=OpenApiParameter.PATH, description="Sport Event ID (UUID)", required=True, type=str),
            OpenApiParameter(name="pk", location=OpenApiParameter.PATH, description="Registration ID (UUID)", required=True, type=str),
        ],
        responses={
            200: TeamRegistrationSerializer,
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            403: OpenApiResponse(description="Permission denied - admin access required"),
            404: OpenApiResponse(description="Registration not found")
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve details of a specific team registration for a sport event.
        
        Returns detailed information about a team's registration for the specified sport event.
        Note: Only administrators can access this endpoint.
        """
        return super().retrieve(request, *args, **kwargs)


class SportEventRegistrationCreateViewSet(viewsets.ModelViewSet):
    """
    API endpoint for registering a team for a specific sport event.
    """
    serializer_class = TeamRegistrationCreateSerializer
    http_method_names = ['post']
    permission_classes = [IsTeamManagerOrAdmin]
    
    def get_queryset(self):
        """
        Filter registrations by sport event ID from URL.
        """
        sport_event_id = self.kwargs['sport_event_pk']
        return TeamRegistration.objects.filter(sport_event__id=sport_event_id)
    
    @extend_schema(
        summary="Register team for sport event",
        description="Register a team for a specific sport event. Only team managers can register their teams.",
        parameters=[
            OpenApiParameter(name="sport_event_pk", location=OpenApiParameter.PATH, description="Sport Event ID (UUID)", required=True, type=str),
        ],
        request=TeamRegistrationCreateSerializer,
        responses={
            201: TeamRegistrationSerializer,
            400: OpenApiResponse(description="Invalid input data or team already registered"),
            401: OpenApiResponse(description="Authentication credentials were not provided"),
            403: OpenApiResponse(description="Permission denied - not team manager or admin"),
            404: OpenApiResponse(description="Sport event not found")
        }
    )
    def create(self, request, *args, **kwargs):
        """
        Register a team for a specific sport event.
        
        Creates a new team registration for the specified sport event.
        The sport event is automatically determined from the URL.
        Only the team manager can register their team for an event.
        Validates that the team hasn't already registered and that the registration deadline hasn't passed.
        """
        sport_event_id = self.kwargs['sport_event_pk']
        
        # Set the sport event in the request data
        mutable_data = request.data.copy()
        mutable_data['sport_event'] = sport_event_id
        
        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )