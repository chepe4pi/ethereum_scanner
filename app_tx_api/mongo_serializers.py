from rest_framework_mongoengine.serializers import DocumentSerializer

from app_sync.mongo_models import EthTransactions


class TxSerializer(DocumentSerializer):
    class Meta:
        model = EthTransactions
