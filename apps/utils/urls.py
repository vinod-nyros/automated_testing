# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns, include
#from django.conf import settings
#from django.http import HttpResponse


urlpatterns = patterns('apps.utils.views',
    (r'^urls/?$', 'urls'),
    (r'^refresh/?$', 'refresh'),
    (r'^clearcache/?$', 'clearcache'),
    (r'^collect_static/?$','collect_static'),
)
