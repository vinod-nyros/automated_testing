# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import smart_unicode, force_unicode, smart_str

trace = 0

class Sql (models.Model):
    description = models.CharField(max_length=160)
    updates     = models.BooleanField(default=False, help_text='Updates DB')  #'Upd!', help_text='Updates the Database!')
    sql         = models.TextField()

    parm1       = models.CharField(blank=True, max_length=30)
    parm2       = models.CharField(blank=True, max_length=30)
    parm3       = models.CharField(blank=True, max_length=30)
    parm4       = models.CharField(blank=True, max_length=30)
    parm5       = models.CharField(blank=True, max_length=30)

    notes       = models.TextField(blank=True)
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)

    def __unicode__ (self):
        return self.description

    #class Meta:
    #    db_table = u'cacounties'


