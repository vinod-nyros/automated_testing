# encoding: utf-8

from django import forms
from django.db import models
#from django.contrib import admin
from django.utils.safestring import mark_safe

from managers import PublishedManager


#### Models

class Snippet (models.Model):
    name        = models.CharField(max_length=100, help_text="Name, identifier-style, no spaces, will be exported into request context")
    #slug       = models.CharField(max_length=100)
    title       = models.CharField(max_length=100, blank=True, help_text="Title, verbose name / short description")
    #js         = models.CharField(max_length=200, blank=True, help_text="Javascript for this snippet")
    #css        = models.CharField(max_length=200, blank=True, help_text="CSS for this snippet")
    #meta       = models.ManyToManyField (Meta, blank=True)
    body        = models.TextField(help_text="Body of snippet, available via {{ &lt;name&gt; }} in templates")

    created     = models.DateTimeField('date created', auto_now_add=True)
    updated     = models.DateTimeField('date updated', auto_now=True)
    published   = models.BooleanField(default=True)

    objects     = PublishedManager()

    def __unicode__ (self):
        #return mark_safe (self.body or self.title or self.name)
        return '%s (%s)' % (self.name, self.title)


    # TODO:  Add slug, template, image

    def get_absolute_url (self): return '/%s/' % self.name #slug
    url = property (get_absolute_url)

