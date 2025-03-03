# register/views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from teams.permissions import IsRegistrationTeamCaptainOrAdmin, IsTeamOwnerOrAdmin

from teams.models import TeamRegistration
from teams.serializers.registration_serializers import (TeamRegistrationSerializer, TeamRegistrationCreateSerializer, TeamRegistrationApprovalSerializer)

from teams.models import Team
from rest_framework import status
from events.models import SportEvent
from django.utils import timezone

class TeamRegistrationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing team registrations for sport events.
    Team captains can register teams, while admins can approve/reject registrations.
    """
    queryset = TeamRegistration.objects.all().order_by('-registration_date')
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['team', 'sport_event', 'status']
    search_fields = ['team__name', 'sport_event__name', 'status']
    ordering_fields = ['registration_date', 'status']

    def get_serializer_class(self):
        """
        Choose the correct serializer based on the action.
        """
        if self.action == 'create':
            return TeamRegistrationCreateSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return TeamRegistrationApprovalSerializer
        return TeamRegistrationSerializer

    def get_permissions(self):
        """
        Assign permissions based on the action being performed.
        """
        if self.action == 'create':
            return [IsAuthenticated(), IsRegistrationTeamCaptainOrAdmin()]
        elif self.action == 'update' or self.action == 'partial_update':
            return [IsAuthenticated(), IsRegistrationTeamCaptainOrAdmin()]
        elif self.action == 'destroy':
            return [IsAuthenticated(), IsRegistrationTeamCaptainOrAdmin()]
        return [IsAuthenticated(), IsRegistrationTeamCaptainOrAdmin()]

    @extend_schema(
        summary="List team registrations",
        description="Retrieve a list of team registrations for sport events. Can be filtered by team, sport event, and registration status.",
        responses={200: TeamRegistrationSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """
        List all team registrations. This can be filtered by team, sport event, or status.
        """
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Create a team registration",
        description="Register a team for a sport event. Only the team captain can register a team.",
        request=TeamRegistrationCreateSerializer,
        responses={201: TeamRegistrationSerializer}
    )
    def create(self, request, *args, **kwargs):
        """
        Register a team for a specific sport event.
        """
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a team registration",
        description="Retrieve details of a specific team registration.",
        responses={200: TeamRegistrationSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific team registration by its ID.
        """
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Approve or reject a team registration",
        description="Approve or reject a team registration. Only admins can approve or reject.",
        request=TeamRegistrationApprovalSerializer,
        responses={200: TeamRegistrationSerializer}
    )
    def update(self, request, *args, **kwargs):
        """
        Update the status of a team registration (approve or reject).
        Only admins can perform this action.
        """
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update a team registration",
        description="Partially update a team registration, such as modifying notes or status.",
        request=TeamRegistrationApprovalSerializer,
        responses={200: TeamRegistrationSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update the registration, such as updating the registration status or notes.
        """
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a team registration",
        description="Delete a team registration. Only admins or the team captain can delete a registration.",
        responses={204: "No content"}
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete a specific team registration.
        Only admins or team captains can delete their team's registration.
        """
        # Retrieve the registration object to delete
        registration = self.get_object()

        # Perform the deletion
        registration.delete()

        # Return a successful response
        return Response(status=status.HTTP_204_NO_CONTENT)

class SportEventRegistrationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to list all team registrations for a specific sport event.
    """
    serializer_class = TeamRegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter registrations by the sport event ID.
        """
        sport_event_id = self.kwargs['sport_event_id']
        return TeamRegistration.objects.filter(sport_event__id=sport_event_id)

class SportEventRegistrationCreateViewSet(viewsets.ViewSet):
    """
    API endpoint to register a team for a specific sport event.
    """
    permission_classes = [IsAuthenticated, IsRegistrationTeamCaptainOrAdmin]

    def create(self, request, *args, **kwargs):
        sport_event_id = kwargs['sport_event_id']
        team_id = request.data.get('team')
        team = Team.objects.get(id=team_id)
        sport_event = SportEvent.objects.get(id=sport_event_id)
        
        # Check if the registration is open for this event
        if sport_event.registration_deadline and sport_event.registration_deadline < timezone.now():
            return Response({"detail": "Registration deadline has passed."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a registration entry
        registration_data = {
            'team': team.id,
            'sport_event': sport_event.id,
            'notes': request.data.get('notes', ''),
        }
        
        serializer = TeamRegistrationCreateSerializer(data=registration_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
