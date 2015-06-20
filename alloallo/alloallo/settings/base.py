from __future__ import unicode_literals, absolute_import

import os.path

from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ImproperlyConfigured

from .braintree import *

gettext_noop = lambda s: s


def get_env_variable(var_name, default=None):
    """Get the environment variable or return exception"""
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        error_msg = "Set %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)

HOST_BASE_URL = None

SECRET_KEY = get_env_variable('SECRET_KEY', '')

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', '..')

# Application definition
INSTALLED_APPS = (
    'alloallo.alloallo',
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'authtools',
    'crispy_forms',
    'easy_thumbnails',
    'alloallo.profiles',
    'alloallo.accounts',
    'alloallo.payments',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'alloallo.twiliobox.auth.TwilioSessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'alloallo.payments.middleware.PayMeNowMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'alloallo', 'alloallo', 'templates'),
)


STATIC_URL = '/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

ROOT_URLCONF = 'alloallo.alloallo.urls'

WSGI_APPLICATION = 'alloallo.alloallo.wsgi.application'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = True

LANGUAGES = (
    ('en', gettext_noop('English')),
)

LANGUAGE_CODE = 'en'

LOGIN_REDIRECT_URL = 'leagues:my'

import dj_database_url
DATABASES = {'default': dj_database_url.config()}
DATABASES['default']['ATOMIC_REQUESTS'] = True

DEFAULT_FROM_EMAIL = 'support@alloallo.eu'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = str(get_env_variable('EMAIL_HOST', ''))

# Default values, if EMAIL_HOST stay empty they will overriden
LOG_REQUESTS = True
LOG_REQUEST_ID_HEADER = "HTTP_HEROKU_REQUEST_ID"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s(%(asctime)s %(name)s %(message)s'
        },
        'sql': {
            'format': '%(asctime)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARN',
        },
        'django.db.backends': {
            'level': 'WARN',
            'handlers': ['console'],
            'propagate': False,
        },
        'alloallo': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARN',
        },
        'alloallo.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}


AUTH_USER_MODEL = 'accounts.User'

# Use Django templates using the new Django 1.8 TEMPLATES settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            # insert more TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

CRISPY_TEMPLATE_PACK = 'bootstrap3'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]


TWILIO_TEST_SID = 'AC2728c00f4891d511c061192e87fcb371'
TWILIO_TEST_TOKEN = '663b4ef990a9&c485#5CxQb1f9a'

LOGIN_REDIRECT_URL = reverse_lazy("profiles:show_self")
LOGIN_URL = reverse_lazy("accounts:login")

TWILIO_LIVE_SID = 'AC31fd5cdbb768c43ad9ab50f9de04db72'
TWILIO_LIVE_TOKEN = 'f565ff4b0ca7f03f85c4711a8335255e'
