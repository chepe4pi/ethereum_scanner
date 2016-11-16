from drf_mongo_filters import MongoFilterBackend
from rest_framework_mongoengine.viewsets import ReadOnlyModelViewSet

from app_core.mixins_for_view import FilterViewMixin
from app_sync.mongo_models import EthTransactions
from app_tx_api.mongo_serializers import TxSerializer


class GetTxListView(FilterViewMixin, ReadOnlyModelViewSet):
    filter_backends = (MongoFilterBackend,)
    serializer_class = TxSerializer
    queryset = EthTransactions.objects.all()
    lookup_field = 'hash'
    filter_fields = ('hash', 'fromAddress', 'toAddress')
