from rest_framework.filters import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from app_follows.filter_backends import FollowsFilterBackend
from app_follows.models import Follow, EthAccountInfo
from app_follows.permissions import IsOwner
from app_follows.serializers import FollowSerializer, EthAccountInfoSerializer


class FollowViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwner)
    queryset = Follow.objects.all()
    filter_backends = (FollowsFilterBackend,)
    serializer_class = FollowSerializer
    lookup_field = 'address'

    def create(self, request, *args, **kwargs):
        request.data.update({"user": request.user.pk})
        return super().create(request, *args, **kwargs)


class EthAccountInfoViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = EthAccountInfo.objects.all()
    serializer_class = EthAccountInfoSerializer
    lookup_field = 'address'
