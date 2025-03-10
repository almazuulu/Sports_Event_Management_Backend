from rest_framework import status, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from scores.models import Score
from scores.serializers import PublicScoreSerializer, ScoreCreateSerializer, ScoreUpdateSerializer, ScoreSerializer, ScoreVerificationSerializer
from scores.permissions import CanManageScores, IsAssignedScorekeeper, CanVerifyScores
from games.models import Game
from django.utils import timezone
from rest_framework.decorators import action, permission_classes
from drf_spectacular.utils import OpenApiParameter
from users.models import User


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = PublicScoreSerializer
    """
    API endpoint for Score management (creating and updating scores).
    """

    @extend_schema(
        summary="Create a new game score",
        description="Creates a new score record for a game. This is typically automated when a game is created.",
        request=ScoreCreateSerializer,
        responses={201: PublicScoreSerializer},
    )
    def create(self, request):
        """
        Create a new score record for a game. This is typically done when a game is created.
        Only accessible by admin users.
        """
        self.check_permissions(request)

        serializer = ScoreCreateSerializer(data=request.data)
        if serializer.is_valid():
            score = serializer.save()

            response_serializer = PublicScoreSerializer(score)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Update a game score",
        description="Updates a specific game score record. Only accessible by assigned scorekeepers and admin.",
        request=ScoreUpdateSerializer,
        responses={200: PublicScoreSerializer},
    )
    @permission_classes([CanManageScores, IsAssignedScorekeeper])
    def update(self, request, pk=None):
        """
        Update a specific score record.
        """
        self.check_permissions(request)
        score = Score.objects.get(pk=pk)

        serializer = ScoreUpdateSerializer(score, data=request.data)
        if serializer.is_valid():
            score = serializer.save()

            response_serializer = PublicScoreSerializer(score)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Get game score details",
        description="Returns the details of a specific score record.",
        responses={200: ScoreSerializer},
    )
    def retrieve(self, request, pk=None):
        """
        Retrieve the details of a specific score record.
        """
        score = Score.objects.get(pk=pk)

        serializer = PublicScoreSerializer(score)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="List all game score records",
        description="Get a list of all score records with optional filters.",
        responses={200: PublicScoreSerializer(many=True)},
        parameters=[
            OpenApiParameter(name="sport_type", description="Filter by sport type", required=False, type=str),
            OpenApiParameter(name="event", description="Filter by event", required=False, type=str),
            OpenApiParameter(name="status", description="Filter by status", required=False, type=str),
            OpenApiParameter(name="ordering", description="Order by field (e.g. status, -status)", required=False, type=str)
        ]
    )
    def list(self, request):
        """
        List all score records with filtering options by sport type, event, status, etc.
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
        summary="Delete a game score",
        description="Deletes a specific score record.",
        responses={204: None},
    )
    def destroy(self, request, pk=None):
        """
        Delete a specific score record.
        """
        self.check_permissions(request)
        score = Score.objects.get(pk=pk)
        score.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        summary="Verify a game score",
        description="Verifies a score record. Only accessible by admin users.",
        request = ScoreVerificationSerializer,
        responses={200: PublicScoreSerializer},
    )
    @action(detail=True, methods=['patch'], permission_classes=[CanVerifyScores])

    def verify(self, request, pk=None):
        """
        Verify a score record.
        """
        self.check_permissions(request)
        score = Score.objects.get(pk=pk)

        score.verified_by = request.user
        score.verified_at = timezone.now()
        score.save()

        serializer = PublicScoreSerializer(score)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
        summary="Assign a scorekeeper to a game",
        description="Assigns a scorekeeper user to a specific game. This action can only be performed by admin users.",
        request=PublicScoreSerializer,
        responses={200: PublicScoreSerializer},
    )
    @permission_classes([IsAdminUser])
    @action(detail=True, methods=['post'], url_path='assign-scorekeeper')
    def assign_scorekeeper(self, request, pk=None):
        """
        Assign a scorekeeper to a specific game.
        Only accessible by admin users.
        """
        try:
            # Get the score object based on the provided score_id (pk)
            score = Score.objects.get(pk=pk)
        except Score.DoesNotExist:
            return Response({"detail": "Score not found."}, status=status.HTTP_404_NOT_FOUND)

        # Get the scorekeeper user ID from the request body
        scorekeeper_id = request.data.get('scorekeeper_id')
        if not scorekeeper_id:
            return Response({"detail": "Scorekeeper ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get the user object based on the scorekeeper_id
            scorekeeper = User.objects.get(id=scorekeeper_id)
        except User.DoesNotExist:
            return Response({"detail": "Scorekeeper not found."}, status=status.HTTP_404_NOT_FOUND)

        # Assign the scorekeeper to the score
        score.scorekeeper = scorekeeper
        score.save()

        # Return the updated score object with the assigned scorekeeper
        serializer = PublicScoreSerializer(score)
        return Response(serializer.data, status=status.HTTP_200_OK)
