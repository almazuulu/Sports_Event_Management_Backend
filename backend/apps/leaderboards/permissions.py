from rest_framework import permissions


class CanManageLeaderboards(permissions.BasePermission):
    """
    Custom permission to only allow administrators to manage leaderboards.
    """
    def has_permission(self, request, view):
        # Anyone can view (GET) leaderboards
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Only admins can manage leaderboards
        return request.user.is_authenticated and request.user.role == 'admin'