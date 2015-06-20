from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from alloallo.profiles import urls as profiles_urls
from alloallo.accounts import urls as accounts_urls
from alloallo.twiliobox import urls as twiliobox_urls
from alloallo.payments import urls as payments_urls

from . import views

urlpatterns = [
    url(r'^users/', include(profiles_urls, namespace='profiles')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(accounts_urls, namespace='accounts')),
    url(r'^calls/', include(twiliobox_urls, namespace='twiliobox')),
    url(r'^payments/', include(payments_urls, namespace='payments')),

    url(r'^about/$', views.AboutPage.as_view(), name='about'),
    url(r'^find-friend/$', views.FindFriend.as_view(), name='find_friend'),
    url(r'^$', views.HomePage.as_view(), name='home'),
]

# User-uploaded files like profile pics need to be served in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
