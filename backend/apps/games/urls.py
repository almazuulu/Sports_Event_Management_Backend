from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    # Will contain game-related endpoints like:
    # path('', views.GameListView.as_view(), name='game-list'),
    # path('<int:pk>/', views.GameDetailView.as_view(), name='game-detail'),
    # path('schedule/', views.ScheduleView.as_view(), name='schedule'),
]