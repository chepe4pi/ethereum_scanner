from drf_mongo_filters import ModelFilterset

from app_sync.mongo_models import EthTransactions


class TxFilterSet(ModelFilterset):
    class Meta:
        model = EthTransactions
