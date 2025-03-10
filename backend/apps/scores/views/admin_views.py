# views/admin_views.py

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from drf_spectacular.utils import extend_schema
from django.http import HttpResponse
from rest_framework.decorators import action, permission_classes
import csv
from ..models import Score
from ..serializers import PublicScoreSerializer

class AdminScoreReportViewSet(viewsets.ViewSet):
    """
    API endpoint for generating score reports. Accessible only by admin users.
    """

    @extend_schema(
        summary="Generate Score Reports",
        description="Generate a report on game scores, accessible only to admin users. Can potentially include export functionality.",
        responses={200: PublicScoreSerializer(many=True)},
    )
    @permission_classes([IsAdminUser])
    def list(self, request):
        """
        Generate a report on all scores.
        This could later be expanded to include CSV/Excel export functionality.
        """
        scores = Score.objects.all()

        # You can modify this report generation logic based on requirements
        # For this example, we just return the scores in a JSON response.
        serializer = PublicScoreSerializer(scores, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Download Score Report as CSV",
        description="Download the score report in CSV format. Accessible only by admin users.",
    )
    @permission_classes([IsAdminUser])
    @action(detail=False, methods=['get'], url_path='download')
    def download_report(self, request):
        """
        Generate a CSV export of game scores for administrative use.
        Only accessible by admin users.
        """
        scores = Score.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="score_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Score ID', 'Game Name', 'Sport Type', 'Total Score', 'Scorekeeper'])

        for score in scores:
            writer.writerow([score.id, score.game.name, score.game.sport_type, score.total_score, score.scorekeeper.username])

        return response
