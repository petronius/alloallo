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
LOGGING['loggers']['django.request']['handlers'] = ['console']
LOGGING['loggers']['django.db.backends']['handlers'] = ['console']
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

if not EMAIL_HOST:
    EMAIL_HOST_USER = str(get_env_variable('SENDGRID_USERNAME'))
    EMAIL_HOST_PASSWORD = str(get_env_variable('SENDGRID_PASSWORD'))
    EMAIL_HOST = str('smtp.sendgrid.net')
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
