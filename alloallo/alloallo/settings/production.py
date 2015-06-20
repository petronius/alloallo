"""
Django settings for alloallo project - local instance.
"""
from __future__ import unicode_literals, absolute_import

from .heroku import *

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', '..')

ALLOWED_HOSTS = ['allo-allo.herokuapp.com']

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
