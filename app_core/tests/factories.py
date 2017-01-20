import factory
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = 'test_username'
    first_name = 'Mr.'
    last_name = 'Minister'
    email = 'test@email.example.com'
    password = '123'
