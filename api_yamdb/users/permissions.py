from rest_framework import permissions
from rest_framework.exceptions import MethodNotAllowed

from .models import ADMIN, USER


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_superuser or request.user.role == ADMIN)
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_superuser or request.user.role == ADMIN)
        )


class IsAuthorOrNotSimpleUserReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user == obj.author
                 or request.user.role != USER
                 or request.user.is_superuser)
        )


class GenreCategoryPermission(IsAdminOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if (request.method != 'DELETE'):
            raise MethodNotAllowed(request.method)
        return (request.method == 'DELETE'
                and request.user.is_authenticated
                and (request.user.role == ADMIN
                     or request.user.is_superuser))
