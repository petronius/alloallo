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
        response = twiml.Response()
        response.say('Welcome to Allo Allo!', voice='alice')

        user = request.user
        if not user or not user.is_paid:
            if not user:
                response.say('Please visit our site to create an account.')
            if not user.is_paid:
                response.say('Please visit our site to make a payment.')
            # profile = Profile.objects.get(user__number=number)
            # profile = Profile.objects.get(user__number='+48606509545')
            return HttpResponse(response)

        if not user.profile.audio_description:
            response.say('Please record your audio description first')
            response.redirect(reverse('description_edit'))
        else:
            response.say('We are happy to hear you.')
            response.redirect(reverse('main_menu'))
        return HttpResponse(response)


class ViewWithHandler(generic.View):
    """
    Use default post to do whatever you want, and post_handler method
    to do something with selected option
    """

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            if request.POST.get('Digits'):
                digits = request.POST['Digits']
                return self.post_handler(
                    request, digits, *args, **kwargs
                )
            return self.post(request, *args, **kwargs)
        return super(ViewWithHandler, self).dispatch(
            request, *args, **kwargs
        )


class MainMenu(ViewWithHandler):
    """ Main voice menu view (that sounds stupid...) """

    menu_options = [
        {
            'desc': 'Call a stranger',
            # 'url': reverse('call_random_person'),
        },
        {
            'desc': 'Call a friend',
            # 'url': reverse('call_friend'),
        },
        {
            'desc': 'Post to your wall',
            # 'url': reverse('post_to_wall'),
        },
        {
            'desc': 'Go to Profile settings',
            # 'url': reverse('profile_settings'),
        },
    ]

    @property
    def saidable_menu(self):
        result = []
        for i, menu_dict in enumerate(self.menu_options, 1):
            result.append(
                'To {}, press {}'.format(menu_dict['desc'], i)
            )
        return '.\n'.join(result)

    def post(self, request):
        response = twiml.Response()
        response.say('Please select an option.', voice='woman')

        with response.gather(
            numDigits=1,
            action=reverse('main_menu'),
            method='POST',
            timeout=15,
        ) as g:
            g.say(self.saidable_menu, loop=3)

        return HttpResponse(response)

    def post_handler(self, request, digit):
        menu_index = int(digit) - 1  # menu is presented starting from 1
        selected = self.menu_options[menu_index]

        response = twiml.Response()
        response.say(
            'You decided to {}'.format(selected['desc'])
        )
        return HttpResponse(response)


class DescriptionEdit(generic.View):

    def post(self, request, confirmation=None):
        response = twiml.Response()
        data = request.POST

        if confirmation is None:
            response.say('Tell us something about you.')
            response.say('To finish, press any key.')
            response.record(
                maxLength='10',
                action=reverse(
                    'description_edit_confirm',
                    kwargs={'confirmation': 1}
                ),
            )
        elif data.get("RecordingUrl", None):
            recording_url = data.get("RecordingUrl", None)
            response.say('Thank you.')
            request.user.profile.audio_description = recording_url
            request.user.profile.save()
            # response.play(recording_url)
            response.redirect(reverse('main_menu'))

        return HttpResponse(response)


class RandomCall(ViewWithHandler):

    def get_random_profile(self):
        return Profile.objects.filter(audio_description__isnull=False).order_by('?').first()

    def get_last_profile(self, request):
        user_id = request.session.get("last_played_profile")
        profile = Profile.objects.get(user_id=user_id)
        return profile

    def post(self, request):
        response = twiml.Response()
        response.say('Now playing a new user profile.'+
            ' Press 1 at any time to start a conversation, and 2 to skip to the'+
            ' next profile', voice='woman')

        user_profile = self.get_random_profile()
        request.session["last_played_profile"] = user_profile.user.id
        audio_url = user_profile.audio_description
        # play the profile
        with response.gather(
            numDigits=1,
            action=reverse('call_random_person'),
            method='POST',
            timeout=40,
        ) as g:
            g.play(audio_url, loop=2)

        return HttpResponse(response)

    def post_handler(self, request, digit):
        request_talk = (digit == "1")
        if request_talk:
            other_profile = self.get_last_profile(request)
            return self.setup_conversation(other_profile)
        else:
            # Give them another choice
            return self.post(request)


    def setup_conversation(self, profile2):
        response = twiml.Response()
        response.say("Connecting you to your selected user.")
        response.dial(profile2.user.number)
        response.say("The call failed or the user hung up.")
        return HttpResponse(response)
        
