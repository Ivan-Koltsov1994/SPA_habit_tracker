from users.models import UserRoles
from rest_framework import permissions

class UserPermissionsModerator(permissions.BasePermission):

    message = 'Вы являетесь модератором...'

    def has_permission(self, request, view):
        if request.user.is_staff or request.user.role == UserRoles.MODERATOR or request.user.is_superuser:
            if view.action in ['list',  'retrieve', 'update', 'partial_update', 'destroy','create']:
                return True
        return False

class UserPermissionsOwner(permissions.BasePermission):
    message = 'Вы  вляетесь владельцем...'

    def has_object_permission(self, request, view, obj):
        # Запретить действия над объектами, если пользователь не аутентифицирован
        if not request.user.is_authenticated():
            return False

        if request.user == obj.owner:
            if view.action in ['list',  'retrieve', 'update', 'partial_update', 'destroy','create']:
                return True
        return False