#from django.db import models

'''
lastmodule.models.py

NOTE:  the code to unregister / reregister the admin instance MUST be in admin.py, and NOT in here -

The code in here is loaded at launch, which then registers the Admin site, and bombs on a duplicate in Userena -

this MUST be empty, and the unreg/rereg in admin, so it gets called lazily from admin.autodiscover, which is called from urls.py, *after* the first web hit

Sigh.

JJW

Old, WRONG attempt:

from django.contrib import admin
from django.contrib.admin.sites import NotRegistered

from customers.models import Customer
from customers.admin import CustomerAdmin


try:
    print 'UNREGISTER', admin.site.unregister (Customer)
except NotRegistered, e:
    print e

print 'REREGISTER', admin.site.register (Customer, CustomerAdmin)
'''