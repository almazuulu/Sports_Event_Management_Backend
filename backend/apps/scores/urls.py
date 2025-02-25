from django.urls import path
from . import views

app_name = 'scores'

urlpatterns = [
    # Will contain score-related endpoints like:
    # path('', views.ScoreListView.as_view(), name='score-list'),
    # path('<int:game_id>/', views.GameScoreView.as_view(), name='game-score'),
    # path('update/<int:game_id>/', views.UpdateScoreView.as_view(), name='update-score'),
]