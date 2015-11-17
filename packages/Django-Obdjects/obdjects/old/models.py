# encoding: utf-8
from __future__ import absolute_import

from django.db import models
from django.contrib import admin
from django.contrib.sites.models import Site as DjangoSite

from eracks.obdjects.minitags import meta as metatag

#class Domain(DjangoSite):
class Site(DjangoSite):
  template_root = models.CharField(max_length=200, blank=True)
  template_name = models.CharField(max_length=200)
  media_root    = models.CharField(max_length=200, blank=True)
  urlconf       = models.CharField(max_length=200, blank=True)
  base          = models.CharField(max_length=200, blank=True)
  create_date   = models.DateTimeField('date created', auto_now_add=True)
  update_date   = models.DateTimeField('date updated', auto_now=True)
  published     = models.BooleanField(default=True)
  def __str__ (self): return self.name


class Meta (models.Model):  # m2m
  title         = models.CharField(max_length=100)
  name          = models.CharField(max_length=100, blank=True)
  http_equiv    = models.CharField(max_length=100, blank=True)
  scheme        = models.CharField(max_length=100, blank=True)
  content       = models.TextField()
  create_date   = models.DateTimeField('date created', auto_now_add=True)
  update_date   = models.DateTimeField('date updated', auto_now=True)
  published     = models.BooleanField(default=True)
  def __str__ (self): return self.title

  @property
  def as_tag (self):
    kw = dict (content=self.content)  # required
    if self.name: kw ['name'] = self.name
    elif self.http_equiv: kw ['http_equiv'] = self.http_equiv
    else: raise Exception, 'Meta error: Must set only name or http_equiv'
    if self.scheme: kw ['scheme'] = self.scheme
    return metatag (**kw)

  class Meta: verbose_name_plural = 'Meta'

# name="date" content="2008-09-15" scheme="YYYY-MM-DD"

# Page - meta, title, js/css, content/snippet

class Snippet (models.Model):
  name          = models.CharField(max_length=100)
  slug          = models.CharField(max_length=100)
  title         = models.CharField(max_length=100)
  js            = models.CharField(max_length=200, blank=True)
  css           = models.CharField(max_length=200, blank=True)
  meta          = models.ManyToManyField (Meta, blank=True)
  body          = models.TextField()
  create_date   = models.DateTimeField('date created', auto_now_add=True)
  update_date   = models.DateTimeField('date updated', auto_now=True)
  published     = models.BooleanField(default=True)
  def __str__ (self): return self.title or self.name
  def get_absolute_url (self): return '/%s/' % self.slug
  url = property (get_absolute_url)


class SiteAdmin (admin.ModelAdmin):
  # NFG - pub_date doesn't show.
  #fields = ('title', 'slug', 'published', 'pub_date', 'body', 'author', 'categories')
  date_hierarchy = 'update_date'
  list_display = ['name', 'published', 'update_date', 'template_root', 'template_name', 'urlconf']
  #prepopulated_fields = { 'slug': ('title',) }
  list_filter = ['published', 'create_date', 'update_date', 'template_root', 'urlconf']
  #filter_horizontal = ['categories']

class MetaAdmin (admin.ModelAdmin):
  fieldsets = (
        (None, { 'fields': (('title', 'published'),) }),
        ('Name or http-equiv', { 'fields': (('name', 'http_equiv'),),'description':'Must use only one or the other' }),
        (None, { 'fields': ('scheme','content') }),
  )
  #fields = ('title', 'slug', 'published', 'pub_date', 'body', 'author', 'categories')
  date_hierarchy = 'update_date'
  list_display = ['title', 'name', 'http_equiv', 'content', 'update_date']
  #prepopulated_fields = { 'slug': ('title',) }
  search_fields = ['title', 'content']
  list_filter = ['published', 'name', 'http_equiv', 'create_date', 'update_date', ]
  #filter_horizontal = ['categories']

class SnippetAdmin (admin.ModelAdmin):
  fieldsets = (
        (None, { 'fields': (('name', 'slug', 'title', 'published'), ('js', 'css'),) }),
        ('Body', { 'fields': ('body',), 'classes': ('collapse', 'wymeditor'), }),
        ('Meta', { 'fields': ('meta',), 'classes': ('collapse', 'wymeditor'), }),
  )
  #fields = ('title', 'slug', 'published', 'pub_date', 'body', 'author', 'categories')
  date_hierarchy = 'update_date'
  list_display = ['name', 'title', 'update_date']
  prepopulated_fields = { 'slug': ('name',) }
  search_fields = ['title', 'body', 'js', 'css']
  list_filter = ['published', 'js', 'css', 'meta', 'create_date', 'update_date', ]
  filter_horizontal = ['meta']
  class Media:
    #css = { "all": ("my_styles.css",) }
    js = ("/js/jquery/jquery.js",
          "/js/wymeditor/jquery.wymeditor.pack.js",
          "/js/wymeditor/plugins/hovertools/jquery.wymeditor.hovertools.js",
          "/js/wymeditor/plugins/resizable/jquery.wymeditor.resizable.js",
          "/js/jjw-multi-init.js",
         )


admin.site.register (Site, SiteAdmin)
admin.site.register (Meta, MetaAdmin)
admin.site.register (Snippet, SnippetAdmin)

