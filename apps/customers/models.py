from django.db import models
from django.contrib.auth.models import User

from apps.utils.managers import PublishedManager

#from filer.fields.image import FilerImageField
from filebrowser.fields import FileBrowseField
from django_countries.fields import CountryField
from userena.models import UserenaBaseProfile
from statecodes import statelist


#### Globals

trace = 0


#### Model classes

#class UserenaProfile (UserenaBaseProfile):
#    user = models.OneToOneField (User, unique=True)  # , verbose_name=_('user'), related_name='my_profile')

class Customer(UserenaBaseProfile):
    user = models.OneToOneField (User, unique=True)  # , verbose_name=_('user'), related_name='my_profile')
#class Customer(models.Model):
#    user        = models.ForeignKey (User, null=True)
    organization = models.CharField (max_length=80,  blank=True, help_text="Company, School, University, Non-profit organization, club, etc")
    title       = models.CharField (max_length=80,  blank=True, help_text="Title at the organization")
    department  = models.CharField (max_length=80,  blank=True, help_text="Department within the organization")
    email       = models.CharField (max_length=160,             help_text="Primary eMail address")
    email2      = models.CharField (max_length=160, blank=True, help_text="Alternate eMail address")
    phone       = models.CharField (max_length=40,              help_text="Primary phone number with area code (and country code if not US)")
    phone2      = models.CharField (max_length=40,  blank=True, help_text="Alternate phone number")

    comments    = models.TextField     (blank=True, help_text="Internal notes, customer comments, record of phone conversations")
    created     = models.DateTimeField  (auto_now_add=True)
    updated     = models.DateTimeField  (auto_now=True)
    published   = models.BooleanField (default=True, help_text='Use this for mailing list opt-out')
    #maillist = models.IntegerField(editable=False)     # Although was originally envisioned as a FK

    class Meta:
        db_table = u'customers'

    def __unicode__ (self):
        return self.organization or self.user.username

    def name (self):
        names = []

        if self.user.first_name:
            names.append (self.user.first_name)

        if self.user.last_name:
            names.append (self.user.last_name)

        return ' '.join (names)
        # nfg, leaves space: '%s %s' % (self.user.first_name, self.user.last_name)

    def default_shipping (self):
        addrs = self.address_set.filter (type__in=['shipping','both'])
        if addrs:
            #assert len (addrs) == 1, 'Too Many shipping addresses returned'
            if len (addrs) >= 1: print 'WARNING: Too Many shipping addresses returned:', addrs
            return addrs [0]

    def default_billing (self):
        addrs = self.address_set.filter (type__in=['billing','both'])
        if addrs:
            #assert len (addrs) == 1, 'Too Many billing addresses returned'
            if len (addrs) >= 1: print 'WARNING: Too Many billing addresses returned:', addrs
            return addrs [0]

    #default_shipping = models.ForeignKey ("Address", related_name='customer_default_shipping', help_text="Default shipping address")
    #default_billing  = models.ForeignKey ("Address", related_name='customer_default_billing', help_text="Default billing address")

    #legacy:
    #primarybilling = models.IntegerField(editable=False) # was originally envisioned as a FK
    #primaryshipping = models.IntegerField(editable=False) # was originally envisioned as a FK
    #primarycreditcard = models.IntegerField(editable=False) # was originally envisioned as a FK


class CustomerImage (models.Model):
    #image       = models.ImageField (upload_to = 'images/customers/')
    #image2      = FilerImageField (null=True, blank=True)
    image       = FileBrowseField (max_length=200, directory="images/customers/") #, extensions=[".jpg",".jpeg",".png",".gif"]) #, blank=True, null=True)
    customer    = models.ForeignKey (Customer, null=True, blank=True)
    link        = models.URLField()
    title       = models.CharField (max_length = 100, blank=True)
    caption     = models.CharField (max_length = 100)
    location    = models.CharField (max_length = 100)
    sortorder   = models.IntegerField (default=100)

    created     = models.DateTimeField (auto_now_add=True)
    updated     = models.DateTimeField (auto_now=True)
    published   = models.BooleanField (default=True)

    objects     = PublishedManager()

    def __unicode__ (self):
        return self.caption

    class Meta:
        ordering = ["sortorder"]
        # db_table = u'categories_products'


class Testimonial (models.Model):
    quote       = models.TextField (help_text="Don't include quotes or italics. Some limited html OK.")
    attribution = models.TextField (help_text="Generally just initials, city, and compeny (Link and some html OK)")
    sortorder   = models.IntegerField (default=100)

    created     = models.DateTimeField (auto_now_add=True)
    updated     = models.DateTimeField (auto_now=True)
    published   = models.BooleanField (default=True)

    objects     = PublishedManager()

    class Meta:
        ordering = ["sortorder"]


# added 7/1612 JJW

address_types = (
    ('shipping','Shipping'),
    ('billing','Billing'),
    ('both','Both shipping and billing'),
    ('other','Alternate address'),
)

# - named addresses like amazon, plus checkboxes for primary/default shipping, billing ('must match ccard')
# "name, for future reference"
# address_nickname
#
# also need 'readonly' flag for once an order is shipped

class Address (models.Model):
    customer    = models.ForeignKey(Customer)
    nickname    = models.CharField(max_length=80,  blank=True,  help_text='Address nickname/description - home, office, manufacturing, etc')
    #description = models.CharField(max_length=80,  blank=True,  help_text='Description - home, office, manufacturing, etc')
    name        = models.CharField(max_length=80,  help_text='Name (if different than above)')
    #organization = models.CharField(max_length=80,  blank=True,  help_text='Organization (if different than above)')
    address1    = models.CharField(max_length=80,               help_text='Street name & number')
    address2    = models.CharField(max_length=80,  blank=True,  help_text='Apt, suite, additional info')
    city        = models.CharField(max_length=80,               help_text='City, town, village, etc')
    state       = models.CharField(max_length=50, choices=statelist, help_text='State, Province, or region')
    zip         = models.CharField(max_length=20,               help_text='Zip or postal code')
    #country     = models.CharField(max_length=80,               help_text='Choose your country')
    country     = CountryField (default='US',                   help_text='Choose your country')
    phone       = models.CharField(max_length=20,  blank=True,  help_text='Phone number for this address, if different from primary')
    email       = models.CharField(max_length=100, blank=True,  help_text='email address for this address, if different from primary')
    type        = models.CharField(max_length=50,  choices=address_types, help_text='Address type - choose, or use nickname if "other"')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published   = models.BooleanField (default=True, help_text="Use this to unpublish, don't delete")

    def __unicode__(self):
        return "%s %s%s %s, %s, %s %s" % (self.name, self.address1, self.address2, self.city, self.state, self.zip, self.country)

    def is_shipping (self):
        return self.type in ['shipping', 'both']

    def is_billing (self):
        return self.type in ['billing', 'both']


#### Forms

# http://djangosnippets.org/snippets/747/ - removed

from django import forms
#from django.forms import widgets
#from django.utils.safestring import mark_safe
#from django.utils.datastructures import MultiValueDict
#from django.forms.util import flatatt

from apps.utils import TemplateForm


class UserForm (TemplateForm):
    template = '_checkout_form.html'
    header = 'Complete your user info as needed'

    class Meta:
        model = User
        fields = ['first_name','last_name','email']  # '__all__'
        # nfg: readonly_fields = ['username']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        #f = self.fields.get('user_permissions', None)
        #if f is not None:
        #    f.queryset = f.queryset.select_related('content_type')


class AddressForm(TemplateForm):
    template = '_checkout_form.html'

    # use form.has_changed!
    #def is_blank (self):
    #    pass

    state = forms.ChoiceField (label='State', initial="Please Select", choices=statelist, help_text="State, province, or region")
    #    widget=forms.RadioSelect, choices=shipping_payments,

    @property
    def header (self):
        rslt = 'Enter your %s address' % self.prefix
        if self.prefix == 'billing':
            rslt += ' (if different than shipping)'
        return rslt

    class Meta:
        model = Address
        exclude = ('customer', 'type', 'description', 'published', 'nickname', 'phone', 'email')  #, 'comment', 'status', 'processed')


class BillingAddressForm(AddressForm):
    prefix = 'billing'  # doesn't work, still have to pass it in

    # only works if  as_table called before is_valid, which only covers 2 out of 3 use cases:
    #def handle_required_fields (self):
    #    for field in self.fields.values():
    #        field.required = False

    def is_empty (self):   # custom, to handle fields with defaults, eg, US for country :)
        for name, field in self.fields.items():
            if name in ['name','address1','address2','city','zip']:
                if trace: print '"%s"' % self [name].value()
                if self [name].value():
                    return False
        return True

    # yuk - django forms suck - have to restate help_text, choices, etc
    name        = forms.CharField(required = False, help_text='Name (if different than above)')
    address1 = forms.CharField (required = False, help_text='Street name & number')
    city     = forms.CharField (required = False, help_text='City, town, village, etc')
    state    = forms.ChoiceField (required = False, choices=statelist, help_text='State, Province, or region')
    zip      = forms.CharField (required = False, help_text='Zip or postal code')


class CustomerForm(TemplateForm):
    template = '_checkout_form.html'
    header = 'Complete your customer info as needed'
    columns = 3

    class Meta:
        model = Customer
        # nope, can't do that: readonly = ('user', )
        exclude = ('user', 'mugshot', 'privacy', 'comments', 'published', 'default_shipping', 'default_billing')



#### Set up single-seq tables (org fm legacy eracks db)

#module_initialized = False
#
#if not module_initialized:
#print "INITIALIZING CUSTOMER MODULE", __name__, __file__
#module_initialized = True

from apps import helpers
from django.db.models.signals import pre_save

#pre_save.connect (helpers.presave, sender=UserenaProfile)
pre_save.connect (helpers.presave, sender=Customer)
pre_save.connect (helpers.presave, sender=CustomerImage)
pre_save.connect (helpers.presave, sender=Testimonial)
pre_save.connect (helpers.presave, sender=Address)


#### NO: see below: Set up Customer model as UserProfile

# let's not do this yet, 4/22/12 JJW - see notes for today

#from django.db.models.signals import post_save
#
#def create_user_profile (sender, instance, created, **kwargs):
#    if created:
#        Customer.objects.create (
#            user = instance,
#            email = instance.email or instance.username,
#            comments = 'Created by create_user_profile',
#        )
#
#post_save.connect(create_user_profile, sender=User)


####  Set up UserenaProfile to auto-create:

from django.db.models.signals import post_save

def create_user_profile (sender, instance, created, **kwargs):
    if created:
        #profile = UserenaProfile.objects.create (user=instance)
        profile = Customer.objects.create (user=instance)
        #instance.username = '%s%s' % (instance.email.split ('@')[0], profile.id)
        #instance.save()
        from userena.models import UserenaSignup
        print 'Checking permissions:', UserenaSignup.objects.check_permissions()

post_save.connect(create_user_profile, sender=User)
