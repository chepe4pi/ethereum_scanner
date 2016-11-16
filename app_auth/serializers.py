from rest_framework.serializers import ModelSerializer

from app_auth.models import ApiKey


class ApiKeySerializer(ModelSerializer):
    class Meta:
        model = ApiKey
        fields = ('key',)