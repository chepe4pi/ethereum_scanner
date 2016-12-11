import factory

from app_auth.models import ApiKey, ClientInfo
from app_core.tests.factories import UserFactory
from app_follows.models import Follow, EthAccountInfo


class ClientInfoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ClientInfo

    ip_address = '127.0.0.2'


class ApiKeyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ApiKey

    key = '123'
    client_info = factory.SubFactory(ClientInfoFactory)


class FollowFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    address = '0x42e6723a0c884e922240e56d7b618bec96f35801'
    name = 'test follow name'

    class Meta:
        model = Follow


class EthAccountInfoFactory(factory.django.DjangoModelFactory):
    avatar = factory.django.ImageField()#from_path='app_core/tests/test_file.jpg')
    address = '0x42e6723a0c884e922240e56d7b618bec96f35801'
    name = 'Test Eth Account Name'

    class Meta:
        model = EthAccountInfo
