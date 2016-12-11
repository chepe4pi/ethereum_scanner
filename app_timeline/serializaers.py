from rest_framework.fields import SerializerMethodField
from rest_framework_mongoengine.serializers import DocumentSerializer

from app_follows.models import Follow, EthAccountInfo
from app_sync.mongo_models import EthTransactions


class TimelineSerializer(DocumentSerializer):
    def __init__(self, *args, **kwargs):
        self.sent_value = None
        self.address2_value = None
        self.address_value = None
        super().__init__(*args, **kwargs)

    amount_in_wei = SerializerMethodField()
    address = SerializerMethodField()
    address2 = SerializerMethodField()
    address_name = SerializerMethodField()
    address_avatar = SerializerMethodField()
    sent = SerializerMethodField()

    def get_amount_in_wei(self, instance):
        return int(instance.value)

    def get_address(self, instance):
        users_follows_list = Follow.objects.filter(user=self.context['request'].user).values_list('address', flat=True)
        if instance.fromAddress in users_follows_list:
            self.sent_value = True
            self.address_value = instance.fromAddress
            self.address2_value = instance.toAddress
            return instance.fromAddress
        if instance.toAddress in users_follows_list:
            self.sent_value = False
            self.address_value = instance.toAddress
            self.address2_value = instance.fromAddress
            return instance.toAddress

    def get_address_name(self, instance):
        account_info = self._get_account_info()
        if account_info:
            return account_info.name

    def get_address_avatar(self, instance):
        account_info = self._get_account_info()
        if account_info:
            return account_info.avatar.url

    def _get_account_info(self):
        if EthAccountInfo.objects.filter(address=self.address_value).exists():
            return EthAccountInfo.objects.filter(address=self.address_value)[0]

    def get_address2(self, instance):
        return self.address2_value

    def get_sent(self, instance):
        return self.sent_value

    class Meta:
        model = EthTransactions
        fields = ('timestamp', 'amount_in_wei', 'address', 'address2', 'address_name', 'address_avatar', 'sent')
