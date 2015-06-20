from django.conf.urls import url
from . import views

urlpatterns = [
    url('client-token', views.client_token, name='client_token'),
]
