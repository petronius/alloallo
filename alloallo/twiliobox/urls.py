from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^incoming$', views.IncomingCall.as_view(), name='incoming_call'),
    url(r'^description_edit$', views.DescriptionEdit.as_view(),
        name='description_edit'),
    # url(r'^description_view$', views.DescriptionView.as_view(),
    #     name='description_view'),
    url(r'^main_menu$', views.MainMenu.as_view(), name='main_menu'),
    # url(r'^(?P<slug>[\w\-]+)$', views.ShowProfile.as_view(), name='show'),
]
