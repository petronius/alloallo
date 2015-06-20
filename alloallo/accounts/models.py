from __future__ import unicode_literals

from authtools.models import AbstractEmailUser

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


class User(AbstractEmailUser):
    number = models.CharField(max_length=64, unique=True)

    USERNAME_FIELD = 'number'

    def get_full_name(self):
        return self.number

    def get_short_name(self):
        return self.number

    @python_2_unicode_compatible
    def __str__(self):
        return self.number
