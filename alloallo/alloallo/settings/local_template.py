"""
Django settings for mycup project - local instance.
"""
from __future__ import unicode_literals, absolute_import

import os.path

from .base import *

SECRET_KEY = 'dfgnksdjfnjkwh234'

INSTALLED_APPS += (
    'django_pdb',
    'debug_toolbar'
)

DEBUG = True
TEMPLATE_DEBUG = True
# POST_MORTEM = True

INTERNAL_IPS = ('127.0.0.1',)
MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

DEBUG_TOOLBAR_CONFIG = {
    # 'INTERCEPT_REDIRECTS': True,
    # 'HIDE_IN_STACKTRACES': ('threading', 'wsgiref', 'debug_toolbar'),
}

ALLOWED_HOSTS = []

LOGGING['loggers']['django']['level'] = 'DEBUG'
LOGGING['loggers']['alloallo']['level'] = 'DEBUG'
LOGGING['loggers']['django.db.backends']['level'] = 'DEBUG'

DATABASE_URL = 'postgres://eebfviroulknql:osyVWO4Fa9Q-9ZpFq-GQ4qVZyR@ec2-54-228-180-92.eu-west-1.compute.amazonaws.com:5432/dgr99vqvt7ues'
DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}
