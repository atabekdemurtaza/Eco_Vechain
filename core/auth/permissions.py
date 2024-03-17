from rest_framework.permissions import BasePermission, SAFE_METHODS


class UserPermissions(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS

        if view.basename in ["user"]:
            if request.method in SAFE_METHODS:
                return True
            return bool(request.user.id == obj.id)

        return False

    def has_permission(self, request, view):
        if view.basename in ["user", "auth-logout"]:
            if request.user.is_anonymous:
                return request.method in SAFE_METHODS
            return bool(
                request.user and request.user.is_authenticated
            )
        return False
