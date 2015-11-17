# -*- coding: utf-8 -*-

from django.db import models


#### Managers

class PublishedManager (models.Manager):
    #def get_query_set(self):
    #    return super(PublishedManager, self).get_query_set().filter (published=True)
    #
    # a better approach: https://github.com/pullswitch/django-checkout/blob/master/checkout/models.py

    def published (self):
        return self.filter (published=True)

    def unpublished (self):
        return self.filter (published=False)
