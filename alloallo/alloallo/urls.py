from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from . import views

# from rest_framework import routers
# from ..leagues.api.viewsets import LeagueViewSet
# router = routers.DefaultRouter()
# router.register(r'leagues', LeagueViewSet)

# router.urls

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^', views.HomeView.as_view(), name='home'),
    # url(r'', include('alloallo.home.urls', namespace="home")),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
