# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns, include
from django.template.base import Context #Template, RequestContext  # Library, Node
#from django.views.generic import ListView

from django.contrib.sitemaps.views import sitemap
from products.views import ProductSitemap
from eracks.sitemaps import StaticViewSitemap

sitemaps = {
    'static': ProductSitemap,
}
sitemaps1 = {
    'static': StaticViewSitemap,
}


#from obdjects.classes import Obdject
#from orders.models import OrderForm
#from home import templets

# Add this to base urls with r"'^' - JJW

urlpatterns = patterns('',
    url(r'^$', 'home.views.index', name='index'),
    url(r'^contact/$', 'home.views.contact', name='contact'),
    url(r'^testresults/$', 'home.views.testresults', name='testresults'),

    url(r'^products_sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^all_sitemap\.xml$',      sitemap, {'sitemaps': sitemaps1}, name='django.contrib.sitemaps.views.sitemap'),

    #(r'^checkout/', Obdject (
    #    template = 'checkout.html',
    #    checkoutform = OrderForm(),
    #    #testimonials = Testimonial.objects.filter (published=True),
    #    content_row = templets.content_row.render (Context (dict (checkoutform = OrderForm()))),  # can't we figure out the tree from here?!  who wants what, etc?  & build precedence..
    #    )
    #),
)
