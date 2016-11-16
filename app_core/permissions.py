from rest_framework import permissions

from app_auth.models import ApiKey


class HasApiKeyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        api_key = request.query_params.get('api_key', None)
        if api_key and ApiKey.objects.filter(key=api_key).exists():
            return True
