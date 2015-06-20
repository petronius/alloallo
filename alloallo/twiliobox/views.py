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

        response.say('Welcome to Allo Allo!', voice='alice')

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
            response.say('Thank you. Here is your description')
            response.play(recording_url)
            # TODO: save it to Profile.audio_description
            response.redirect(reverse('main_menu'))

        return HttpResponse(response)
