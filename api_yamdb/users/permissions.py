from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied




class CategoryGenreTitlePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        # if ((request.method in permissions.SAFE_METHODS)
        #     or (request.user.role == 'admin')
        #     or (request.user.is_superuser)):
        if (request.user.is_authenticated):
            return True
        raise PermissionDenied('Отказано в доступе')

    def has_object_permission(self, request, view, obj):
        if ((request.user.role == 'admin')
            or (request.user.is_superuser)):
            return True
        raise PermissionDenied('Удалять категории, жанры и тайтлы могут только админы')

class ReviewPermission(permissions.BasePermission):
    ALLOWED_ROLES = ['admin', 'moderator']
    def has_permission(self, request, view):
        return bool((request.method in permissions.SAFE_METHODS)
                    or (request.user.is_authenticatd))

    def has_obect_permission(self, request, view, obj):
        if ((request.method in permissions.SAFE_METHODS)
           or (obj.author == request.user)
           or (request.user.role in self.ALLOWED_ROLES)
           or (request.user.is_superuser)):
            return True
        raise PermissionDenied('Нельзя изменять или удалять чужие оценки и комментарии')

class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool((request.user.role is 'admin')
                    or (request.user.is_superuser))
    

class CommentPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool((request.method in permissions.SAFE_METHODS)
                    or (request.user and request.user.is_authenticated))

    def has_object_permission(self, request, view, obj):
        if ((request.method in permissions.SAFE_METHODS)
            or (obj.author == request.user)
            or (request.user.role in self.ALLOWED_ROLES)
            or (request.user.is_superuser)):
            return True
        raise PermissionDenied('Нельзя изменять или удалять чужой контент')
