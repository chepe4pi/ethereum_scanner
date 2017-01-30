from django.contrib.auth.models import User
from rest_framework import mixins
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app_auth.models import ApiKey, ClientInfo
from app_auth.serializers import ApiKeySerializer, UserInfoSerializer
from ipware.ip import get_real_ip, get_ip


class ApiKeyViewSet(GenericViewSet,
                    mixins.CreateModelMixin):
    permission_classes = (AllowAny,)
    queryset = ApiKey.objects.all()

    def create(self, request, *args, **kwargs):
        client_info_data = {
            'ip_address': get_real_ip(request) or get_ip(request),
        }
        if request.user.is_authenticated():
            client_info_data.update({'user': request.user})
        if 'HTTP_USER_AGENT' in request.META:
            client_info_data.update({'http_user_agent': request.META['HTTP_USER_AGENT']})

        client_info = ClientInfo.objects.create(**client_info_data)
        api_key = ApiKey.objects.create(client_info_id=client_info.pk)
        return Response(status=status.HTTP_200_OK, data=ApiKeySerializer(api_key).data)


class UserInfoViewSet(GenericViewSet,
                      mixins.ListModelMixin):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.none()
    serializer_class = UserInfoSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.id)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = response.data[0]
        return response
