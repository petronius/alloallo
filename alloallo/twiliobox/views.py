# from django.shortcuts import render
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.views import generic
from django.http import HttpResponse
from django.core.urlresolvers import reverse as dreverse

from twilio import twiml

# Create your views here.

Profile = apps.get_model('profiles.Profile')


def reverse(name, *args, **kwargs):
    name = 'twiliobox:{}'.format(name)
    return dreverse(name, *args, **kwargs)


class IncomingCall(generic.View):
    """ Handle incoming view """

    def post(self, request):
        data = request.POST
        number = data['From']
        response = twiml.Response()

        response.say('Welcome to Allo Allo!')

        try:
            profile = Profile.objects.get(user__number=number)
            # profile = Profile.objects.get(user__number='+48606509545')
        except ObjectDoesNotExist:
            response.say('Please visit our site to create an account')
            return HttpResponse(response)

        if not profile.audio_description:
            response.say('Please record your audio description first')
            response.redirect(reverse('description_edit'))
        else:
            response.say('We are happy to hear you.')
            # response.redirect(reverse('main_menu'))
        return HttpResponse(response)


class MainMenu(generic.View):

    def post(self, request):
        response = twiml.Response()
        response.say('This is the main menu')
        return HttpResponse(response)


class DescriptionEdit(generic.View):

    def post(self, request, confirmation=None):
        response = twiml.Response()
        data = request.POST

        if confirmation is None:
            response.say('Tell others something about you in 30 seconds')
            response.record(
                maxLength='30',
                action=reverse(
                    'description_edit_confirm',
                    kwargs={'confirmation': 1}
                ),
            )
        elif data.get("RecordingUrl", None):
            recording_url = data.get("RecordingUrl", None)
            response.say('Thank you. Here is your description')
            response.play(recording_url)
            # TODO: save it to Profile.audio_description
            response.redirect(reverse('main_menu'))

        return HttpResponse(response)
