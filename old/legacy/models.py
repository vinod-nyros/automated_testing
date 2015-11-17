# -*- coding: utf-8 -*-

from django.db import models
#from django.utils.encoding import smart_unicode, force_unicode, smart_str
#from django.core.exceptions import ImproperlyConfigured
#from django.utils.safestring import mark_safe
#from django.template.defaultfilters import slugify

#from taggit.managers import TaggableManager

#from utils import minitags as tags  # import dropdown  #, ul, li
#from utils.minitags2 import TagStream
#from utils.tagstream22 import TagStream as TagStream22
#from utils.tagstream24_5 import TagStream as TagStream24_5
#from utils import spreadto5
#from utils.managers import PublishedManager


#### globals

trace = 0


#### Postgres "UI"-related tables - pitched 3/25/12 - implem & use my AutoAdmin tables!
# [ removed ]


#### eRacks db Views - convenience models, updates will fail

# THIS IS A VIEW!  DO NOT LET SOUTH DELETE IT! 7/8/11 JJW
class Costspersku(models.Model):
    sku = models.CharField(max_length=50)
    defaultcost = models.FloatField()
    class Meta:
        db_table = u'costspersku'

# THIS IS A VIEW!  DO NOT LET SOUTH DELETE IT! 7/8/11 JJW
class Optchoices(models.Model):
    optid = models.IntegerField()
    choiceid = models.IntegerField()
    class Meta:
        db_table = u'optchoices'
        verbose_name = 'Optchoices View'
        verbose_name_plural = 'Optchoices View'


#### Managers - also exposed in the templates :)
#
#class CateogoryProductManager (models.Manager):
#   by_category
#
#    def published (self):
#        return self.filter (published=True)


new_ChoiceOption='''
class ChoiceOption (models.Model):  # from Wilder Ranch insight 7/9/11
    # NEW Sun 7/10/11
    name = models.CharField(max_length=50, blank=True, help_text='Name to display in config grid - blank uses the Option name by default.')
    #this belongs on Option:
    #description = models.CharField(max_length=100, blank=True, help_text='Name to display in config grid - blank uses the Option name by default.')
    qty = models.IntegerField(default=1, help_text='Number of lines of this option to display in config grid. Defaults to 1.')
    single = models.BooleanField (default=False, help_text='If checked, there are no OptionChoices, the defaultchoice is the only possible choice.')
    allowed_quantities = models.CommaSeparatedIntegerField (max_length=100, help_text='Comma-separated list of integers, eg "1,2,4" etc.')
    required = models.IntegerField (default=0, help_text='Required number of this option - if >0, this option will not have a "none" choice.  If 0, a "none" choice will be available.')

    choice = models.ForeignKey(Choice) # , db_column='productid')
    option = models.ForeignKey(Option) # , db_column='optionid')
    defaultchoice = models.ForeignKey(Choice, default=get_none_choice) # , db_column='defaultchoiceid')  # default='TBD',null=True, blank=True

    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__ (self):
        return '%s: %s' % (self.choice, self.option)
'''


#### Lesser or as-yet-unused eRacks production tables

# deleted 7/16/12 JJW, moved to customers
#class Addresses(models.Model): # Should move this to customers app, or use satchmo contacts
#    id = models.IntegerField(primary_key=True)
#    customerid = models.IntegerField()
#    address1 = models.CharField(max_length=50)
#    address2 = models.CharField(max_length=50)
#    name = models.CharField(max_length=50)
#    city = models.CharField(max_length=50)
#    state = models.CharField(max_length=50)
#    zip = models.CharField(max_length=50)
#    country = models.CharField(max_length=50)
#    phone = models.CharField(max_length=50)
#    email = models.CharField(max_length=50)
#    type = models.CharField(max_length=50)
#    #dt = models.DateTimeField()
#    created = models.DateTimeField(auto_now_add=True)
#    updated = models.DateTimeField(auto_now=True)
#
#    class Meta:
#        db_table = u'addresses'


class Emails(models.Model):
    #id = models.IntegerField(primary_key=True)
    customerid = models.IntegerField()
    orderid = models.IntegerField()
    dt = models.DateTimeField()
    email = models.TextField()

    class Meta:
        db_table = u'emails'


class Creditcards(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    creditcardtype = models.CharField(max_length=50)
    number = models.IntegerField()
    expiry = models.DateTimeField()
    dt = models.DateTimeField()
    customerid = models.IntegerField()

    class Meta:
        db_table = u'creditcards'

class Items(models.Model):
    id = models.IntegerField(primary_key=True)
    serial = models.IntegerField()
    productid = models.IntegerField()
    dt = models.DateTimeField()
    orderid = models.IntegerField()
    shippingmethod = models.CharField(max_length=50)
    shippingcost = models.FloatField()
    trackingnum = models.CharField(max_length=50)
    dtprocessed = models.DateTimeField()
    state = models.CharField(max_length=50)
    price = models.FloatField()
    cost = models.FloatField()
    linenum = models.IntegerField()
    hours = models.IntegerField()
    warranty = models.CharField(max_length=50)
    comment = models.TextField()

    class Meta:
        db_table = u'items'


class Issues(models.Model):
    id = models.IntegerField(primary_key=True)
    customerid = models.CharField(max_length=50)
    issue = models.CharField(max_length=50)
    open = models.TextField() # This field type is a guess.
    dt = models.DateTimeField()
    consultant = models.CharField(max_length=50)
    emailid = models.IntegerField()

    class Meta:
        db_table = u'issues'


class Itemcomponents(models.Model):
    id = models.IntegerField(primary_key=True)
    itemid = models.IntegerField()
    serial = models.IntegerField()
    choiceid = models.IntegerField()
    dt = models.DateTimeField()
    comment = models.TextField()
    price = models.FloatField()
    hours = models.IntegerField()

    class Meta:
        db_table = u'itemcomponents'


#### Set up single-seq tables (org fm legacy eracks db - all db id's in one sequence)
'''
from django_eracks.apps import helpers
from django.db.models.signals import pre_save

pre_save.connect (helpers.presave, sender=Product)
pre_save.connect (helpers.presave, sender=Prodopt)
pre_save.connect (helpers.presave, sender=Prodoptchoice)
pre_save.connect (helpers.presave, sender=Option)
pre_save.connect (helpers.presave, sender=Choice)
pre_save.connect (helpers.presave, sender=ChoiceCategory)
pre_save.connect (helpers.presave, sender=Categories)
pre_save.connect (helpers.presave, sender=Image)
#pre_save.connect (helpers.presave, sender=OptionChoice or ChoiceOption)
'''


## admin moved to admin.py 7/6/11 JJW
