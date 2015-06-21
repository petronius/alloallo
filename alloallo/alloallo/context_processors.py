from __future__ import unicode_literals, absolute_import

from django.conf import settings


def global_variables(request):
    return {
        'INCOMING_NUMBERS': settings.INCOMING_NUMBERS,
        'MAIN_INCOMING_NUMBER': settings.MAIN_INCOMING_NUMBER,
    }
