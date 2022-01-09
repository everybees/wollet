from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, BasePermission


class ActionBasedPermission(AllowAny):
    """
    Grant or deny access to a view, based on a mapping in view.action_permissions
    """

    def has_permission(self, request, view):
        for klass, actions in getattr(view, 'action_permissions', {}).items():
            if view.action in actions:
                return klass().has_permission(request, view)
            elif view.action is None:
                return True  # This handles 'OPTIONS' HTTP methods
        return False


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.auth is None:
            return False
        token = Token.objects.get(key=request.auth.key)
        is_admin = token.user.user_type == "admin"
        return bool(is_admin)


class IsElite(BasePermission):
    def has_permission(self, request, view):
        if request.auth is None:
            return False
        token = Token.objects.get(key=request.auth.key)
        is_elite = token.user.user_type == 'elite'
        return bool(is_elite)
