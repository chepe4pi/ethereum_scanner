from rest_framework.serializers import ModelSerializer

from app_follows.models import Follow, EthAccountInfo


class FollowSerializer(ModelSerializer):
    class Meta:
        model = Follow
        fields = ('user', 'address', 'name')
        extra_kwargs = {'user_id': {'write_only': True}}
        read_only_fields = ('created', 'id')


class EthAccountInfoSerializer(ModelSerializer):
    class Meta:
        model = EthAccountInfo
        fields = ('avatar', 'name')
