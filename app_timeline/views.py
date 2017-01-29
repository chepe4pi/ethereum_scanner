from mongoengine import Q
from rest_framework import mixins
from rest_framework_mongoengine.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated

from app_core.mixins_for_view import FilterPaginatorViewMixin
from app_follows.models import Follow
from app_sync.mongo_models import EthTransactions
from app_timeline.serializaers import TimelineSerializer


class TimeLineViewSet(FilterPaginatorViewMixin, mixins.ListModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TimelineSerializer

    def get_queryset(self):
        q_list = []
        users_folows_list = Follow.objects.filter(user=self.request.user)
        for follow in users_folows_list:
            q_list.append(Q(fromAddress=follow.address, timestamp__gte=follow.created.timestamp()))
            q_list.append(Q(toAddress=follow.address, timestamp__gte=follow.created.timestamp()))
        if q_list:
            query = q_list.pop()
            for item in q_list:
                query |= item
            return EthTransactions.objects.filter(query)
        return EthTransactions.objects.none()
