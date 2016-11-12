from drf_mongo_filters import MongoFilterBackend
from rest_framework_mongoengine.generics import ListAPIView

from app_sync.mongo_models import EthTransactions
from app_tx_api.mongo_filters import TxFilterSet
from app_tx_api.mongo_serializers import TxSerializer


class GetTxListView(ListAPIView):
    filter_backends = (MongoFilterBackend,)
    filter_class = TxFilterSet
    serializer_class = TxSerializer
    queryset = EthTransactions.objects