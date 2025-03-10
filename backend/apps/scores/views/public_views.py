from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from ..models import Score
from ..serializers import PublicScoreSerializer, PublicLiveScoreSerializer

class PublicScoreListPagination(PageNumberPagination):
    """
    Custom pagination class to paginate score list for public access.
    You can configure the `page_size` here, or override it globally in settings.
    """
    page_size = 10  # Set default page size, or you can change this in the settings

class PublicScoreViewSet(viewsets.GenericViewSet):
    """
    API endpoint for public access to score list with basic information.
    """
    queryset = Score.objects.all()  # Get all scores
    serializer_class = PublicScoreSerializer  # Use PublicScoreSerializer
    permission_classes = [AllowAny]  # Public access - no authentication required
    pagination_class = PublicScoreListPagination  # Use custom pagination class

    @extend_schema(
        summary="Public list of scores",
        description="Retrieve a paginated list of all scores with limited information for public access.",
        responses={200: PublicScoreSerializer(many=True)},
    )
    def list(self, request):
        """
        List all scores with limited public information (paginated).
        No authentication required.
        """
        # Fetch all scores from the database
        scores = Score.objects.all()

        # Apply pagination
        page = self.paginate_queryset(scores)
        if page is not None:
            # Serialize and return paginated response
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # If no pagination, return all scores (in case of small data)
        serializer = self.get_serializer(scores, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Public access to a specific game's score",
        description="Retrieve the details of a specific score record for a game, accessible to the public.",
        responses={200: PublicScoreSerializer},
    )
    def retrieve(self, request, pk=None):
        """
        Retrieve the details of a specific score record.
        Accessible to the public (no authentication required).
        """
        try:
            score = Score.objects.get(pk=pk)
        except Score.DoesNotExist:
            return Response({"detail": "Score not found."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the score object using PublicScoreSerializer
        serializer = self.get_serializer(score)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
class PublicLiveScoreViewSet(viewsets.GenericViewSet):
    """
    API endpoint for public access to live scores of ongoing games.
    """
    permission_classes = [AllowAny]  # Public access - no authentication required

    @extend_schema(
        summary="Public access to live scores",
        description="Retrieve a list of ongoing games with current scores, accessible to the public.",
        responses={200: PublicLiveScoreSerializer(many=True)},
    )
    def list(self, request):
        """
        Retrieve live scores for ongoing games.
        Accessible to the public (no authentication required).
        """
        # Retrieve ongoing games (i.e., games with status "in-progress")
        live_games = Score.objects.filter(game__status='in_progress')  # Assuming 'in_progress' is a valid status

        # Serialize the data using the PublicLiveScoreSerializer
        serializer = PublicLiveScoreSerializer(live_games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)