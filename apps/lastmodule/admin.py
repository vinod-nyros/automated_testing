#from django.db import models

'''
lastmodule.admin.py

This module is here so it loads last, after all the other apps

Please be sure it's in the app list *last* in settings.py

Handy for deregistereing / reregistereing admin modules, for one

NOTE:  This cannot simply go in lastmodule.__init__.py, because admin.py is
*specifically* loaded from admin.site.autodiscover, called from urls.py at the
first web hit (NOT at launch!).

See also the note in models.py

JJW
'''

from django.contrib import admin
from django.contrib.admin.sites import NotRegistered

from customers.models import Customer
from customers.admin import CustomerAdmin


try:
    admin.site.unregister (Customer)
except NotRegistered, e:
    print e

admin.site.register (Customer, CustomerAdmin)
