# teams/views.py
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend
from teams.permissions import IsTeamOwnerOrAdmin

from teams.models import Team
from teams.serializers import TeamSerializer, TeamCreateSerializer, TeamUpdateSerializer

class TeamsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Teams management.
    Provides CRUD operations with appropriate permissions.
   
    Admins have full access to create, update, and delete teams.
    Authenticated users can view teams' details.
    """
    queryset = Team.objects.all().order_by('name')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    authentication_classes = [JWTAuthentication]

    def get_serializer_class(self):
        if self.action == 'create':
            return TeamCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TeamUpdateSerializer
        return TeamSerializer
    
    def get_permissions(self):
        """
        Assign permissions based on the action being performed.
        """
        if self.action == 'create':
            return [IsAuthenticated(), IsTeamOwnerOrAdmin()]
        elif self.action == 'update' or self.action == 'partial_update':
            return [IsAuthenticated(), IsTeamOwnerOrAdmin()]
        elif self.action == 'destroy':
            return [IsAuthenticated(), IsTeamOwnerOrAdmin()]
        return [IsAuthenticated(), IsTeamOwnerOrAdmin()]
    
    @extend_schema(
        summary="List all teams",
        description="Returns a list of all teams. Requires authentication.",
        responses={200: TeamSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new team",
        description="Create a new team. Only administrators can create teams.",
        request=TeamCreateSerializer,
        responses={201: TeamSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a team",
        description="Get details of a specific team. Requires authentication.",
        responses={200: TeamSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update a team",
        description="Fully update a specific team. Only administrators can update teams.",
        request=TeamUpdateSerializer,
        responses={200: TeamSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a team",
        description="Delete a specific team. Only administrators can delete teams.",
        responses={204: None}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
