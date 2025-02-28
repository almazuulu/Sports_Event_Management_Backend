from rest_framework import permissions
from users.permissions import IsAdminUser, IsTeamCaptain


class IsTeamCaptainOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow team captains to access their own teams or admins to access any team.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                (request.user.role == 'admin' or request.user.role == 'team_captain'))
    
    def has_object_permission(self, request, view, obj):
        # Allow admin to access any team
        if request.user.is_authenticated and request.user.role == 'admin':
            return True
        
        # Allow team captains to access only their own teams
        return request.user.is_authenticated and request.user.role == 'team_captain' and obj.captain == request.user


class IsTeamOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow only the team's captain or admins to perform actions on a team.
    """
    def has_object_permission(self, request, view, obj):
        # Allow admin to access any team
        if request.user.is_authenticated and request.user.role == 'admin':
            return True
        
        # Allow team captains to access only their own teams
        return request.user.is_authenticated and request.user.role == 'team_captain' and obj.captain == request.user


class IsPlayerTeamCaptainOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow only the captain of the player's team or admins to modify a player.
    """
    def has_object_permission(self, request, view, obj):
        # Allow admin to access any player
        if request.user.is_authenticated and request.user.role == 'admin':
            return True
        
        # Allow team captains to access only their team's players
        return request.user.is_authenticated and request.user.role == 'team_captain' and obj.team.captain == request.user


class IsRegistrationTeamCaptainOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow only the team captain who created the registration or admins to access it.
    """
    def has_object_permission(self, request, view, obj):
        # Allow admin to access any registration
        if request.user.is_authenticated and request.user.role == 'admin':
            return True
        
        # Allow team captains to access only their team's registrations
        return request.user.is_authenticated and request.user.role == 'team_captain' and obj.team.captain == request.user


class IsTeamMember(permissions.BasePermission):
    """
    Custom permission to allow any member of a team to access team resources.
    Useful for read-only access to team data.
    """
    def has_object_permission(self, request, view, obj):
        # For non-safe methods (POST, PUT, DELETE), use stricter permissions
        if request.method not in permissions.SAFE_METHODS:
            return False
        
        # For safe methods (GET, HEAD, OPTIONS), check if user is a member of the team
        return (request.user.is_authenticated and 
                hasattr(request.user, 'player_profiles') and 
                request.user.player_profiles.filter(team=obj, is_active=True).exists())


class CanManageRegistration(permissions.BasePermission):
    """
    Custom permission for registration management:
    - Admins can approve/reject registrations
    - Team captains can only cancel their own pending registrations
    """
    def has_object_permission(self, request, view, obj):
        # Always allow admins
        if request.user.is_authenticated and request.user.role == 'admin':
            return True
        
        # For team captains
        if request.user.is_authenticated and request.user.role == 'team_captain':
            # Can only access their own team's registrations
            if obj.team.captain != request.user:
                return False
            
            # For DELETE requests (cancellation), can only cancel pending registrations
            if request.method == 'DELETE':
                return obj.status == 'pending'
            
            # For other methods, can only view
            return request.method in permissions.SAFE_METHODS
        
        return False


class PublicReadOnly(permissions.BasePermission):
    """
    Custom permission to allow anyone to read public endpoints,
    but only authenticated users can make changes.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated