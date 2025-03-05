from rest_framework import generics
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiExample
from teams.models import Team
from teams.serializers import PublicTeamSerializer
from teams.permissions import PublicReadOnly

# PublicTeamListView with Swagger description
@extend_schema(
    summary="List all the teams",
    description="Retrieve a paginated list of teams. ",
    responses={200: PublicTeamSerializer},
    examples=[
        OpenApiExample(
            'Example response - List of Teams',
            value={
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "name": "Thunderbolts",
                "description": "Local basketball team from New York",
                "captain": {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
                    "email": "captain@example.com",
                    "first_name": "John",
                    "last_name": "Smith"
                },
                "contact_email": "team@example.com",
                "contact_phone": "+1234567890",
                "status": "active",
                "player_count": 12,
                "created_at": "2025-01-15T12:00:00Z"
            },
            response_only=True,
        )
    ]
)
class PublicTeamListView(generics.ListAPIView):
    """
    Public endpoint to get a paginated list of teams.
    """
    queryset = Team.objects.all()
    serializer_class = PublicTeamSerializer
    permission_classes = [PublicReadOnly]  # Allow any user (public access)
    pagination_class = None  # Use default pagination

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Apply search if query parameter is present
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        return queryset

# PublicTeamDetailView with Swagger description
@extend_schema(
    summary="Retrieve a team",
    description="Retrieve detailed information of a specific team by its ID (UUID). This endpoint provides complete details including the team name, captain, contact info, status, and more.",
    responses={200: PublicTeamSerializer},
    examples=[
        OpenApiExample(
            'Example response - Team Details',
            value={
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "name": "Thunderbolts",
                "description": "Local basketball team from New York",
                "captain": {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
                    "email": "captain@example.com",
                    "first_name": "John",
                    "last_name": "Smith"
                },
                "contact_email": "team@example.com",
                "contact_phone": "+1234567890",
                "status": "active",
                "player_count": 12,
                "created_at": "2025-01-15T12:00:00Z"
            },
            response_only=True,
        )
    ]
)
class PublicTeamDetailView(generics.RetrieveAPIView):
    """
    Public endpoint to get detailed information of a specific team.
    """
    queryset = Team.objects.all()
    serializer_class = PublicTeamSerializer
    permission_classes = [PublicReadOnly]  # Allow any user (public access)
    lookup_field = 'id'  # Look up by the 'id' (UUID)
