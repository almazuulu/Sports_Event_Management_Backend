from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Will contain user-related endpoints like:
    # path('profile/', views.ProfileView.as_view(), name='profile'),
    # path('register/', views.RegisterView.as_view(), name='register'),
]