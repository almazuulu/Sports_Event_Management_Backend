from rest_framework import viewsets, permissions
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from ..models import Score
from ..serializers import ScoreSerializer, ScoreCreateSerializer, ScoreUpdateSerializer
from ..permissions import CanManageScores, CanVerifyScores
from rest_framework.pagination import PageNumberPagination

class ScorePagination(PageNumberPagination):
    page_size = 10  # Customize the pagination size if needed
    page_size_query_param = 'page_size'
    max_page_size = 100

class ScoreViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing scores, including retrieval, creation, updating, and verification.
    """
    queryset = Score.objects.all()
    pagination_class = ScorePagination

    def get_serializer_class(self):
        """
        Returns different serializers based on the action being performed.
        """
        if self.action == 'create':
            return ScoreCreateSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return ScoreUpdateSerializer
        return ScoreSerializer

    def get_permissions(self):
        """
        Defines the permissions required for each action.
        """
        if self.action == 'create':
            permission_classes = [IsAdminUser]  # Only admins can create scores
        elif self.action == 'verify':
            permission_classes = [CanVerifyScores]  # Only admins can verify scores
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [CanManageScores]  # Assigned scorekeeper or admin
        else:
            permission_classes = [permissions.IsAuthenticated]  # All authenticated users
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Filter the queryset based on user permissions.
        """
        queryset = Score.objects.all()
        user = self.request.user
        if user.role == 'team_captain':
            # Filter scores only for the teams the user is associated with
            queryset = queryset.filter(team__captain=user)
        return queryset

    @extend_schema(
        summary='Create a new score record for a game.',
        description='Only accessible by admins to create new scores automatically linked with the game.',
        request=ScoreCreateSerializer,
        responses={201: ScoreSerializer}
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new score record for a game.
        Only accessible by admins.
        """
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary='Update a score record.',
        description='This method is overridden to block PATCH requests.',
        responses={405: 'Method Not Allowed'}
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Update a score (PATCH method is restricted).
        This method is overridden to block PATCH requests.
        """
        raise MethodNotAllowed("PATCH method is not allowed.")

    @extend_schema(
        summary='Delete a score record.',
        description='This method is overridden to block DELETE requests.',
        responses={405: 'Method Not Allowed'}
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete a score (DELETE method is restricted).
        This method is overridden to block DELETE requests.
        """
        raise MethodNotAllowed("DELETE method is not allowed.")

    @extend_schema(
        summary='Verify a score record.',
        description='Admins can verify completed scores and mark them as official.',
        request=None,  # You can add a request schema if needed, such as for an optional confirmation field
        responses={200: ScoreSerializer}
    )
    @action(detail=True, methods=['post'], permission_classes=[CanVerifyScores])
    def verify(self, request, *args, **kwargs):
        """
        Mark a score as verified (only accessible by admins).
        """
        score = self.get_object()
        score.is_verified = True
        score.save()
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        summary='List all scores with filtering options.',
        description='Retrieve a paginated list of scores with options to filter by sport type, event, or status.',
        responses={200: ScoreSerializer}
    )
    def list(self, request, *args, **kwargs):
        """
        List all game scores with filtering options.
        """
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary='Retrieve detailed information about a specific score.',
        description='Retrieve detailed information, including all scoring events, for a specific score.',
        responses={200: ScoreSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Get detailed information about a specific score.
        """
        return super().retrieve(request, *args, **kwargs)
