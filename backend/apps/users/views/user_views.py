from rest_framework import generics, permissions
from ..models import User
from ..serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer
from ..permissions import IsAdminUser, IsOwnerOrAdmin

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
   
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAdminUser()]
        return [permissions.IsAuthenticated()]
   
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer
    
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsOwnerOrAdmin]
   
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer
    
class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()  # Добавляем queryset
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return self.request.user