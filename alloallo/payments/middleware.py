
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
        if isinstance(user, AnonymousUser) or not user:
            return
        if user.is_paid:
            return
        payment_url = reverse("payments:payment")
        payment_url = reverse("payments:checkout")
        if request.path != payment_url and request.path != checkout_url:
            return HttpResponseRedirect(payment_url)


