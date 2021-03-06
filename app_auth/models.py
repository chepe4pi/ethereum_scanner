import binascii
import os

from django.contrib.auth.models import User
from django.db import models


class ClientInfo(models.Model):
    user = models.OneToOneField(User, related_name='client_info', null=True)
    ip_address = models.CharField(max_length=15, null=True)
    http_user_agent = models.TextField()


class ApiKey(models.Model):
    key = models.CharField(max_length=40)
    client_info = models.OneToOneField(ClientInfo)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(ApiKey, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __unicode__(self):
        return self.key, self.user
