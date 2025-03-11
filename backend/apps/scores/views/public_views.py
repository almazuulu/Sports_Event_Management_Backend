from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from ..models import Score  # Assuming the Score model exists
from ..serializers import PublicScoreSerializer, PublicLiveScoreSerializer, PublicScoreSerializer

class PublicScoreViewSet(viewsets.GenericViewSet):
    """
    Provides public access to score information, including live scores and details.
    """
    
    queryset = Score.objects.all()  # Or use any other method to get scores

    @extend_schema(
        summary="List all scores (Public)",
        description="This endpoint provides public access to basic score information for all games.",
        responses={200: PublicScoreSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        scores = self.queryset.all()
        serializer = PublicScoreSerializer(scores, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Retrieve score details for a specific game (Public)",
        description="This endpoint provides public access to a specific game's score information.",
        responses={200: PublicScoreSerializer},
    )
    @action(detail=True, methods=['get'])
    def details(self, request, *args, **kwargs):
        score = self.get_object()
        serializer = PublicScoreSerializer(score)
        return Response(serializer.data)

    @extend_schema(
        summary="Retrieve live scores (Public)",
        description="This endpoint provides real-time access to scores of ongoing games.",
        responses={200: PublicLiveScoreSerializer(many=True)},
    )
    @action(detail=False, methods=['get'])
    def live(self, request, *args, **kwargs):
        # Filter scores to only include ongoing games
        live_scores = self.queryset.filter(status='in_progress')  # Example filter for live games
        serializer = PublicLiveScoreSerializer(live_scores, many=True)
        return Response(serializer.data)
