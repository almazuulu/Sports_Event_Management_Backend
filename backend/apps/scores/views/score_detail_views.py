from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from ..models import Score, ScoreDetail
from ..serializers import ScoreDetailCreateSerializer, PublicScoreSerializer
from ..permissions import CanManageScores, IsAssignedScorekeeper


class ScoreDetailViewSet(viewsets.GenericViewSet):
    """
    API endpoint for managing score details for a specific game.
    """

    @extend_schema(
        summary="Create a new score detail",
        description="Records a new scoring event during a game (e.g., goal, point).",
        request=ScoreDetailCreateSerializer,
        responses={201: PublicScoreSerializer},
    )
    @permission_classes([IsAuthenticated, CanManageScores | IsAssignedScorekeeper])
    @action(detail=True, methods=['post'], url_path='details')
    def create_score_detail(self, request, pk=None):
        """
        Create a new score detail for a game. This is done when an event such as a goal or point is scored.
        Accessible only by assigned scorekeepers or admins.
        """
        try:
            # Get the score object based on the provided score_id (pk)
            score = Score.objects.get(pk=pk)
        except Score.DoesNotExist:
            return Response({"detail": "Score not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has permission to record score details for this game
        if not request.user.has_perm('app_name.can_manage_scores', score) and score.scorekeeper != request.user:
            return Response({"detail": "You do not have permission to add score details."}, status=status.HTTP_403_FORBIDDEN)

        # Create the score detail
        serializer = ScoreDetailCreateSerializer(data=request.data)
        if serializer.is_valid():
            score_detail = serializer.save(score=score)  # Link the score detail to the score
            score.total_score = score.calculate_total_score()  # You may need to implement this method
            score.save()

            # Return the created score detail and the updated score
            response_serializer = PublicScoreSerializer(score_detail)
            return Response({
                'score_detail': response_serializer.data,
                'updated_score': score.total_score
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="List Score Details",
        description="Retrieve a list of score details for a specific game.",
        responses={200: PublicScoreSerializer(many=True)},
    )
    @permission_classes([IsAuthenticated, CanManageScores | IsAssignedScorekeeper])
    def list_score_details(self, request, pk=None):
        """
        List all score details for a specific game.
        Accessible only by assigned scorekeepers or admins.
        """
        try:
            # Get the score object based on the provided score_id (pk)
            score = Score.objects.get(pk=pk)
        except Score.DoesNotExist:
            return Response({"detail": "Score not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has permission to view score details for this game
        if not request.user.has_perm('app_name.can_manage_scores', score) and score.scorekeeper != request.user:
            return Response({"detail": "You do not have permission to view score details."}, status=status.HTTP_403_FORBIDDEN)

        # Get all score details for the score
        score_details = score.score_details.all()
        serializer = PublicScoreSerializer(score_details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
    summary="Update Score Detail",
    description="Update a specific score detail for a game.",
    request=ScoreDetailCreateSerializer,
    responses={200: PublicScoreSerializer},
    )
    @permission_classes([IsAuthenticated, CanManageScores | IsAssignedScorekeeper])
    @action(detail=True, methods=['put'], url_path='details/(?P<detail_id>[^/.]+)')
    def update_score_detail(self, request, pk=None, detail_id=None):
        """
        Update a specific score detail for a game.
        Accessible only by assigned scorekeepers or admins.
        """
        try:
            # Get the score detail object based on the provided detail_id
            score_detail = ScoreDetail.objects.get(pk=detail_id)
        except ScoreDetail.DoesNotExist:
            return Response({"detail": "Score detail not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has permission to update score details for this game
        if not request.user.has_perm('app_name.can_manage_scores', score_detail.score) and score_detail.score.scorekeeper != request.user:
            return Response({"detail": "You do not have permission to update this score detail."}, status=status.HTTP_403_FORBIDDEN)

        # Update the score detail
        serializer = ScoreDetailCreateSerializer(score_detail, data=request.data)
        if serializer.is_valid():
            score_detail = serializer.save()
            score_detail.score.total_score = score_detail.score.calculate_total_score()  # You may need to implement this method
            score_detail.score.save()

            # Return the updated score detail and the updated score
            response_serializer = PublicScoreSerializer(score_detail)
            return Response({
                'updated_score_detail': response_serializer.data,
                'updated_score': score_detail.score.total_score
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Delete Score Detail",
        description="Delete a specific score detail for a game.",
        responses={204: None},
    )
    @permission_classes([IsAuthenticated, CanManageScores | IsAssignedScorekeeper])
    @action(detail=True, methods=['delete'], url_path='details/(?P<detail_id>[^/.]+)')
    def delete_score_detail(self, request, pk=None, detail_id=None):
        """
        Delete a specific score detail for a game.
        Accessible only by assigned scorekeepers or admins.
        """
        try:
            # Get the score detail object based on the provided detail_id
            score_detail = ScoreDetail.objects.get(pk=detail_id)
        except ScoreDetail.DoesNotExist:
            return Response({"detail": "Score detail not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has permission to delete score details for this game
        if not request.user.has_perm('app_name.can_manage_scores', score_detail.score) and score_detail.score.scorekeeper != request.user:
            return Response({"detail": "You do not have permission to delete this score detail."}, status=status.HTTP_403_FORBIDDEN)

        # Delete the score detail
        score = score_detail.score
        score_detail.delete()
        score.total_score = score.calculate_total_score()  # You may need to implement this method
        score.save()

        return Response(status=status.HTTP_204_NO_CONTENT)