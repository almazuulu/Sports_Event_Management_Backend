from rest_framework import permissions
from users.permissions import IsAdminUser
from teams.models import Player


class IsTeamManagerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow team managers to access their own teams or admins to access any team.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                (request.user.role == 'admin' or request.user.role == 'team_manager'))
    
    def has_object_permission(self, request, view, obj):
        # Allow admin to access any team
        if request.user.is_authenticated and request.user.role == 'admin':
            return True
        
        # Allow team managers to access only their own teams
        return request.user.is_authenticated and request.user.role == 'team_manager' and obj.manager == request.user


class IsTeamOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow only the team's manager or admins to perform actions on a team.
    """
    def has_object_permission(self, request, view, obj):
        # Allow admin to access any team
        if request.user.is_authenticated and request.user.role == 'admin':
            return True
        
        # Allow team managers to access only their own teams
        return request.user.is_authenticated and request.user.role == 'team_manager' and obj.manager == request.user


class IsPlayerTeamManagerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow only the manager of the player's team or admins to modify a player.
    """
    def has_object_permission(self, request, view, obj):
        # Allow admin to access any player
        if request.user.is_authenticated and request.user.role == 'admin':
            return True
        
        # Allow team managers to access only their team's players
        return request.user.is_authenticated and request.user.role == 'team_manager' and obj.team.manager == request.user


class IsRegistrationTeamManagerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow only the team manager who created the registration or admins to access it.
    """
    def has_object_permission(self, request, view, obj):
        # Allow admin to access any registration
        if request.user.is_authenticated and request.user.role == 'admin':
            return True
        
        # Allow team managers to access only their team's registrations
        return request.user.is_authenticated and request.user.role == 'team_manager' and obj.team.manager == request.user


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
    - Team managers can only cancel their own pending registrations
    """
    def has_object_permission(self, request, view, obj):
        # Always allow admins
        if request.user.is_authenticated and request.user.role == 'admin':
            return True
        
        # For team managers
        if request.user.is_authenticated and request.user.role == 'team_manager':
            # Can only access their own team's registrations
            if obj.team.manager != request.user:
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


class IsTeamCaptain(permissions.BasePermission):
    """
    Custom permission to only allow team captains to access the view.
    This is a player who has been designated as a captain.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        # Check if the user is a player who is a captain of any team
        return Player.objects.filter(
            user=request.user, 
            is_captain=True
        ).exists()
        
    def has_object_permission(self, request, view, obj):
        # For team-related objects, check if the user is a captain of this specific team
        team = None
        
        if hasattr(obj, 'team'):
            team = obj.team
        elif hasattr(obj, 'manager'):  # This is a team itself
            team = obj
            
        if team and request.user.is_authenticated:
            return Player.objects.filter(
                user=request.user, 
                team=team,
                is_captain=True
            ).exists()
            
        return False


class IsTeamManagerOrCaptain(permissions.BasePermission):
    """
    Custom permission to allow either team managers or team captains to access resources.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        # Allow team managers
        if request.user.role == 'team_manager':
            return True
            
        # Allow team captains (players who are captains)
        if request.user.role == 'player':
            return Player.objects.filter(
                user=request.user, 
                is_captain=True
            ).exists()
            
        return False
        
    def has_object_permission(self, request, view, obj):
        # Allow admin access
        if request.user.role == 'admin':
            return True
            
        # Get the team from the object
        team = None
        if hasattr(obj, 'team'):
            team = obj.team
        elif hasattr(obj, 'manager'):  # This is a team itself
            team = obj
            
        if not team:
            return False
            
        # Allow team manager access
        if request.user.role == 'team_manager' and team.manager == request.user:
            return True
            
        # Allow team captain access
        if request.user.role == 'player':
            return Player.objects.filter(
                user=request.user, 
                team=team,
                is_captain=True
            ).exists()
            
        return False