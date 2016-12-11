from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    message = 'Access to object not allowed.'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
