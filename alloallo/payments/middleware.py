
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser


class PayMeNowMiddleware(object):

    def process_request(self, request):
        """
        If the user hasn't paid, send them off to the payment screen.
        """
        user = request.user
        # Doesn't matter if the user isn't logger in
        if (
            getattr(request, 'ignore_check', False) or
            not user or
            isinstance(user, AnonymousUser) or
            user.is_paid
        ):
            return
        allowed_urls = [
            reverse("accounts:logout"),
            reverse("payments:payment"),
            reverse("payments:checkout"),
        ]
        if request.path not in allowed_urls:
            return HttpResponseRedirect(reverse("payments:payment"))
