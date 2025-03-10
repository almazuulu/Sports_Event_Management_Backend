from django.urls import path, include
from rest_framework.routers import DefaultRouter
from scores.views import ScoreViewSet, ScoreDetailViewSet, PublicScoreViewSet, PublicLiveScoreViewSet, AdminScoreReportViewSet

app_name = 'scores'
router = DefaultRouter()
router.register(r'', ScoreViewSet, basename='score')
router.register(r'score-detail', ScoreDetailViewSet, basename='score-detail')
router.register(r'public/scores', PublicScoreViewSet, basename='public-scores')

urlpatterns = [
    # Will contain score-related endpoints like:
    # path('', views.ScoreListView.as_view(), name='score-list'),
    # path('<int:game_id>/', views.GameScoreView.as_view(), name='game-score'),
    # path('update/<int:game_id>/', views.UpdateScoreView.as_view(), name='update-score'),
    path('', include(router.urls)),
    path('assign-scorekeeper/<int:pk>/', ScoreViewSet.as_view({'post': 'assign_scorekeeper'}), name='assign-scorekeeper'),
    path('api/public/scores/live/', PublicLiveScoreViewSet.as_view({'get': 'list'}), name='public-live-scores'),
    path('reports/', AdminScoreReportViewSet.as_view({'get': 'list'}), name='score-reports'),
    path('reports/download/', AdminScoreReportViewSet.as_view({'get': 'download_report'}), name='download-score-report'),
]
