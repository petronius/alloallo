from django.conf import settings
from django.db import models

# Create your models here.


class WallPost(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    # recording url
    message = models.TextField()

    played_for = models.TextField()

    # this is not how you are supposed to use an RDBMS
    def was_played_for(self, user):
        return str(user.id) in self.played_for.split(",")

    def mark_played_for(self, user):
        self.played_for += ",{}".format(user.id)
        self.save()
