from django.urls import path, include
from rest_framework.routers import DefaultRouter
from scores.views import ScoreViewSet, ScoreDetailViewSet, PublicScoreViewSet, TeamScoreViewSet, AdminScoreReportViewSet

app_name = 'scores'
router = DefaultRouter()

router.register(r'scores', ScoreViewSet, basename='score')
router.register(r'score-details', ScoreDetailViewSet, basename='score-detail')
router.register(r'public/scores', PublicScoreViewSet, basename='public-scores')
router.register(r'teams', TeamScoreViewSet, basename='team-scores')


urlpatterns = [
    path('', include(router.urls)),
    path('reports/', AdminScoreReportViewSet.as_view({'get': 'list'}), name='score-reports'),
    path('reports/download/', AdminScoreReportViewSet.as_view({'get': 'download_report'}), name='download-score-report'),

]
