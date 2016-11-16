from rest_framework.fields import SerializerMethodField
from rest_framework_mongoengine.serializers import DocumentSerializer

from app_sync.mongo_models import EthTransactions


class TxSerializer(DocumentSerializer):
    value = SerializerMethodField()

    def get_value(self, instance):
        return int(instance.value)

    class Meta:
        model = EthTransactions
        fields = (
        'fromAddress', 'toAddress', 'input', 'hash', 'nonce', 'value', 'gas', 'gasPrice', 'blockNumber', 'timestamp')
