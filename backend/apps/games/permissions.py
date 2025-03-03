from rest_framework import permissions


class CanViewGame(permissions.BasePermission):
    """
    Permission to allow authenticated users to view games.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated


class CanManageGame(permissions.BasePermission):
    """
    Permission to allow only administrators to create, update, or delete games.
    According to section 5 of the SRS, only admins can modify game schedules.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.method in permissions.SAFE_METHODS:
            return True
            
        return request.user.role == 'admin'
        
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
            
        return request.user.role == 'admin'


class CanUpdateGameStatus(permissions.BasePermission):
    """
    Permission to allow admins and assigned scorekeepers to update game status.
    According to section 2.5 of the SRS, scorekeepers can update game status.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
            
        # Admins can always update
        if request.user.role == 'admin':
            return True
            
        # Scorekeepers can only update if they are assigned to this game
        if request.user.role == 'scorekeeper':
            return obj.scorekeeper == request.user
            
        return False


class CanManageGameTeams(permissions.BasePermission):
    """
    Permission to allow administrators to assign teams to games.
    According to section 2.4 of the SRS, teams need to be assigned to games.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        if request.method in permissions.SAFE_METHODS:
            return True
            
        return request.user.role == 'admin'


class CanManageGamePlayers(permissions.BasePermission):
    """
    Permission to allow team captains to manage their team's player selections for games.
    According to section 2.3 of the SRS, team captains can assign players to matches.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
            
        # Admin can always manage
        if request.user.role == 'admin':
            return True
            
        # Team captains can only manage their own teams
        if request.user.role == 'team_captain':
            return obj.game_team.team.captain == request.user
            
        return False