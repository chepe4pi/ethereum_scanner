from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator

from app_follows.models import Follow, EthAccountInfo


class FollowSerializer(ModelSerializer):
    def validate_address(self, value):
        if len(value.lstrip('0x').lstrip('0X')) == 40:
            return value
        else:
            raise ValidationError("Address is not valid")

    class Meta:
        model = Follow
        fields = ('user', 'address', 'name')
        extra_kwargs = {'user_id': {'write_only': True}}
        read_only_fields = ('created', 'id')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'address')
            )
        ]


class EthAccountInfoSerializer(ModelSerializer):
    class Meta:
        model = EthAccountInfo
        fields = ('avatar', 'name')
