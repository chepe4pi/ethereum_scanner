from rest_framework_mongoengine.viewsets import ReadOnlyModelViewSet

from app_core.mixins_for_view import FilterViewMixin
from app_core.permissions import HasApiKeyPermission
from app_sync.mongo_models import EthTransactions
from app_tx_api.mongo_serializers import TxSerializer


class GetTxListView(FilterViewMixin, ReadOnlyModelViewSet):
    serializer_class = TxSerializer
    permission_classes = (HasApiKeyPermission,)
    queryset = EthTransactions.objects.all()
    lookup_field = 'hash'
    filter_fields = ('hash', 'fromAddress', 'toAddress',
                     'blockNumber', 'blockNumber__gt', 'blockNumber__lt', 'blockNumber__gte', 'blockNumber__lte',
                     'timestamp', 'timestamp__gt', 'timestamp__lt', 'timestamp__gte', 'timestamp__lte')
