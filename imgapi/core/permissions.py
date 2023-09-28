from rest_framework.permissions import BasePermission
from .models import User

class ExpiringLinkAllowed(BasePermission):
    """Permission for admin, enterprise or custom users"""
    def has_permission(self, request, view):
        return request.user.is_superuser or (request.user.is_authenticated and request.user.custom_temp_link) or (request.user.is_authenticated and request.user.user_tier == User.ENTERPRISE)