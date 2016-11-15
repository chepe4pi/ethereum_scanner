from rest_framework.fields import SerializerMethodField, CharField
from rest_framework_mongoengine.serializers import DocumentSerializer

from app_sync.mongo_models import EthTransactions, EthBlocks


class TxSerializer(DocumentSerializer):
    value = SerializerMethodField()
    timestamp = SerializerMethodField()

    def get_value(self, instance):
        return int(instance.value)

    def get_timestamp(self, instance):
        block = EthBlocks.objects(number=instance.block.number)[0]
        return block.timestamp

    class Meta:
        model = EthTransactions
        fields = (
        'fromAddress', 'toAddress', 'input', 'hash', 'nonce', 'value', 'gas', 'gasPrice', 'blockNumber', 'timestamp')


class BlockSerializer(DocumentSerializer):
    value = SerializerMethodField()

    def get_value(self, instance):
        return int(instance.value)

    class Meta:
        model = EthBlocks
        fields = ('fromAddress', 'toAddress', 'input', 'hash', 'nonce', 'value', 'gas', 'gasPrice', 'blockNumber')
