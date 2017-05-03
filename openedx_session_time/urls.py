# -*- coding: utf-8 -*-
"""
URLs for openedx_session_time.
"""
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'', TemplateView.as_view(template_name="openedx_session_time/base.html")),
]
