from rest_framework import permissions


class IsUserProfile(permissions.BasePermission):
    # Запретить действия над объектами, если пользователь не аутентифицирован

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated():
            return False

        if request.user.email == obj.email:
            if view.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy', 'create']:
                return True
        return False
