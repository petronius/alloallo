
import braintree
import json

from django.http import HttpResponse

from ..alloallo.settings.braintree import SAMPLE_CLIENT_TOKEN

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

def checkout(request):
    pass
