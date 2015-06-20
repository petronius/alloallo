# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'alloallo/home.html'
