from __future__ import unicode_literals, absolute_import

from django.contrib.contenttypes.models import ContentType
from django.db.models.loading import get_model
from django.utils.functional import cached_property


class ContentTypeContainer(object):
    @cached_property
    def all(self):
        return ContentType.objects.get_for_models(
            get_model('leagues', 'DivisionSettings'),
            get_model('leagues', 'CupSettings'),
            get_model('matches', 'CupRound'),
            get_model('matches', 'DivisionRound')
        )

contenttypes = ContentTypeContainer()
