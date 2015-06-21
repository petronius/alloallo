"""
Django settings for alloallo project - local instance.
"""
from __future__ import unicode_literals, absolute_import

from .heroku import *

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', '..')

ALLOWED_HOSTS = ['allo-allo.herokuapp.com']

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

TWILIO_NUMBER = MAIN_INCOMING_NUMBER.replace(' ', '')
TWILIO_LIVE_SID = 'AC1a44690eb4ffcd13bd05ae9c82d07442'
TWILIO_LIVE_TOKEN = 'bc4498d22a5e70d666b6049fd36d6520'
