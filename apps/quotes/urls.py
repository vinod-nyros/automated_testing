# -*- coding: utf-8 -*-
from django.conf.urls import patterns # url, include

urlpatterns = patterns ('',
    (r'^(?P<num>.*)\.pdf$', 'quotes.views.quote', { 'pdf': True }),
    (r'^(?P<num>.*)/*$', 'quotes.views.quote'),
    #(r'^(?P<num>[^/]*)/pdf$', 'eracks9.apps.quotes.views.quote', { 'pdf': True }),
)

