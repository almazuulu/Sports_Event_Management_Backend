# views.py (Teams app)
from rest_framework import generics
from rest_framework.permissions import AllowAny
# from ..models import Team
from teams.models import Team
# from .serializers import PublicTeamSerializer
from teams.serializers import PublicTeamSerializer
# from .permissions import PublicReadOnly
from teams.permissions import PublicReadOnly

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

class PublicTeamDetailView(generics.RetrieveAPIView):
    """
    Public endpoint to get detailed information of a specific team.
    """
    queryset = Team.objects.all()
    serializer_class = PublicTeamSerializer
    permission_classes = [PublicReadOnly]  # Allow any user (public access)
    lookup_field = 'id'  # Look up by the 'id' (UUID)
