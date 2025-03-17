from rest_framework import generics, permissions, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from django_filters.rest_framework import DjangoFilterBackend

from ..models import User
from ..serializers import (
    UserSerializer, 
    UserCreateSerializer, 
    UserUpdateSerializer, 
    ProfileSerializer, 
    RoleSerializer
    )
from ..permissions import IsAdminUser, IsOwnerOrAdmin


class UserListView(generics.ListCreateAPIView):
    """
    API endpoint for listing all users and creating new users.
    """
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['email', 'first_name', 'last_name', 'username', 'role']
    search_fields = ['email', 'first_name', 'last_name', 'username']
    ordering_fields = ['email', 'first_name', 'last_name', 'username', 'date_joined']
   
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAdminUser()]
        elif self.request.method == 'POST':
            return []
        return [permissions.IsAuthenticated()]
   
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer
    
    @extend_schema(
        summary="List users",
        description="Get a list of all users in the system. Admin only.",
        parameters=[
            OpenApiParameter(name="email", description="Filter by email", required=False, type=str, location=OpenApiParameter.QUERY),
            OpenApiParameter(name="first_name", description="Filter by first name", required=False, type=str, location=OpenApiParameter.QUERY),
            OpenApiParameter(name="last_name", description="Filter by last name", required=False, type=str, location=OpenApiParameter.QUERY),
            OpenApiParameter(name="username", description="Filter by username", required=False, type=str, location=OpenApiParameter.QUERY),
            OpenApiParameter(name="role", description="Filter by role (admin, team_manager, player, scorekeeper, public)", required=False, type=str, location=OpenApiParameter.QUERY),
            OpenApiParameter(name="search", description="Search in email, first name, last name, and username", required=False, type=str, location=OpenApiParameter.QUERY),
            OpenApiParameter(name="ordering", description="Order by field (e.g. email, first_name, -date_joined)", required=False, type=str, location=OpenApiParameter.QUERY),
        ]
    )
    def list(self, request, *args, **kwargs):
        """
        List all users in the system.
        
        Returns a paginated list of all user accounts.
        Supports filtering by email, name, username, and role.
        Note: Only administrators can access this endpoint.
        """
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Create user",
        description="Create a new user account."
    )
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
    
    @extend_schema(
        summary="Retrieve user",
        description="Get information about a specific user."
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve details of a specific user.
        
        Returns the complete user profile for the specified user ID.
        Only accessible by administrators or the account owner.
        """
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary="Full user update",
        description="Completely update a specific user."
    )
    def update(self, request, *args, **kwargs):
        """
        Completely update a specific user.
        
        Updates all fields of the specified user account.
        Requires all mandatory fields to be provided.
        Only accessible by administrators or the account owner.
        """
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Partial user update",
        description="Partially update a specific user."
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a specific user.
        
        Updates only the provided fields of the specified user account.
        Only accessible by administrators or the account owner.
        """
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Delete user",
        description="Delete a specific user."
    )
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
    Authentication required.
    """
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """
        Returns the current authenticated user.
        """
        return self.request.user
    
    @extend_schema(
        summary="Get current user profile",
        description="Returns complete profile information of the current authenticated user."
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve the current user's profile information.
        
        Returns complete profile information of the current authenticated user,
        including ID, email, username, first name, last name, and role.
        """
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary="Full profile update",
        description="Updates all fields of the current user's profile."
    )
    def update(self, request, *args, **kwargs):
        """
        Full update of the current user's profile.
        
        Allows updating profile data, requires all mandatory fields to be provided.
        """
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Partial profile update",
        description="Updates only the specified fields of the current user's profile."
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Partial update of the current user's profile.
        
        Allows updating individual profile fields without sending all data.
        """
        return super().partial_update(request, *args, **kwargs)
    
    
class RolesListView(APIView):
    """
    API endpoint for listing all available user roles in the system.
    Only administrators can access this endpoint.
    """
    permission_classes = [IsAdminUser]
    
    @extend_schema(
        description="Returns all available user roles with descriptions. Only accessible by administrators.",
        responses={
            200: OpenApiResponse(
                response=RoleSerializer(many=True),
                description="List of roles with their descriptions"
            ),
            403: OpenApiResponse(
                description="Permission denied. Only administrators can access this endpoint."
            )
        }
    )
    def get(self, request):
        """
        Get a list of all available user roles in the system.
        
        Returns detailed information about each role including:
        - Role ID (used in API requests)
        - Display name
        - Description
        
        Note: Only administrators can access this endpoint.
        """
        # Get the role choices from the User model
        role_choices = User.ROLE_CHOICES
        
        # Create a detailed role list
        roles_info = []
        for role_id, role_name in role_choices:
            # Add descriptions for each role
            description = ""
            if role_id == "admin":
                description = "Full system access with all permissions"
            elif role_id == "team_manager":
                description = "Manager responsible for team operations and management"
            elif role_id == "player":
                description = "Player registered in a team"
            elif role_id == "scorekeeper":
                description = "User responsible for recording scores and match results"
            elif role_id == "public":
                description = "Regular user with basic access to the system"
            
            roles_info.append({
                "id": role_id,
                "name": role_name,
                "description": description
            })
        
        # Serialize the roles
        serializer = RoleSerializer(roles_info, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)