from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    url(r'^incoming$',
        csrf_exempt(views.IncomingCall.as_view()),
        name='incoming_call'),
    url(r'^call_random_person$',
        csrf_exempt(views.RandomCall.as_view()),
        name='call_random_person'),
    url(r'^description_edit$',
        csrf_exempt(views.DescriptionEdit.as_view()),
        name='description_edit'),
    url(r'^description_edit/(?P<confirmation>[\d])$',
        csrf_exempt(views.DescriptionEdit.as_view()),
        name='description_edit_confirm'),
    # url(r'^description_view$', views.DescriptionView.as_view(),
    #     name='description_view'),
    url(r'^main_menu$',
        csrf_exempt(views.MainMenu.as_view()),
        name='main_menu'),
    # url(r'^(?P<slug>[\w\-]+)$', views.ShowProfile.as_view(), name='show'),
]
