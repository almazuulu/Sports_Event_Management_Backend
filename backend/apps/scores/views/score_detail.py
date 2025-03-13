from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

from scores.models import Score, ScoreDetail
from scores.serializers import (
    ScoreDetailSerializer,
    ScoreDetailCreateSerializer,
)
from scores.permissions import CanManageScores


class ScoreDetailViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing score details (individual scoring events within a game).
    
    Provides CRUD operations with appropriate permissions:
    - Scorekeepers can add and update scoring events for their assigned games
    - Admins can view, create, update, and delete scoring events
    - Public users can view scoring events
    
    Authentication is done via JWT Bearer token.
    """
    queryset = ScoreDetail.objects.all()
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['score', 'team', 'player', 'event_type']
    ordering_fields = ['time_occurred', 'minute', 'created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ScoreDetailCreateSerializer
        return ScoreDetailSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, CanManageScores]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_serializer_context(self):
        """
        Add the score object to the serializer context if score_id is provided
        """
        context = super().get_serializer_context()
        
        if self.action == 'create' and 'score_id' in self.kwargs:
            try:
                context['score'] = Score.objects.get(id=self.kwargs['score_id'])
            except Score.DoesNotExist:
                pass
        
        return context
    
    def perform_create(self, serializer):
        """
        Set the score and created_by fields when creating a score detail
        """
        # If nested under a score, get the score from URL
        if 'score_id' in self.kwargs:
            score = Score.objects.get(id=self.kwargs['score_id'])
            serializer.save(score=score, created_by=self.request.user)
        else:
            serializer.save(created_by=self.request.user)
    
    @extend_schema(
        summary="List score details",
        description="Get a list of scoring events with filtering options",
        parameters=[
            OpenApiParameter(name="score", description="Filter by score ID", required=False, type=str),
            OpenApiParameter(name="team", description="Filter by team ID", required=False, type=str),
            OpenApiParameter(name="player", description="Filter by player ID", required=False, type=str),
            OpenApiParameter(name="event_type", description="Filter by event type", required=False, type=str),
            OpenApiParameter(name="ordering", description="Order by field", required=False, type=str)
        ],
        responses={200: ScoreDetailSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """
        List all scoring events.
        Supports filtering by score, team, player, and event_type.
        """
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Create score detail",
        description="Create a new scoring event",
        request=ScoreDetailCreateSerializer,
        responses={
            201: ScoreDetailSerializer,
            400: OpenApiResponse(description="Bad request - invalid data")
        }
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new scoring event.
        Only scorekeepers assigned to the game or users with score management 
        permissions can create scoring events.
        """
        return super().create(request, *args, **kwargs)
    
    @extend_schema(
        summary="Retrieve score detail",
        description="Get details of a specific scoring event",
        responses={
            200: ScoreDetailSerializer,
            404: OpenApiResponse(description="Not found - scoring event does not exist")
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve detailed information about a specific scoring event.
        """
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary="Update score detail",
        description="Update a scoring event (full update)",
        request=ScoreDetailSerializer,
        responses={
            200: ScoreDetailSerializer,
            400: OpenApiResponse(description="Bad request - invalid data"),
            403: OpenApiResponse(description="Forbidden - insufficient permissions"),
            404: OpenApiResponse(description="Not found - scoring event does not exist")
        }
    )
    def update(self, request, *args, **kwargs):
        """
        Update all details of an existing scoring event (full update).
        Only scorekeepers assigned to the game or users with score management
        permissions can update scoring events.
        """
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Partially update score detail",
        description="Update specific fields of a scoring event",
        request=ScoreDetailSerializer,
        responses={
            200: ScoreDetailSerializer,
            400: OpenApiResponse(description="Bad request - invalid data"),
            403: OpenApiResponse(description="Forbidden - insufficient permissions"),
            404: OpenApiResponse(description="Not found - scoring event does not exist")
        }
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Update specific fields of an existing scoring event (partial update).
        Only scorekeepers assigned to the game or users with score management
        permissions can update scoring events.
        """
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Delete score detail",
        description="Remove a scoring event from the system",
        responses={
            204: OpenApiResponse(description="No content - scoring event successfully deleted"),
            403: OpenApiResponse(description="Forbidden - insufficient permissions"),
            404: OpenApiResponse(description="Not found - scoring event does not exist")
        }
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete a scoring event from the system.
        Only scorekeepers assigned to the game or users with score management
        permissions can delete scoring events.
        """
        return super().destroy(request, *args, **kwargs)
    
    @extend_schema(
        summary="Score details for a specific score",
        description="Get all scoring events for a specific game score",
        parameters=[
            OpenApiParameter(name="score_id", location=OpenApiParameter.PATH, description="Score ID", required=True, type=str)
        ],
        responses={200: ScoreDetailSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='by-score/(?P<score_id>[^/.]+)')
    def by_score(self, request, score_id=None):
        """
        Get all scoring events for a specific game score.
        Ordered by time occurred.
        """
        score_details = self.queryset.filter(score_id=score_id).order_by('time_occurred')
        
        page = self.paginate_queryset(score_details)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(score_details, many=True)
        return Response(serializer.data)