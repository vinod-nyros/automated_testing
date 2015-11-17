# -*- coding: utf-8 -*-

#import re, os

#from django.template import TemplateSyntaxError, VariableDoesNotExist

#from django.core.cache import cache
from django.contrib.sites.models import Site
from django.utils.translation import get_language
from django.template import Library, Template, Context # , Node, Variable
#from django.db.models import Count #Avg

from keyedcache import cache_function

from eracksaccessories.bloglet.models import Post

#from satchmo_store.shop.templatetags.satchmo_category import category_tree
#from satchmo_store.shop.templatetags.satchmo_util import satchmo_search_form as my_search_form
#from satchmo_utils.templatetags import get_filter_args
#from django.utils.translation import get_language

#from utils.minitags import a as link, ul, li, h3
from utils import hamlpy



## globals

register = Library()
trace = 0
site = Site.objects.get (name='eRacks Accessories')
lang = get_language()
cachetime = 3600   # 10 hours - could make it longer


## haml templates

bloglet_haml='''
.box
  %h2 {{ title }}
  %ul
    - for item in list
      %li <a href="{{ item.get_absolute_url }}" title="{{ item.description }}">{{ item.name }}</a>
'''

bloglet_haml='''
.box
  %h2 {{ title }}
  - for item in list
    .bloglet_entry
      {{ item|safe }}
    <hr width=75%>
'''


## tags

@cache_function (length=cachetime)
def inner_bloglet():
    #print 'Uncached Bloglet'

    posts = Post.objects.filter (published=True, categories__slug__iexact='eracks-news').order_by ('-pub_date').values_list ('body', flat=True)
    #posts = Post.objects.filter (published=True, categories__slug__iexact='eracks-accessories-news').order_by ('-pub_date').values_list ('body', flat=True)
    #posts = Post.objects.filter (published=True).order_by ('-pub_date').values_list ('body', flat=True)

    c = Context (dict (
        title='Accessories News',   # "eRacks" won't fit!
        list=posts,
        ))
    return Template (hamlpy (bloglet_haml)).render (c)

    return '<hr width=75%>'.join (posts)

    #c = Context (dict (
    #    title='The Latest...',
    #    list=Category.objects.annotate (prods=Count('product')).order_by ('-prods') [:10]))
    #return Template (hamlpy (bloglet_haml)).render (c)

    #def whatsnew (self, req, ses, **kw):
    #posts = Post.objects.filter (published=True,
    #          categories__slug__iexact='eracks-news').order_by ('-pub_date').values_list ('body', flat=True)
    #return '<hr width=75%>'.join (posts)

@register.simple_tag
def bloglet():
    return inner_bloglet()


