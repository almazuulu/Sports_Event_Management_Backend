from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

from teams.models import Team
from teams.serializers import PublicTeamSerializer
from teams.permissions import PublicReadOnly


class PublicTeamListView(generics.ListAPIView):
    """
    API endpoint for listing teams with limited information for public viewing.
    This endpoint doesn't require authentication.
    """
    queryset = Team.objects.filter(status='active')
    serializer_class = PublicTeamSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    
    @extend_schema(
        summary="List public teams",
        description="Returns a list of active teams with limited information. No authentication required.",
        parameters=[
            OpenApiParameter(name="search", description="Search teams by name", required=False, type=str),
            OpenApiParameter(name="ordering", description="Order results by name (e.g., name, -name)", required=False, type=str),
        ],
        responses={
            200: PublicTeamSerializer(many=True),
        }
    )
    def get(self, request, *args, **kwargs):
        """
        List all active teams with limited information.
        
        Returns a paginated list of active teams with basic information
        suitable for public viewing. Includes team name, logo, and 
        general team statistics.
        
        This endpoint is accessible without authentication.
        """
        return super().get(request, *args, **kwargs)


class PublicTeamDetailView(generics.RetrieveAPIView):
    """
    API endpoint for viewing details of a specific team for public viewing.
    This endpoint doesn't require authentication.
    """
    queryset = Team.objects.filter(status='active')
    serializer_class = PublicTeamSerializer
    permission_classes = [AllowAny]
    
    @extend_schema(
        summary="Get public team details",
        description="Returns public information about a specific team. No authentication required.",
        parameters=[
            OpenApiParameter(name="pk", location=OpenApiParameter.PATH, description="Team ID (UUID)", required=True, type=str),
        ],
        responses={
            200: PublicTeamSerializer,
            404: OpenApiResponse(description="Team not found or not active")
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve public information about a specific team.
        
        Returns basic information about the requested team including
        team name, logo, manager name, and active player count.
        
        Only active teams are visible through this endpoint.
        This endpoint is accessible without authentication.
        """
        return super().get(request, *args, **kwargs)