from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users to access the view.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow object owners or admins to access it.
    """
    def has_permission(self, request, view):
        # Check basic authentication
        return request.user and request.user.is_authenticated
   
    def has_object_permission(self, request, view, obj):
        # Allow administrators to access any user
        if request.user.is_authenticated and request.user.role == 'admin':
            return True
       
        # Users can only access their own resources
        return obj == request.user


class IsTeamManager(permissions.BasePermission):
    """
    Custom permission to only allow team managers to access the view.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'team_manager'


class IsPlayer(permissions.BasePermission):
    """
    Custom permission to only allow players to access the view.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'player'


class IsTeamCaptain(permissions.BasePermission):
    """
    Custom permission to only allow team captains to access the view.
    This is a player who is designated as captain of a team.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        # Check if user is a player
        if request.user.role != 'player':
            return False
            
        # Check if the player is a captain of any team
        from teams.models import Player
        return Player.objects.filter(
            user=request.user, 
            is_captain=True
        ).exists()


class IsTeamManagerOrCaptain(permissions.BasePermission):
    """
    Custom permission to only allow team managers or team captains to access the view.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        # Allow team managers
        if request.user.role == 'team_manager':
            return True
            
        # Allow team captains (players who are captains)
        if request.user.role == 'player':
            from teams.models import Player
            return Player.objects.filter(
                user=request.user, 
                is_captain=True
            ).exists()
            
        return False


class IsScorekeeper(permissions.BasePermission):
    """
    Custom permission to only allow scorekeepers to access the view.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'scorekeeper'