# -*- coding: utf-8 -*-

from django.conf.urls import patterns #, url, include

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # main product page - by category, by application, etc
    #
    # commented out temporarily JJW 11/1/12 til done - use redir to /showroom for now
    #(r'^$',                                      'products.views.products'),

    # redirect legacy zope URLs
    (r'^config/?$',                               'products.views.config'),
    (r'^(?P<legacy_category>[\w\-\ ]+)/config/?$','products.views.config'),

    # Ajax product configurator entrypoint
    (r'^update_grid/$',                           'products.views.update_grid'),
    #(r'^configgrid/(?P<sku>.*)$', 'django_eracks.apps.legacy.views.configgrid'),
    #(r'^configgrid2/(?P<sku>.*)$', 'django_eracks.apps.legacy.views.configgrid2'),

    # Category list
    (r'^categories/$',                            'products.views.categories'),

    # Individual category & product - these must be last, since they match everything :)
    (r'^(?P<category>[\w\-\ ]+)/$',               'products.views.category'),
    (r'^(?P<category>[\w\-\ ]+)/(?P<sku>.*)/$',   'products.views.product'),
)
