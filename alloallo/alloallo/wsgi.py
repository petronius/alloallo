"""
WSGI config for alloallo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
from __future__ import unicode_literals, absolute_import

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alloallo.alloallo.settings.production")

from django.core.wsgi import get_wsgi_application
from dj_static import Cling

application = Cling(get_wsgi_application())
