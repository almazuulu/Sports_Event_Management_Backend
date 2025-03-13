from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .views import ScoreViewSet, ScoreDetailViewSet

# Main router for scores
router = DefaultRouter()
router.register(r'scores', ScoreViewSet, basename='score')
router.register(r'score-details', ScoreDetailViewSet, basename='score-detail')

# Nested router for score details within a score
score_details_router = NestedSimpleRouter(router, r'scores', lookup='score')
score_details_router.register(r'details', ScoreDetailViewSet, basename='score-score-detail')

app_name = 'scores'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(score_details_router.urls)),
]