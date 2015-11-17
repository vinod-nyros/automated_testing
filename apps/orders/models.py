# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

#from utils.managers import PublishedManager
from catax.models import Catax


#### globals, choices

trace = 0

order_statuses = (
    ('new', 'New'),
    ('verified', 'Verified'),
    ('canceled', 'Canceled'),
    ('fraud', 'Fraud'),
    ('invalid', 'Invalid'),
    ('test', 'Test'),
    ('open', 'Open'),
    ('inprogress', 'In Progress'),
    ('shipped', 'Shipped'),
    ('paid', 'Paid'),
    ('shippedandpaid', 'Shipped and Paid'),
    ('returned', 'Returned'),
    ('repair', 'In for repair'),
    ('closed', 'Closed'),
    # see zope admin
)

old_from_zope='''
    open
    approved
    charged
    awaitingwire
    funded
    hold
    parts
    picked
    production
    assembled
    testing
    burnin
    tested
    software
    OSInstall
    test
    fraud
    invalid
    shiphold
    partial
    shipped
    dropshipped
    invoiced
    paid
    canceled
    closed
    RMA
    returned
'''

shipping_methods_with_multiplier = (
    ( "('Ground',1.0)", 'Ground'),  # note about insured - disclaimer for insurance claim process!
    ( "('3day',1.8)",   '3-day'),
    ( "('2day',2.4)",   '2-day'),
    ( "('1day',3.5)",   'Next Day'),
    ( "('1dayAM',4.5)",   'Next Day AM'),
    ( "('IntlEcon',7.0)",  'International Economy (5-7 days)'),
    ( "('IntlExpr',15.0)",  'International Express (2-3 days)'),
    ( "('Freight',1.0)", 'Freight'),  # note about insured - disclaimer for insurance claim process!
    ( "('Willcall',0.0)", 'Will Call')
)

shipping_methods = (
    ("ground",    'Ground'),
    ("3day",      '3-day'),
    ("2day",      '2-day'),
    ("1day",      'Next Day'),
    ("1dayAM",    'Next Day AM'),
    ("IntlEcon",  'International Economy (5-7 days)'),
    ("IntlExpr",  'International Express (2-3 days)'),
    ("freight",   'Freight'),
    ("willcall",  'Will Call'),
)

preferred_shippers = (
    ('Any', 'No Preference'),
    ('UPS', 'UPS'),
    ('FedEx', 'FedEx'),
    ('DHL', 'DHL'),
    ('Aero', 'Aero Logistics'),
    ('Airborne', 'Airborne'),
    ('USPS', 'US Postal Service (International only)'),
    ('BAX', 'BAX Global'),
    ('None', 'None (Will Call)'),
    ('Other', 'Other (enter in "Special Instructions" field)')
)

from_zope_circa_2005_6='''
    abf_pro (ABF Freight Pro)
    aero (Aero Logistics)
    dhl (DHL)
    fedex1a (FedEx Priority Overnight)
    fedex1p (FedEx Standard Overnight)
    fedex2 (FedEx 2-Day)
    fedex3 (FedEx 3-Day)
    fedexGR (FedEx Ground / Residential)
    redstar (USF RedStar)
    ups3day (UPS 3-Day Select)
    upsblue (UPS Blue 2-Day)
    upsground (UPS Ground)
    upsred (UPS Red Overnight)
    usps_express (USPS Postal Express International 2-3 day)

    later add tracking URL, etc -
'''


referral_types = (
    ('', 'Please Select'),
    ('google', 'Google search'),
    ('googlead', 'Google Ad'),
    ('yahoo', 'Yahoo'),
    ('Facebook','Facebook'),
    ('Twitter','Twitter'),
    ('YouTube','YouTube'),
    ('Online Web magazine','Online Web magazine(please enter it below)'),
    ('Phoronix','Phoronix'),
    ('search', 'Other search engine (please enter below)'),
    ('Github','Github(Please enter who below)'),
    ('The Var Guy top 50','The Var Guy top 50'),
    #('dir', 'Web Directory (dmoz, Yahoo dir, etc - enter below)'),
    ('press', 'Press release'),
    ('repeat', 'Repeat business'),
    ('referral', 'Referral or word-of-mouth (please enter below)'),
    ('flyer', 'Brochure or flyer (please enter promo code below)'),
    ('conf', 'Conference or Trade Show (please enter below)'),
    ('list', 'Mailing list or newsgroup (please enter below)'),
    ('project', 'Open-Source site (OpenBSD, Zope, etc - enter below)'),
    ('mag', 'Magazine article (please enter mag and month/yr below)'),
    ('magad', 'Magazine ad (please enter mag and month/yr below)'),
    ('blog', 'Link from portal or blog (please enter below)'),
    ('website', 'Other link or website (please enter below)'),
    ('auction', 'Auction site (eBay, UBid, etc - please enter below)'),
    ('other', 'Other - please enter below')
)

shipping_payments = (
    #('included', 'Included - Estimated shipping included with order'),
    #('separate', 'Separate - Actual shipping charged separately (credit card orders only)'),
    #('customer', '3rd party - Bill customer or 3rd-party account number using above shipper',)
    ('included', 'Included - Shipping paid with order'),   # Estimated shipping included with order'),
    ('customer', 'Customer - Bill customer/3rd-party'),
)


payment_methods = (
    ('', 'Please Select'),
    ('byccard', 'Credit Card'),
    ('bycheck', 'Check in Advance'),
    ('bypo',    'Purchase Order'),
    ('bywire',  'Wire Transfer'),
)


payment_terms = (
    ('ccard', 'card ending in'),
    ('cod', "COD Cashier's check"),
    ('check', 'Company check (on approval)'),
    ('internal', 'Internal use'),
    ('net0', 'Net 0'),
    ('net5', 'Net 5'),
    ('net10', 'Net 10'),
    ('net30', 'Net 30'),
    ('po','Purchase Order (requires approval)'),
    ('wire', 'Wire Transfer'),
)


order_sources = (
    ('zope', 'Legacy Zope Order'),
    ('website', 'Website order'),
    ('other', 'Other - see comments'),
)


#### Managers

class OrderManager(models.Manager):

    def open(self):
        return self.filter(status='open')

    def shipped(self):
        return self.filter(status in ['shipped','shippedandpaid'])

    # etc - see https://github.com/pullswitch/django-checkout/blob/master/checkout/models.py


#### Models

'''
class NameValuePair (models.Model):
    name    = models.CharField (max_length=50)
    value   = models.CharField (max_length=100)
    title   = models.CharField (max_length=200)
    description = models.TextField()

    class Meta:
        abstract = True

class ShippingMethod (NameValuePair):
class PreferredShipper (NameValuePair):
class ReferralType (NameValuePair):
'''

columns = '''id title email
shiptype shipname shiporg shipaddr1 shipaddr2 shipcity shipstate shipzip shipcountry shipphone shipper shipmethod shiprate shipcost
billtype billname billaddr1 billaddr2 billcity billstate billzip
paymeth cclast4 ccmonth ccyear ccauthnum cc_cvv cc_corp_pin cc_charged_date cc_initials
instr orderdate orderstatus ordernum internalnotes adjustments adjustamt
tracknumbers shipdate shipinitials'''.split()


## orders imported from Zope summer 2012

class ImportedOrder(models.Model):
    title               = models.CharField (max_length=50, help_text='Order Title - typically an email address')
    email               = models.CharField (max_length=50, help_text='email address for the order - usually matches title')

    shiptype            = models.CharField (max_length=10, help_text='Shipping type - US or Intl')
    shipname            = models.CharField (max_length=80, help_text='Shipping name')
    shiporg             = models.CharField (max_length=80, help_text='Shipping organization', blank=True)
    shipaddr1           = models.CharField (max_length=80, help_text='Shipping address - line 1')
    shipaddr2           = models.CharField (max_length=60, help_text='Shipping address - line 2', blank=True)
    shipcity            = models.CharField (max_length=40, help_text='Shipping city')
    shipstate           = models.CharField (max_length=2,  help_text='Shipping state', blank=True)
    shipzip             = models.CharField (max_length=10, help_text='Shipping zip or postal code', blank=True)
    shipcountry         = models.CharField (max_length=40, help_text='Shipping country', blank=True)
    shipregn            = models.CharField (max_length=30, help_text='Shipping region, province, area, etc', blank=True)
    shipphone           = models.CharField (max_length=20, help_text='Shipping phone #', blank=True)
    shipper             = models.CharField (max_length=15, help_text='Shipper / shipping carrier name', blank=True, choices=preferred_shippers)
    shipmethod          = models.CharField (max_length=10, help_text='Shipping method', choices=shipping_methods)
    #shiprate            = models.FloatField (blank=True,   help_text='Shipping multiplier of base (ground) rate')
    shiprate            = models.CharField (max_length=10, help_text='Shipping multiplier of base (ground) rate', blank=True)
    shipcost            = models.FloatField (              help_text='Shipping cost')
    shippay             = models.CharField (max_length=10, help_text="Shipping payment method - included, or billed to customer's card or account", choices=shipping_payments)
    #shipprice           = models.FloatField (blank=True,   help_text='Shipping price')
    shipprice           = models.CharField (max_length=10, help_text='Shipping price', blank=True)
    shipacct            = models.CharField (max_length=20, help_text="Shipping account number, for shipping billed to customer's account", blank=True)
    #shipincl            = models.FloatField (blank=True,   help_text='Shipping included (not used much)')
    shipincl            = models.CharField (max_length=10, help_text='Shipping included (not used much)', blank=True)

    billtype            = models.CharField (max_length=10, help_text='Billing type - US or Intl', blank=True)
    billname            = models.CharField (max_length=80, help_text='Billing name', blank=True)
    billorg             = models.CharField (max_length=80, help_text='Billing organization', blank=True)
    billaddr1           = models.CharField (max_length=80, help_text='Billing address - line 1', blank=True)
    billaddr2           = models.CharField (max_length=60, help_text='Billing address - line 2', blank=True)
    billcity            = models.CharField (max_length=40, help_text='Billing city', blank=True)
    billstate           = models.CharField (max_length=2,  help_text='Billing state', blank=True)
    billzip             = models.CharField (max_length=10, help_text='Billing zip or postal code', blank=True)
    billcountry         = models.CharField (max_length=20, help_text='Billing country', blank=True)
    billregn            = models.CharField (max_length=30, help_text='Billing region, province, area, etc', blank=True)
    billphone           = models.CharField (max_length=20, help_text='Billing phone #', blank=True)

    billfax             = models.CharField (max_length=20, help_text='Billing fax #', blank=True)
    billinitials        = models.CharField (max_length=10, help_text='Billing employee initials', blank=True)
    billemail           = models.CharField (max_length=50, help_text='Billing email address for the order, if different than main order email', blank=True)
    billsame            = models.CharField (max_length=3,  help_text='Billing address same as shipping address')

    iagree              = models.CharField (max_length=3,  help_text='User has checked the "I Agree" box for the terms and conditions')
    reftyp              = models.CharField (max_length=10, help_text='Referral type for this order', choices=referral_types)
    refsrc              = models.CharField (max_length=100, help_text='Referral source for "other" referral types', blank=True)
    refnum              = models.CharField (max_length=30, help_text='Purchase Order or customer reference number', blank=True)

    approved_date       = models.DateTimeField (           help_text='Date order was approved (not used much)', null=True, blank=True)
    saleinitials        = models.CharField (max_length=10, help_text='Sales employee initials', blank=True)

    paymeth             = models.CharField (max_length=12, help_text='Payment method', choices=payment_methods)
    payterms            = models.CharField (max_length=20, help_text='Payment terms', blank=True, choices=payment_terms)
    payinitials         = models.CharField (max_length=10, help_text='Payment employee initials', blank=True)

    cclast4             = models.CharField (max_length=10, help_text='Credit card - last 4 digits', blank=True)
    ccmonth             = models.IntegerField (            help_text='Credit card expiry date - Month', blank=True, null=True)
    ccyear              = models.IntegerField (            help_text='Credit card expiry date - Year', blank=True, null=True)
    ccauthnum           = models.IntegerField (            help_text='Credit card authorization - confirmation number', blank=True, null=True)
    cc_cvv              = models.CharField (max_length=20, help_text='Credit card - CVV verification code', blank=True)
    cc_corp_pin         = models.IntegerField (            help_text='Credit card - corporate PIN number', blank=True, null=True)
    cc_charged_date     = models.DateTimeField (           help_text='Credit card - Date card was charged (only used in mid-2000s)', blank=True, null=True)
    cc_initials         = models.CharField (max_length=10, help_text='Credit card employee initials', blank=True)

    taxcounty           = models.CharField (max_length=50, help_text='Tax county', blank=True)
    #taxrate             = models.FloatField (blank=True,   help_text='Tax rate')
    taxrate             = models.CharField (max_length=10, help_text='Tax rate', blank=True)
    #salestax            = models.FloatField (blank=True,   help_text='Tax amount (exception - not used much)')
    salestax            = models.CharField (max_length=10, help_text='Tax amount (exception - not used much)', blank=True)

    orderdate           = models.DateTimeField (           help_text='Order date', blank=True, null=True)
    orderstatus         = models.CharField (max_length=15, help_text='Order status', choices=order_statuses)
    ordernum            = models.IntegerField (            help_text='Order number - should match id')
    instr               = models.TextField (blank=True,    help_text='Special instructions for this order')
    internalnotes       = models.TextField (blank=True,    help_text='Internal notes for this order')
    oldnotes            = models.TextField (blank=True,    help_text='Old notes for this order (not used much)')
    adjustments         = models.TextField (blank=True,    help_text='Adjustments, if any, to this order')
    #adjustamt           = models.FloatField (blank=True,   help_text='Adjustment amount')
    adjustamt           = models.CharField (max_length=10, help_text='Adjustment amount', blank=True)
    #costofgoods         = models.FloatField (blank=True,   help_text='Cost of Goods for this order, total')
    costofgoods         = models.CharField (max_length=10, help_text='Cost of Goods for this order, total', blank=True)
    tracknumbers        = models.TextField (blank=True,    help_text='Tracking numbers for this order')
    shipdate            = models.DateTimeField (           help_text='Shipping - Date shipped', null=True, blank=True)
    shipinitials        = models.CharField (max_length=10, help_text='Shipping employee initials', blank=True)

    def name (self):
        return self.shipname or self.billname

    def org (self):
        return self.shiporg or self.billorg

    def name_org (self):
        return self.name or self.org


class ImportedOrderLine(models.Model):
    order               = models.ForeignKey (ImportedOrder, help_text='Parent Order number')
    line                = models.IntegerField (             help_text='Order line item number - matches id')
    title               = models.CharField (max_length=50, help_text='Title - typically the same as Sku')
    sku                 = models.CharField (max_length=50, help_text='Sku - typically the same as Title')
    product             = models.CharField (max_length=50, help_text='Product name - eRacks/<Sku>')
    summary             = models.TextField (blank=True,    help_text='Summary for this line item - changed items')
    qty                 = models.IntegerField (            help_text='Quantity of this line item')
    baseprice           = models.FloatField (              help_text='Base price of system')
    totprice            = models.FloatField (              help_text='Total price of system')
    notes               = models.TextField (blank=True,    help_text='Notes for this line item')
    weight              = models.IntegerField (blank=True, help_text='Weight of this system')
    shipper             = models.CharField (max_length=50, help_text='Name of shipper for this line item', blank=True)
    shipdate            = models.DateTimeField (           help_text='Shipping - Date shipped', null=True, blank=True)
    shipprice           = models.FloatField (blank=True,   help_text='Shipping price of this system / line item', null=True)
    tracknum            = models.CharField (max_length=50, help_text='Tracking number for this line item', blank=True)
    serial              = models.CharField (max_length=50, help_text='Serial number for this line item (Typically the Mac address)', blank=True)
    serials             = models.TextField (blank=True,    help_text='Multiple Serial numbers for this line item (Typically the Mac address)')
    details             = models.TextField (blank=True,    help_text='Detailed / full config dictionary for this system')


## Django-based orders & transferred orders

class Order(models.Model):  # also shipping, customer, address, etc
    customer            = models.ForeignKey ("customers.Customer", related_name='orders')
    reference_number    = models.CharField (max_length=50, blank=True, help_text="Customer Reference Number / Purchase Order Number")
    shipping            = models.DecimalField (decimal_places=2, max_digits=10,         default=0,          help_text='Shipping amount')  # need Shipping table
    shipping_method     = models.CharField (max_length=50, choices=shipping_methods,    default='ground',   help_text='Choose preferred shipping method & speed')
    preferred_shipper   = models.CharField (max_length=50, choices=preferred_shippers,  default='Any',      help_text='Choose your preferred shipper')
    shipping_payment    = models.CharField (max_length=80, choices=shipping_payments,   default='included', help_text='Choose shipping payment method (Put account number & details in "Special Instructions" below as needed)')
    referral_type       = models.CharField (max_length=80, choices=referral_types,      default='Please Select', help_text='How did you hear of us?')
    referral_source     = models.CharField (max_length=80, blank=True, help_text='Please specify if Referral Type is "Other"')
    special_instructions= models.TextField (blank=True,	    help_text='Customer special instructions for this order - shipping, build, options, etc')
    cart                = models.TextField (blank=True,     help_text='Serialized copy of shopping cart at time of purchase')

    california_tax      = models.ForeignKey (Catax, null=True, blank=True, verbose_name='Sales Tax (CA Only)', help_text='California shipments please choose county/city')
    ship_to_address     = models.ForeignKey ("customers.Address", related_name='order_ship_to', help_text='Ship to this address')
    bill_to_address     = models.ForeignKey ("customers.Address", related_name='order_bill_to', help_text='Bill to this address')

    agree_to_terms      = models.BooleanField (default=False, help_text='Customer agreed to terms and accepted EULA')

    comment             = models.TextField (blank=True, help_text='Internal comments on this order')
    status              = models.CharField (max_length=50, choices=order_statuses, help_text='Order status')
    source              = models.CharField (max_length=50, choices=order_sources, default='website', help_text='Source of order - Website, Imported Zope order, Phone, etc')

    created             = models.DateTimeField(auto_now_add=True)
    updated             = models.DateTimeField(auto_now=True)
    processed           = models.DateTimeField(blank=True, null=True)  # is this needed? JJW Jul 19, 2012

    #published          = models.BooleanField(default=True)  #use the status field instead
    #tax                = models.DecimalField (max_digits=10, decimal_places=2, default=0)
    #returned           = models.TextField()  # make this a status
    #price              = models.DecimalField()

    objects = OrderManager()

    def __unicode__(self):
        if self.customer:
            #return "Order #{0}: {1}".format(self.id, self.customer)  #self.user.get_full_name())
            return "Order #%s: %s" % (self.id, self.customer)  #self.user.get_full_name())

        #return "Order#{0}".format(self.id)
        return "Order #%s" % self.id


    class Meta:
        db_table = u'orders'


class OrderPayment (models.Model):
    '''
    Method of Payment - added whenever a payment is made, partial or in full.

    See also paymeth* and cc_* fields from ImportedOrder

    Note that PO number belongs on the Order - it's needed before the payment method
    Invoice number?  this is really an accountng function

    Check number, though, maybe - wire transfer advice number too TT/PI, etc

    NOTE 1/5/13 JJW:  Shouldn't we keep adress, zip, name_on_card, here, too? it goes with the ccard charge..
    '''
    order               = models.ForeignKey (Order, help_text='Order number')
    payment_method      = models.CharField (max_length=12, help_text='Payment method', choices=payment_methods, default='Please Select')
    payment_terms       = models.CharField (max_length=20, help_text='Payment terms', blank=True, choices=payment_terms)

    last_4              = models.CharField (max_length=10, help_text='Credit card - last 4 digits', blank=True)
    expiry_date         = models.DateField (               help_text='Credit card expiry date - MMYY', blank=True, null=True)
    #expiry_month        = models.IntegerField (            help_text='Credit card expiry date - Month', blank=True, null=True)
    #expiry_year         = models.IntegerField (            help_text='Credit card expiry date - Year', blank=True, null=True)
    auth_num            = models.IntegerField (            help_text='Credit card authorization - confirmation number', blank=True, null=True)
    # n cc_cvv              = models.CharField (max_length=20, help_text='Credit card - CVV verification code', blank=True)
    # n cc_corp_pin         = models.IntegerField (            help_text='Credit card - corporate PIN number', blank=True, null=True)
    # see created/updated fields - cc_charged_date     = models.DateTimeField (           help_text='Credit card - Date card was charged (only used in mid-2000s)', blank=True, null=True)
    # y (user) cc_initials         = models.CharField (max_length=10, help_text='Credit card employee initials', blank=True)
    user                = models.ForeignKey (User, help_text='Customer username or employee processing payment')  # formerly payinitials & cc_initials both
    comments            = models.TextField (blank=True, help_text='Comments on this payment')
    created             = models.DateTimeField(auto_now_add=True)
    updated             = models.DateTimeField(auto_now=True)

    def expiry_mmyy (self):
        return self.expiry_date.strftime ('%m%y')

    def __unicode__ (self):
        return ('Order #%s %s payment' % (self.order.id, self.payment_method))


# class OrderShipment
# tracking_number, payment, line item, shipping address, etc

#class OrderCogs
#    fk to order line - m21

'''
class OrderStatusChange (models.Model):
    old_status          = models.CharField (max_length=50, choices=order_statuses, help_text='Order status before this change')
    new_status          = models.CharField (max_length=50, choices=order_statuses, help_text='Order status after this change')
    initials            = models.CharField (max_length=10, help_text='Employee initials')

    comments            = models.TextField (blank=True, help_text='Comments on this status change')
    created             = models.DateTimeField(auto_now_add=True)
    updated             = models.DateTimeField(auto_now=True)
'''

from_zope_order='''
    title email
    paymeth y
    reftyp y
    shiptype
    iagree
    billsame
    ccmonth
    shipcity
    shipzip
    shipmethod
    shiprate
    shipcost
    email
    ccyear
    refnum
    shipaddr1
    shipaddr2
    shipname
    shipstate
    shippay
    shipper
    refsrc
    cc_cvv
    cclast4
    shipcountry
    billtype
    orderdate
    ccauthnum
    adjustments
    internalnotes
    adjustamt
    orderstatus
    index
    ordernum
'''

from_zope_order_lineitem='''
    title
    sku
    product
    summary
    qty
    baseprice
    totprice
    notes
    weight
    shipper
    tracknum
    index
    serial
'''

from_checkout9_and_current_checkout_pages='''
shipping address:
Full Name       Person's full name to ship to
Organization        Organization, blank if none
eMail address       Complete eMail address (name@domain.com)
Phone number        Phone number with area code(required for expedited shipping)
Address 1       Shipping address (number, street)
Address 2       Suite, dept, mail drop, or add'l info
City        City name
Zip Code        Zip or Postal Code
US  State:
Int'l   Country:
Province/Region:
Billing is same     My billing / credit card information is the same as my shipping information
'''

#### Forms

from django import forms
#from django.forms import ModelForm
from apps.utils import TemplateForm


class OrderForm(TemplateForm):
    template = '_checkout_form.html'
    header = 'Enter your order info'

    # bug: 'required' not picked up on bool field, even though blank is False.
    agree_to_terms = forms.BooleanField (label='Agree to terms', required=True, help_text='You agree to our <a href="/policies/">legal terms and conditions</a>')   # accepted_eula

    class Meta:
        model = Order
        exclude = ('customer', 'shipping', 'comment', 'status', 'processed', 'cart', 'ship_to_address', 'bill_to_address', 'source')
        widgets = { 'shipping_payment': forms.RadioSelect() }


from fields import CreditCardField, ExpiryDateField, VerificationValueField
from apps.utils import ccards

class PaymentForm(TemplateForm):
    template = '_checkout_form.html'
    header = 'Enter your payment info &nbsp; <img src="/images/orders/ccards4.gif" title="We accept Visa/MC/Amex/Discover" />'

    cvv_code    = VerificationValueField (required=False, label="CVV Code",     help_text='3 digits on back for Visa/MC, 4 digits on front for Amex')  # not saved
    card_number = CreditCardField        (required=False, label="Card Number",  help_text='Credit card number - 13-16 digits')  # not saved
    expiry_date = ExpiryDateField        (                label="Expiry Date",  help_text='Credit card expiration date - MMYY')

    def clean_cvv_code (self):
        data = self.cleaned_data['cvv_code']

        if self.cleaned_data.get ('payment_method', '') == 'byccard' and not data:
            raise forms.ValidationError ('Required for payment method of "Credit Card"')

        return data

    def clean_card_number (self):
        data = self.cleaned_data['card_number']

        if trace: print '"%s"' % bool(data), ccards.validate (data), ccards.vendor (data), self.cleaned_data.get ('payment_method', '')

        if self.cleaned_data.get ('payment_method', '') == 'byccard':
            if not data:
                raise forms.ValidationError ('Required for payment method of "Credit Card"')

            vendor = ccards.vendor (data)

            if not ccards.validate (data):
                raise forms.ValidationError ("Invalid %s card number" % vendor)
            elif vendor not in ('MasterCard', 'Visa', 'Amex', 'Discover'):
                raise forms.ValidationError ('We only accept Visa, MasterCard, Discover, and Amex, not ' + vendor)

            # OK if we made it here
            self.last_4 = data [-4:]

        elif data:
            raise forms.ValidationError ('Should be blank unless payment method is "Credit Card"')

        return data  # Always return the cleaned data, whether you have changed it or not.

    class Meta:
        model = OrderPayment
        #exclude = ('payment_terms', 'employee', 'comments', 'created', 'updated', 'auth_num', 'last_4', 'expiry_month', 'expiry_year')
        fields= ('payment_method', 'card_number', 'cvv_code', 'expiry_date')
        #widgets = { 'expiry_date': ExpiryDateField(help_text='Credit card expiration date - MMYY') }


#### Set up single-seq tables (org fm legacy eracks db - all db id's in one sequence)

from apps import helpers
from django.db.models.signals import pre_save

pre_save.connect (helpers.presave, sender=Order)
pre_save.connect (helpers.presave, sender=OrderPayment)

