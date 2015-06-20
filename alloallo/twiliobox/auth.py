from importlib import import_module

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.functional import SimpleLazyObject


TWILIO_SESSION_PREFIX = 'TWILIO_SESSION_'
User = apps.get_model('accounts.User')


class TwilioSessionMiddleware(object):
    def __init__(self):
        engine = import_module(settings.SESSION_ENGINE)
        self.SessionStore = engine.SessionStore

    def process_request(self, request):
        if 'HTTP_X_TWILIO_SIGNATURE' not in request.META:
            return

        request.ignore_check = True
        try:
            user_number = request.POST['From']
            session_key = TWILIO_SESSION_PREFIX + user_number
            request.session = self.SessionStore(session_key)
            request.user = SimpleLazyObject(
                lambda: User.objects.get(number=user_number)
            )
        except ObjectDoesNotExist:
            pass
