from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models import ImageField

from ethereum_scanner.settings import MEDIA_ROOT

storage = FileSystemStorage(location=MEDIA_ROOT)


class EthAccountInfo(models.Model):
    address = models.CharField(max_length=63)
    name = models.CharField(max_length=255)
    avatar = ImageField(storage=storage, null=True)


class Follow(models.Model):
    user = models.ForeignKey(User, related_name='follows')
    address = models.CharField(max_length=63, db_index=True)
    name = models.CharField(max_length=255, null=True)
    created = models.DateTimeField(auto_now_add=True)

    # TODO user and address unique_together via validate_unique()
