from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from app_auth.models import ApiKey


class ApiKeySerializer(ModelSerializer):
    class Meta:
        model = ApiKey
        fields = ('key',)


class UserInfoSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'profile_image_url')

    profile_image_url = SerializerMethodField()

    def get_profile_image_url(self, instance):
        if SocialAccount.objects.filter(user=instance).exists():
            return SocialAccount.objects.get(user=instance).get_avatar_url()
