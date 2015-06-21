"""
Django settings for alloallo project - local instance.
"""
from __future__ import unicode_literals, absolute_import

from .heroku import *

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', '..')

ALLOWED_HOSTS = ['allo-allo.herokuapp.com']

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

TWILIO_NUMBER = MAIN_INCOMING_NUMBER.replace(' ', '')
TWILIO_LIVE_SID = 'AC31fd5cdbb768c43ad9ab50f9de04db72'
TWILIO_LIVE_TOKEN = 'f565ff4b0ca7f03f85c4711a8335255e'
