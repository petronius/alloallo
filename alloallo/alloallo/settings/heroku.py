"""
Django settings for alloallo project - local instance.
"""
from __future__ import unicode_literals, absolute_import

from .base import *

LOGGING['handlers']['error_log'] = {
    'level': 'ERROR',
    'class': 'django.utils.log.AdminEmailHandler',
}
LOGGING['loggers']['django']['handlers'] = ['console']
LOGGING['loggers']['alloallo']['handlers'] = ['console']
LOGGING['loggers']['alloallo']['level'] = 'DEBUG'
LOGGING['loggers']['alloallo.request']['handlers'] = ['console']

STATIC_URL = '/static/'

MIDDLEWARE_CLASSES = (
    'sslify.middleware.SSLifyMiddleware',
) + MIDDLEWARE_CLASSES

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)
