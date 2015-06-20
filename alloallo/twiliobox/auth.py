from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sessions.backends.base import CreateError
from django.contrib.sessions.backends.db import SessionStore
from django.utils.functional import SimpleLazyObject


TWILIO_SESSION_PREFIX = 'TWILIO_SESSION_'
User = apps.get_model('accounts.User')


class ForcedSessionIdSessionStore(SessionStore):
    def create(self):
        try:
            self.save(must_create=True)
        except CreateError:
            self.delete()
            self.save()
        self.modified = True
        self._session_cache = {}
        return


class TwilioSessionMiddleware(object):
    def process_request(self, request):
        if 'HTTP_X_TWILIO_SIGNATURE' not in request.META:
            return

        request.ignore_check = True
        try:
            user_number = request.POST['From']
            session_key = TWILIO_SESSION_PREFIX + user_number
            request.session = ForcedSessionIdSessionStore(session_key)
            request.user = SimpleLazyObject(
                lambda: User.objects.get(number=user_number)
            )
        except ObjectDoesNotExist:
            pass


def flush_user_session(request, number):
    session_key = TWILIO_SESSION_PREFIX + request.user.number
    ForcedSessionIdSessionStore(session_key).create()
