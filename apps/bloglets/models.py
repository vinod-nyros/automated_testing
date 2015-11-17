# encoding: utf-8

#from __future__ import absolute_import

from django.db import models
from django.contrib.auth.models import User

from apps.utils.managers import PublishedManager
from filebrowser.fields import FileBrowseField

from django.conf import settings
#if settings.DEBUG:
#    from bloglets import templets  # triggers template generation in debug & Django reload


# from http://www.allyourpixel.com/post/metaweblog-38-django/
# most recently from eracksaccessories 4/12 JJW

class Post(models.Model):
    slug        = models.SlugField(max_length=100, unique=True)
    title       = models.CharField(max_length=200)
    image       = FileBrowseField (max_length=200, directory="images/", extensions=[".jpg",".jpeg",".png",".gif"])  #, blank=True, null=True)
    pub_date    = models.DateTimeField('Date published') # auto_now_add=True) # editable=True) # blank=True, null=True)
    body        = models.TextField()
    #tags       = models.ManyToManyField(Tag)
    author      = models.ForeignKey(User)

    created     = models.DateTimeField('Date created', auto_now_add=True)
    updated     = models.DateTimeField('Date updated', auto_now=True)
    published   = models.BooleanField(default=True)
    #status      = models.CharField(max_length=32, default='Draft') # choices=STATUS_CHOICES, radio_admin=True,
    categories  = models.ManyToManyField ('Category')

    objects     = PublishedManager()

    def __unicode__ (self):
        return self.title

    class Meta:
        ordering = ["-pub_date"]


class Category(models.Model):
    slug        = models.SlugField(max_length=100, unique=True)
    title       = models.CharField(max_length=200)

    created     = models.DateTimeField('Date created', auto_now_add=True)
    updated     = models.DateTimeField('Date updated', auto_now=True)
    published   = models.BooleanField(default=True)

    objects     = PublishedManager()

    def __unicode__ (self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'


#### Admin moved to admin.py 7/11/11 JJW



#### Set up single-seq tables (org fm legacy eracks db)

from apps import helpers
from django.db.models.signals import pre_save

pre_save.connect (helpers.presave, sender=Post)
pre_save.connect (helpers.presave, sender=Category)
