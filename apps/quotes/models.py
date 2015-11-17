# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import smart_unicode, force_unicode, smart_str
from django.contrib.auth.models import User

#from customers.models import Customer  # non-full-path import causes double-import
from customers.models import Customer
from filebrowser.fields import FileBrowseField

trace = 0

moved_to_customers='''
class Customer(models.Model):  # Should move this to cutomers app, along w/Addresses
    #id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=80)
    # company_name?! contact?!
    title = models.CharField(max_length=80, blank=True)
    dept = models.CharField(max_length=80, blank=True)
    email = models.CharField(max_length=160)
    email2 = models.CharField(max_length=160, blank=True)
    phone = models.CharField(max_length=40)
    phone2 = models.CharField(max_length=40, blank=True)
    shipping_address = models.TextField()
    billing_address = models.TextField(help_text='leave blank for same', blank=True)

    #legacy:
    maillist = models.IntegerField(editable=False)  # was originally envisioned as a FK - chg to Bool?
    primarybilling = models.IntegerField(editable=False) # was originally envisioned as a FK
    primaryshipping = models.IntegerField(editable=False) # was originally envisioned as a FK
    primarycreditcard = models.IntegerField(editable=False) # was originally envisioned as a FK

    comment = models.TextField()
    #dt = models.DateTimeField(auto_now=True)
    created = models.DateTimeField (auto_now_add=True)
    modified = models.DateTimeField (auto_now=True)

    def __unicode__ (self): return self.name

    class Meta:
        db_table = u'customers'
'''


class Quote(models.Model):
    customer        = models.ForeignKey (Customer,  blank=True, null=True, help_text='click "+" to create new')  # blank/null ==> quote template
    quote_number    = models.CharField (max_length=20, unique=True, help_text='eRacks quote id - letters/numbers/underscore/dashes ok, no spaces')
    approved_by     = models.ForeignKey (User, default=2,       help_text='Manager or admin person approving quote') # should check for is_staff
    valid_for       = models.IntegerField (default=10,              help_text='Number of days the quote is valid for') # or valid_through!
    purchase_order  = models.CharField (max_length=20, blank=True,  help_text='Customer Purchase Order number, etc')
    customer_reference = models.CharField (max_length=200, blank=True, help_text="Other customer reference number, RFQ, contact name, etc")
    comments    = models.TextField     (blank=True, default="", help_text="comments for quotes ")
    # image       = models.ImageField (max_length=100, blank=True, null=True, upload_to='images/quotes/')
    image       = FileBrowseField (max_length=200, directory="images/products/", blank=True, null=True)
    terms           = models.CharField (max_length=20, default='ccard', help_text='Net 5, Wire Transfer, ccard, etc')
    discount        = models.FloatField(blank=True, default=0,      help_text='Dollars or percent, according to type')
    discount_type   = models.CharField (max_length=1, blank=True, default='$', choices=(('$', 'Dollars'),('%','Percent')))
    shipping        = models.FloatField(blank=True,                 help_text='Estimated weight - lbs')
    shipping_method = models.CharField (max_length=40, blank=True,  help_text='UPS, FedEx, Freight, 3-Day, etc')
    target          = models.FloatField(help_text="The customer's budget, or where the customer would like the quote to be")
    # closed = models.BooleanField()
    # notes = models.TextField(help_text="Internal notes and comments on this quote")

    created = models.DateTimeField (auto_now_add=True)
    modified = models.DateTimeField (auto_now=True)

    def __unicode__ (self): return str(self.quote_number)
    def is_template (self): return self.customer is None

    def get_absolute_url (self):
        return self.url

    @property
    def url (self):
        from django.core.urlresolvers import reverse
        return reverse ('quotes.views.quote', args=[str(self.quote_number)])
        #return "/quotes/%s" % self.quote_number

    @property
    def totprice (self):
        return sum ((line.price*line.quantity for line in self.quotelineitem_set.all()))

    @property
    def totqty (self):
        return sum ((line.quantity for line in self.quotelineitem_set.all()))

    @property
    def summary (self, separator='<br>'):
        return separator.join (
            ('Line: %s Qty: %s Model: %s%s%s' % (num+1, line.quantity, line.model, separator, line.description.replace ('\n', separator))
                    for num, line in enumerate (self.quotelineitem_set.all())
            )
        )

    @property
    def header_items (self, separator='<br>'):
        items = []
        if self.customer:
            items.append ('Quote for %s' % self.customer)
        if self.valid_for:
            items.append ('Valid for %s days' % self.valid_for)
        if self.purchase_order:
            items.append ( 'Purchase Order # %s' % self.purchase_order)
        if self.customer_reference:
            items.append ('Customer Reference # %s' % self.customer_reference)
        if self.approved_by:
            items.append ('Approved by: %s' % self.approved_by)
        if self.discount:
            items.append ('Discount: %0.2f %s' % (self.discount, self.discount_type))
        if self.terms:
            items.append ('Terms: %s' % self.terms)
        return separator.join (items)

    #class Meta:
    #    db_table = u'quotes'


class QuoteLineItem(models.Model):
    quote = models.ForeignKey(Quote)
    #item = 		# generate in template or view
    model = models.CharField (max_length=60, help_text='eRacks Model name, eg "OPTERNATOR", or make one up for custom quotes')
    quantity = models.IntegerField()
    comments    = models.TextField(blank=True, default="", help_text="comments for quote line item ")
    shipping    = models.FloatField(blank=True, default=45, help_text='Estimated weight - lbs')
    description = models.TextField(help_text='Start with a line for general description, then one config item per line for components')
    image       = FileBrowseField (max_length=200, directory="images/products/", blank=True, null=True)
    cost = models.FloatField(help_text="our cost")
    price = models.FloatField(help_text="customer price")

    created = models.DateTimeField (auto_now_add=True)
    modified = models.DateTimeField (auto_now=True)

    def __unicode__ (self): return '%dx%s' % (self.quantity,self.model)

    #class Meta:
    #    db_table = u'quote_lineitems'


### set up single-seq tables (org fm legacy eracks db)

#module_initialized = False
#
#if not module_initialized:
#print "INITIALIZING QUOTE MODULE"
#module_initialized = True

from apps import helpers
from django.db.models.signals import pre_save

pre_save.connect (helpers.presave, sender=Quote)
#pre_save.connect (helpers.presave, sender=Customer)
pre_save.connect (helpers.presave, sender=QuoteLineItem)
