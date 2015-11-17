# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns, include
from django.template.base import Context #Template, RequestContext  # Library, Node
#from django.views.generic import ListView


# Add this to base urls with r'^' include or +=  - JJW

urlpatterns = patterns('orders.views',
    (r'^checkout/$', 'checkout'),
    (r'^checkout/confirm/$', 'checkout', { 'confirm': True }),
    (r'^checkout/order/$', 'order'),
    (r'^checkout/ordered/$', 'ordered'),

    (r'^cart/$', 'cart'),
    (r'^session/$', 'view_session'),
    (r'^admin_order_grid/$', 'admin_order_grid'),
)

