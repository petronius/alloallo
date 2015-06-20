
import braintree
import json

from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse

from ..alloallo.settings.braintree import SAMPLE_CLIENT_TOKEN
from .models import BraintreeTransaction

JSON_CONTENT_TYPE="application/json"


def json_response(f):
    def wrapped(*args, **kwargs):
        resp = f(*args, **kwargs)
        if isinstance(resp, HttpResponse):
            return resp
        data = json.dumps(resp)
        return HttpResponse(data, content_type=JSON_CONTENT_TYPE)
    return wrapped


@json_response
def client_paid(request):
    return {}

# Quick and dirty
@csrf_exempt
def checkout(request):
    nonce = request.POST.get("payment_method_nonce")
    if not nonce:
        return HttpResponse("Invalid nonce.", status="403")
    user = request.user
    # Set the user as paid up
    user.is_paid = True
    user.save()
    # Store the transaction
    transaction = BraintreeTransaction(user=user, nonce=nonce)
    transaction.save()
    return HttpResponseRedirect(reverse("profiles:show_self"))

class PaymentsPage(generic.TemplateView):
    template_name = "payment.html"
