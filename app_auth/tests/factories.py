import factory

from app_auth.models import ApiKey, ClientInfo


class ClientInfoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ClientInfo

    ip_address = '127.0.0.2'


class ApiKeyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ApiKey

    key = '123'
    client_info = factory.SubFactory(ClientInfoFactory)
