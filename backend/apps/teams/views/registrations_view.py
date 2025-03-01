# register/views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from teams.permissions import IsRegistrationTeamCaptainOrAdmin

from teams.models import TeamRegistration
from teams.serializers.registration_serializers import (TeamRegistrationSerializer, TeamRegistrationCreateSerializer, TeamRegistrationApprovalSerializer)

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
