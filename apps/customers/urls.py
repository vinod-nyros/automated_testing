# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns, include
#from django.template.base import Context #Template, RequestContext  # Library, Node
#from django.views.generic import ListView

#from obdjects.classes import Obdject
#from customers.models import CustomerImage, Testimonial
#from customers import templets


urlpatterns = patterns('',
    #(r'^', 'customers.views.test'),

    (r'^$', 'customers.views.index'),
    #(r'^index2', 'customers.views.index2'),
    #(r'^index3', Obdject (
    #    template = 'customers.html',
    #    customers = CustomerImage.objects.filter (published=True),
    #    testimonials = Testimonial.objects.filter (published=True),
    #    )
    #),
    #(r'^index4/', include ('customers.views')),

    #(r'^',  ListView.as_view (
    #            #model=Publisher,
    #            context_object_name="publisher_list",
    #            queryset = CustomerImage.objects.filter(published=True),
    #            template_name = "books/acme_list.html",
    #        )
    #),

    (r'^save_email/$', 'customers.views.save_email'),
    (r'^emails/$', 'customers.views.emails'),
)
