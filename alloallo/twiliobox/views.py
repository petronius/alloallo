# from django.shortcuts import render
from urllib.parse import quote_plus
import random

from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.views import generic
from django.http import HttpResponse
from django.core.urlresolvers import reverse as dreverse

from twilio import twiml
from twilio.rest import TwilioRestClient

from . import auth

# Create your views here.

Profile = apps.get_model('profiles.Profile')
User = apps.get_model('accounts.User')
WallPost = apps.get_model('twiliobox.WallPost')


def reverse(name, *args, **kwargs):
    name = 'twiliobox:{}'.format(name)
    return dreverse(name, *args, **kwargs)


class IncomingCall(generic.View):
    """ Handle incoming view """

    def post(self, request):
        response = twiml.Response()

        user = request.user
        if isinstance(user, AnonymousUser) or not (
            user and user.first_name and user.last_name
        ):
            response.say('Welcome to Allo, Allo!', voice='woman')
        else:
            response.say(
                'Hello {} {}! Welcome to Allo, Allo!'.format(
                    user.first_name, user.last_name
                ),
                voice='woman'
            )

        if not user or not user.is_paid:
            if not user:
                response.say('Please visit our site to create an account.')
            if not user.is_paid:
                response.say('Please visit our site to make a payment.')
            # profile = Profile.objects.get(user__number=number)
            # profile = Profile.objects.get(user__number='+48606509545')
            return HttpResponse(response)

        auth.flush_user_session(request, request.user.number)

        if not user.profile.audio_description:
            response.say('Please record your audio description first')
            response.redirect(reverse('description_edit'))
        else:
            response.say('We are happy to hear you.')
            response.redirect(reverse('main_menu'))

        return HttpResponse(response)


# class StatusCallback(generic.View):
#     def _do_return_call(self, number, other_number):
#         client = TwilioRestClient(settings.TWILIO_LIVE_SID, settings.TWILIO_LIVE_TOKEN)
#         call = client.calls.create(
#             url=self.request.build_absolute_uri(reverse('review_call')) + '?other_number=' + quote_plus(other_number),
#             to=number,
#             from_=settings.TWILIO_NUMBER
#         )
#         return call.sid

#     def post(self, request):
#         data = request.POST
#         if request.session.get('conversation_succeded'):
#             return_call_id = self._do_return_call(data['From'], data['To'])
#             request.session['conversation_succeded'] = False
#             return HttpResponse(return_call_id)
#         return HttpResponse('')


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
            'url': 'call_random_person',
        },
        #{
        #    'desc': 'Call a friend',
        #    # 'url': 'call_friend',
        #},
        {
            'desc': 'Broadcast a story to your friends',
            'url': 'post_to_wall',
        },
        {
            'desc': 'Listen to your your friends\' wall posts',
            'url': 'listen_to_wall',
        },
        {
            'desc': 'Edit your profile message',
            'url': 'description_edit',
        },
        #{
        #    'desc': 'Go to Profile settings',
        #    # 'url': 'profile_settings',
        #},
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
        if selected.get('url'):
            response.redirect(reverse(selected['url']))
        return HttpResponse(response)


class Introduction(generic.View):
    """ play an intorduction of user1 calling to user2 """
    def post(self, request, user_pk):
        response = twiml.Response()
        response.say('Allo, allo! Someone is calling you!', voice='woman')
        caller_profile = Profile.objects.get(user__pk=user_pk)
        response.play(caller_profile.audio_description)
        # TODO: check if the user wants to talk
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

    def get_random_profile(self, request):
        profiles = [p for p in Profile.objects.all()]
        random.shuffle(profiles)
        for profile in profiles:
            try:
                if request.user and request.user.id == profile.user.id:
                    continue
            except:
                pass
            if profile.audio_description:
                return profile

    def get_last_profile(self, request):
        user_id = request.session.get("last_played_profile")
        profile = Profile.objects.get(user_id=user_id)
        return profile

    def post(self, request):
        response = twiml.Response()
        response.say(
            'Playing a random user profile. ' +
            'Press 1 at any time to start a conversation. ' +
            'Press 2 to skip to the next profile.',
            voice='woman')

        user_profile = self.get_random_profile(request)
        if not user_profile:
            response.say("Could not find a profile to match you with.")
            return HttpResponse(response)
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

    def setup_conversation(self, call_to_profile):
        response = twiml.Response()
        response.say("Connecting you to selected user.")
        self.request.session['conversation_succeded'] = True

        dial = response.dial(
            action=reverse('better_callback')
        )
        # This will introduce caller to the called person
        introduction_url = reverse(
            'introduce',
            kwargs={'user_pk': self.request.user.pk}
        )

        dial.number(call_to_profile.user.number, url=introduction_url)

        response.say("The call failed or the user hung up.")
        return HttpResponse(response)


class PostToWall(generic.View):
    def post(self, request, confirmation=None):
        response = twiml.Response()
        data = request.POST

        if confirmation is None:
            response.say('Please record your story after the beep.', voice="alice")
            response.say('To finish, press any key.', voice="alice")
            response.record(
                maxLength='10',
                action=reverse(
                    'post_to_wall_confirm',
                    kwargs={'confirmation': 1}
                ),
            )
        elif data.get("RecordingUrl", None):
            recording_url = data.get("RecordingUrl", None)
            response.say('Thank you. This story is now available to your friends.')
            wpost = WallPost(user=request.user, message=recording_url)
            wpost.save()

        return HttpResponse(response)


class ListenToWall(ViewWithHandler):

    def get_next_pending_wall_post(self, user, friends_list):
        for friend in friends_list:
            result = list(WallPost.objects.filter(user=friend))
            for post in result:
                if not post.was_played_for(user):
                    return friend, post
        return None, None

    def post(self, request, confirmation=None):
        response = twiml.Response()
        user = request.user
        friends = request.user.friends.all()
        friend, post = self.get_next_pending_wall_post(user, friends)
        if not post:
            response.say("We're sorry, but no stories from your friends are available.", voice="alice")
            response.redirect(reverse('main_menu'))
            return HttpResponse(response)
        msg = "Now playing a story from {} {}".format(friend.first_name, friend.last_name)
        response.say(msg)
        response.say("Press 1 at any time to skip to the next message.")

        with response.gather(
            numDigits=1,
            action=reverse('listen_to_wall'),
            method='POST',
            timeout=40,
        ) as g:
            post.mark_played_for(user)
            post.save()
            g.play(post.message, loop=1)

        return HttpResponse(response)

    def post_handler(self, request, confirmation=None):
        return self.post(request, confirmation)


# class QuickTest(generic.View):
#     def post(self, request):
#         response = twiml.Response()
#         response.say("Connecting you to random user.")
#         self.request.session['conversation_succeded'] = True

#         dial = response.dial(
#             action=reverse('better_callback')
#         )
#         # This will introduce caller to the called person
#         introduction_url = reverse(
#             'introduce',
#             kwargs={'user_pk': self.request.user.pk}
#         )

#         random_guy = User.objects.get(pk=22)

#         to_review = self.request.session.get('calls_to_review', [])
#         to_review.insert(0, random_guy.pk)
#         self.request.session['calls_to_review'] = to_review

#         dial.number(random_guy.number, url=introduction_url)

#         response.say("The call failed or the user hung up.")
#         return HttpResponse(response)


class BetterCallback(generic.View):
    def post(self, request):
        client = TwilioRestClient(
            settings.TWILIO_LIVE_SID, settings.TWILIO_LIVE_TOKEN)
        sid = request.POST.get('DialCallSid')
        call = client.calls.get(sid)

        # Having call.to and call.from_ here
        # just an extra check
        assert request.user == User.objects.get(number=call.from_)

        user1 = User.objects.get(number=call.from_)
        user2 = User.objects.get(number=call.to)

        client = TwilioRestClient(settings.TWILIO_LIVE_SID, settings.TWILIO_LIVE_TOKEN)
        client.calls.create(
            url=''.join([
                self.request.build_absolute_uri(reverse('review_call')),
                '?pk_from={}&pk_to={}'.format(user1.pk, user2.pk)
            ]),
            to=request.user.number,
            from_=settings.TWILIO_NUMBER
        )
        return HttpResponse('ok')


class ReviewIncomingCall(generic.View):
    def post(self, request):
        # Get the sid of call that has just been made
        pk_from = request.GET.get('pk_from')
        pk_to = request.GET.get('pk_to')

        other_user = User.objects.get(pk=pk_to)

        response = twiml.Response()
        response.say(
            'You have been talking with {} {}.'.format(
                other_user.first_name, other_user.last_name
            )
        )
        with response.gather(
            numDigits=1,
            action=''.join([
                reverse('add_friend_call'),
                '?pk_from={}&pk_to={}'.format(pk_from, pk_to)
            ]),
            method='POST',
            timeout=15,
        ) as g:
            g.say('Press 1 to add him as a friend or just hang up.')

        return HttpResponse(response)


class AddFriendCall(generic.View):
    def post(self, request):
        pk_from = request.GET.get('pk_from')
        pk_to = request.GET.get('pk_to')
        user1 = User.objects.get(pk=pk_from)
        user2 = User.objects.get(pk=pk_to)
        user1.friends.add(user2)

        response = twiml.Response()
        response.say(
            'You have added {} {} as a friend.'.format(
                user2.first_name, user2.last_name
            )
        )
        return HttpResponse(response)
