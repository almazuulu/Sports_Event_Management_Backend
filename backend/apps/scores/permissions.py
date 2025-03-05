from rest_framework import permissions


class IsScorekeeper(permissions.BasePermission):
    """
    Custom permission to only allow scorekeepers to update scores.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'scorekeeper'


class IsAssignedScorekeeper(permissions.BasePermission):
    """
    Custom permission to only allow the assigned scorekeeper to update the score.
    """
    def has_object_permission(self, request, view, obj):
        # Allow if user is the assigned scorekeeper for this score
        return (request.user.is_authenticated and 
                request.user.role == 'scorekeeper' and 
                obj.scorekeeper == request.user)


class CanManageScores(permissions.BasePermission):
    """
    Custom permission to allow both assigned scorekeepers and admins to manage scores.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ['admin', 'scorekeeper']
        
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
            
        # Admins can always manage scores
        if request.user.role == 'admin':
            return True
            
        # Scorekeepers can only manage scores they're assigned to
        if request.user.role == 'scorekeeper':
            return obj.scorekeeper == request.user
            
        return False


class CanVerifyScores(permissions.BasePermission):
    """
    Custom permission to only allow administrators to verify scores.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'