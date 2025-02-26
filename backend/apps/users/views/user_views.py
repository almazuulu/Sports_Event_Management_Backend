from rest_framework import generics, permissions
from ..models import User
from ..serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer
from ..permissions import IsAdminUser, IsOwnerOrAdmin


class UserListView(generics.ListCreateAPIView):
    """
    API endpoint for listing all users and creating new users.
    """
    queryset = User.objects.all()
   
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAdminUser()]
        return [permissions.IsAuthenticated()]
   
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer
    
    def list(self, request, *args, **kwargs):
        """
        List all users in the system.
        
        Returns a paginated list of all user accounts.
        Note: Only administrators can access this endpoint.
        """
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """
        Create a new user account.
        
        Allows creation of a new user with specified role, name, email and password.
        Requires authentication to access this endpoint.
        """
        return super().create(request, *args, **kwargs)
   
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting specific users.
    Only administrators or the account owner can access this endpoint.
    """
    queryset = User.objects.all()
    permission_classes = [IsOwnerOrAdmin]
   
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve details of a specific user.
        
        Returns the complete user profile for the specified user ID.
        Only accessible by administrators or the account owner.
        """
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """
        Completely update a specific user.
        
        Updates all fields of the specified user account.
        Requires all mandatory fields to be provided.
        Only accessible by administrators or the account owner.
        """
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a specific user.
        
        Updates only the provided fields of the specified user account.
        Only accessible by administrators or the account owner.
        """
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a specific user.
        
        Permanently removes the specified user account from the system.
        Only accessible by administrators or the account owner.
        """
        return super().destroy(request, *args, **kwargs)
    
class ProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for managing the current user's profile.
    Requires authentication.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """
        Returns the current authenticated user.
        """
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve the current user's profile information.
        
        Returns complete profile information of the current authenticated user,
        including ID, email, first name, last name, and role.
        """
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """
        Full update of the current user's profile.
        
        Allows updating profile data, requires all mandatory fields to be provided.
        """
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """
        Partial update of the current user's profile.
        
        Allows updating individual profile fields without sending all data.
        """
        return super().partial_update(request, *args, **kwargs)