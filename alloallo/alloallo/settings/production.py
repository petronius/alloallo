"""
Django settings for alloallo project - local instance.
"""
from __future__ import unicode_literals, absolute_import

from .heroku import *

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', '..')

ALLOWED_HOSTS = ['allo-allo.herokuapp.com']

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

TWILIO_NUMBER = MAIN_INCOMING_NUMBER.replace(' ', '')
TWILIO_LIVE_SID = 'ACfb92dacf5b98f36c584b7032cf004938'
TWILIO_LIVE_TOKEN = '73149d1d1c120222a99e50e9ca83f4a2'
