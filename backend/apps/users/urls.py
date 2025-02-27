from django.urls import path
from .views import UserListView, UserDetailView, ProfileView, PasswordChangeView, RolesListView

app_name = 'users'
urlpatterns = [
    path('roles/', RolesListView.as_view(), name='roles-list'),
    path('', UserListView.as_view(), name='user-list'),
    path('<uuid:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', PasswordChangeView.as_view(), name='change-password'),
]