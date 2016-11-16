from constance import config
from mongoengine import connect
from rest_framework_mongoengine.viewsets import ReadOnlyModelViewSet

from app_core.mixins_for_view import FilterViewMixin
from app_sync.mongo_models import EthTransactions
from app_tx_api.mongo_serializers import TxSerializer


# TODO I have to find other way
connect(config.MONGO_DATABASE_NAME)


class GetTxListView(FilterViewMixin, ReadOnlyModelViewSet):
    serializer_class = TxSerializer
    queryset = EthTransactions.objects.all()
    lookup_field = 'hash'
    filter_fields = ('hash', 'fromAddress', 'toAddress',
                     'blockNumber', 'blockNumber__gt', 'blockNumber__lt', 'blockNumber__gte', 'blockNumber__lte',
                     'timestamp', 'timestamp__gt', 'timestamp__lt', 'timestamp__gte', 'timestamp__lte')
