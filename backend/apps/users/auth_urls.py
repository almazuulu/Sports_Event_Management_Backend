from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .serializers.auth_serializers import CustomTokenObtainPairView

app_name = 'auth'

urlpatterns = [
    path('', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
]