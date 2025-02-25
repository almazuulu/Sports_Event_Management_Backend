from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users to access the view.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to access it.
    """
    def has_object_permission(self, request, view, obj):
        # Allow admin to access any user
        if request.user.is_authenticated and request.user.role == 'admin':
            return True
        
        # Allow users to access their own resources
        return obj == request.user

class IsTeamCaptain(permissions.BasePermission):
    """
    Custom permission to only allow team captains to access the view.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'team_captain'

class IsScorekeeper(permissions.BasePermission):
    """
    Custom permission to only allow scorekeepers to access the view.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'scorekeeper'