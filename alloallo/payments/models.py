
from django.conf import settings
from django.db import models

class BraintreeTransaction(models.Model):
    nonce = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
