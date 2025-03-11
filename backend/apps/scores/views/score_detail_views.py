from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from ..models import ScoreDetail
from ..serializers import ScoreDetailSerializer, ScoreDetailCreateSerializer
from ..permissions import IsAssignedScorekeeper, CanManageScores

class ScoreDetailViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing score details for a game.
    """
    queryset = ScoreDetail.objects.all()
    permission_classes = [permissions.IsAuthenticated]  # Default permission, will be further customized
    
    def get_permissions(self):
        """
        Customizing permission for different actions
        """
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['create', 'update', 'destroy']:
            self.permission_classes = [IsAssignedScorekeeper | CanManageScores]  # Custom permissions for modifying score details
        return super().get_permissions()

    @extend_schema(
        description="Lists all score details for a game, ordered by time. Admin users have full access, Team captains can only view scores for their teams, Public users see limited information",
        summary="List all score details for a game.",
        responses={200: ScoreDetailSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        score_id = kwargs.get('score_id')
        queryset = self.get_queryset().filter(score__id=score_id).order_by('time')  # Filter by game ID
        serializer = ScoreDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        description="Creates a new score detail (e.g., goal, point) during a game. Assigned Scorekeepers or Admin users can create new score details.",
        summary='Create a new score detail for a game.',
        request=ScoreDetailCreateSerializer,
        responses={201: ScoreDetailSerializer},
    )
    def create(self, request, *args, **kwargs):
        score_id = kwargs.get('score_id')
        serializer = ScoreDetailCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(score_id=score_id)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @extend_schema(
        description="Retrieves detailed information about a specific scoring event.",
        summary="Retrieve a specific score detail.",
        responses={200: ScoreDetailSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        score_id = kwargs.get('score_id')
        detail_id = kwargs.get('pk')
        queryset = self.get_queryset().filter(score__id=score_id)
        score_detail = queryset.get(id=detail_id)
        serializer = ScoreDetailSerializer(score_detail)
        return Response(serializer.data)

    @extend_schema(
        description="Updates a specific scoring event for a game (e.g., correcting points). Assigned Scorekeepers or Admin users can update score details.",
        summary="Update a specific score detail.",
        request=ScoreDetailCreateSerializer,
        responses={200: ScoreDetailSerializer},
    )
    def update(self, request, *args, **kwargs):
        score_id = kwargs.get('score_id')
        detail_id = kwargs.get('pk')
        queryset = self.get_queryset().filter(score__id=score_id)
        score_detail = queryset.get(id=detail_id)
        serializer = ScoreDetailCreateSerializer(score_detail, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @extend_schema(
        description="Deletes a specific scoring event from the game. Assigned Scorekeepers or Admin users can delete score details.",
        summary="Delete a specific score detail.",
        responses={204: None},
    )
    def destroy(self, request, *args, **kwargs):
        score_id = kwargs.get('score_id')
        detail_id = kwargs.get('pk')
        queryset = self.get_queryset().filter(score__id=score_id)
        score_detail = queryset.get(id=detail_id)
        score_detail.delete()
        return Response(status=204)
