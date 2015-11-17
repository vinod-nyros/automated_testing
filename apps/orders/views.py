# -*- coding: utf-8 -*-

#import cgi
#from cStringIO import StringIO
from pprint import pformat

from django.shortcuts import render_to_response
from django.template import RequestContext, Template, Context
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.safestring import mark_safe
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ValidationError

#from sx.pisa3 import pisaDocument
from django_xhtml2pdf.utils import generate_pdf

from apps.utils import minitags as tags
from apps.utils import Breadcrumb, unslugify

from home.helpers import SessionHelper

#from orders import templets
from orders.models import OrderForm, ImportedOrder, PaymentForm

from customers.models import UserForm, Customer,CustomerForm, Address,AddressForm, BillingAddressForm


#### Globals

trace = 0
trace_grid = 0
trace_order = 1


#### Utility functions

def add_to_cart (request):  # called from here (deprecating) and from product view with redirect to /cart/, here
  ses = request.session
  post = request.POST #.dict()
  seshelp = SessionHelper (request.session)

  prod = ses.get ('prod', None)

  if prod:
      seshelp.update (request, called_from_cart=True)
      ses ['cart'] = ses.get ('cart', []) + [prod]
      ses ['prod'] = {}


#### utility classes

class Container (object):  # Q & D dict-to-attr converter
  def __init__ (self, data={}):
    self.__dict__ = dict (data)


#### Utility / admin views:

#@user_passes_test(lambda u: u.is_staff)
@login_required
def view_session (request):
    return HttpResponse ('Session:' + pformat (request.session.items()), content_type="text/plain")


default_excluded = ('fraud', 'closed', 'canceled', 'test', 'invalid')

@user_passes_test(lambda u: u.is_staff)
def admin_order_grid (request):
    excluded = request.GET.get ('excluded', default_excluded)

    return render_to_response ('admin_grid.html', dict (
            orders=ImportedOrder.objects.exclude (orderstatus__in=excluded),
        ), context_instance=RequestContext(request))


#### Forms used by customer views
# used model form in Orders


#### Templates

order_email = Template ('''
Order # {{ order.id }}
Name {{ name }}
Addresses {{ addr }}
Ccard # {{ form.card_number }}
Expiry {{ payment.expiry_mmyy }}
CVV # {{ form.cvv_code }}
Amount $ {{ gtts }}
Email {{ email }}


''')



#### Customer views

def cart (request):
    ses = request.session
    post = request.POST #.dict()
    seshelp = SessionHelper (request.session)

    if post:
        if post.get ('add', None):          # check if we have smth to add to ses.cart
            add_to_cart (request)

        elif post.get ('delete', None):     # delete entire cart
            ses ['cart'] = []

        elif post.get ('update', None):     # update quantities in shopping cart
            cart = ses ['cart']
            newqties = post.getlist ('updqty')

            for i, newqty in enumerate (newqties):
                if newqty.isdigit() and int (newqty) != cart [i] ['qty']:
                    if trace_grid: print 'changing line:', i, 'qty', cart [i] ['qty'], 'to', newqty
                    cart [i] ['qty'] = int (newqty)
                    #cart [i] ['extprice'] = int (newqty) * cart [i] ['totprice']

            if trace:
                for num, line in enumerate (cart):
                    print 'line/qty:', num, line ['qty']

            to_delete = reversed([num for num, line in enumerate (cart) if line ['qty'] == 0])

            for num in to_delete:
                if trace_grid: print 'deleting line:', num
                del cart [num]

            ses ['cart'] = cart

    # now display cart fm session - empty cart is handled in template
    cart = ses.get ('cart', None)

    if trace: print pformat (cart)

    return render_to_response('cart.html', dict (
            breadcrumbs=(Breadcrumb ('Cart', 'Your Cart', '/cart/'),),
            summary=seshelp.cart_summary_table(),
            content=seshelp.cart_details(),
            title='Your Cart',
        ), context_instance=RequestContext(request))


from email_extras.utils import send_mail  #, send_mail_template

@login_required
def checkout (request, confirm=False):
    ses = request.session
    seshelp = SessionHelper (ses)
    totqty, grandtot = seshelp.cart_totals() # TODO: convert these legacy references to use the dict retruned from cart_summary
    post = request.POST
    get = request.GET
    user = request.user
    cart = ses.get ('cart')

    if not cart:  # likely landed here from somewhere else, redirect to "Cart is empty" message
        return HttpResponseRedirect ('/cart/')

    if post:
        customer                = ses.get ('customer')
        billing_address         = ses.get ('billing_address')
        shipping_address        = ses.get ('shipping_address')

        if trace_order: print 'POST', customer, billing_address, shipping_address

        user_form               = UserForm (post, instance=user)
        customer_form           = CustomerForm (post, instance=customer)
        order_form              = OrderForm (post)
        shipping_address_form   = AddressForm (post, prefix='shipping', instance=shipping_address)
        billing_address_form    = BillingAddressForm (post, prefix='billing', instance=billing_address)
        payment_form            = PaymentForm (post)

        def cross_form_fdedits():  # must be called after forms are checked
            if shipping_address_form['state'].value() == 'CA' and not order_form['california_tax'].value():
                # this fails on Dj 1.7.x
                #order_form._update_errors ({ 'california_tax': ['CA shipments must choose county'] })
                # nope, this isn't trapped
                #raise ValidationError ('CA shipments must choose county',
                #    code='CA_County_required')
                    #params={ 'california_tax': 'county required' })
                order_form.add_error ( 'california_tax', 'Shipments to CA must choose county')
                return False

            return True

        if (customer_form.is_valid()
                and order_form.is_valid()
                and shipping_address_form.is_valid()
                and (billing_address_form.is_valid() or billing_address_form.is_empty())  # has_changed nfg for choice fields like state
                and payment_form.is_valid()
                and cross_form_fdedits()
            ):
            # Process the forms taking care of proper creation order for FKs
            customer = customer_form.save (commit=False)
            customer.user = user
            ses ['customer'] = customer
            #customer.save()
            if trace: print 'POST CUSTOMER', customer.id, user.id, customer.user_id

            order = order_form.save (commit=False)


            # TODO: compute shipping based on weight, boxes, etc!
            multiplier = 1.0      # TODO: get this from table, above
            #multiplier = totqty  # no - (totqty is the # of line items)

            if order.shipping_payment == "included":
                # Note to Mani & developers: What we should do here is:
                # - ensure the totweight is calculated correctly, including the quantity of each line item
                # - (check also how quotes work too, and ensure the cart is being filled correctly)
                # - in the future, also includ # of packages in the calcualtion, as shipping of each box has a separate cost
                # We could also look into a shipping calcualtion add-on for Django
                shipping = seshelp.cart_summary() ['totweight'] * multiplier
            else:
                shipping = 0.0

            if order.california_tax:
                tax = grandtot * float (order.california_tax.tax)/100
            else:
                tax = 0.0

            order.tax = tax
            order.shipping = str(shipping)
            order.customer = customer
            order.status = 'new'
            order.cart = cart

            shipping_address = shipping_address_form.save (commit=False)
            shipping_address.customer = customer

            if billing_address_form.is_empty():  # not has_changed():
                shipping_address.type = 'both'
                ses ['shipping_address'] = shipping_address
                #shipping_address.save()
                order.bill_to_address = shipping_address
                billing_address = shipping_address
                billing_name = customer.name()
            else:
                shipping_address.type = 'shipping'
                ses ['shipping_address'] = shipping_address
                #shipping_address.save()
                billing_address = billing_address_form.save (commit=False)
                billing_address.customer = customer
                billing_address.type = 'billing'
                ses ['billing_address'] = billing_address
                #billing_address.save()
                order.bill_to_address = billing_address
                if not billing_address.name:
                    billing_address.name = customer.name()
                billing_name = billing_address.name

            order.ship_to_address = shipping_address
            ses ['billing_name'] = billing_name
            ses ['order'] = order
            #order.save()

            payment = payment_form.save(commit=False)
            payment.user = user
            payment.order = order
            payment.last_4 = payment_form.cleaned_data ['card_number'] [-4:]
            payment.payment_terms = payment.payment_method [2:]
            ses ['payment'] = payment
            ses ['payment_data'] = payment_form.cleaned_data
            #payment.save()

            gtts = grandtot + tax + shipping
            ses ['gtts'] = gtts

            if confirm:  # display conf form
                return render_to_response ('confirm.html', dict (
                    breadcrumbs     = ( Breadcrumb ('Checkout', 'Checkout - Enter info', '/checkout/'),
                                        Breadcrumb ('Confirm', 'Confirm your order', '/checkout/confirm/'),
                                      ),
                    ses         = ses,
                    seshelp     = seshelp,
                    summary     = seshelp.cart_summary_table(), # JJW 8/7/15 for consistency in new theme templates
                    grandtot    = grandtot,
                    totqty      = totqty,
                    tax         = tax,
                    shipping    = shipping,
                    gtts        = gtts,
                    order       = order,
                    payment     = payment
                ), context_instance=RequestContext(request))

    else:  # it's a GET, fill in the inital form
        #customer = user.customer_set.all() [:1] or []
        customer = Customer.objects.filter(user=user)

        if customer:
            address_obj = Address.objects.filter(customer=customer)
            user_form                = UserForm (instance=user)
            customer                 = customer [0]

            if trace: print 'CUSTOMER', customer.id, user.id, customer.user_id
            customer_form            = CustomerForm (instance=customer)
            ses ['customer']         = customer
            order_form               = OrderForm()
            if address_obj:
                shipping_address_form    = AddressForm (prefix='shipping', instance=customer.default_shipping())
            else:
                shipping_address_form    = AddressForm (prefix='shipping', instance=customer.default_shipping(),initial={'name': customer.user.first_name + ' ' + customer.user.last_name})
            #shipping_address_form    = AddressForm (prefix='shipping', instance=customer.default_shipping(),initial={'name': customer.user.first_name})
            billing_address_form     = BillingAddressForm (prefix='billing', instance=customer.default_billing())
            ses ['shipping_address'] = customer.default_shipping()
            ses ['billing_address']  = customer.default_billing()
            payment_form             = PaymentForm ()
        else:
            if trace: print 'USER', user, user.id
            user_form               = UserForm()
            customer_form           = CustomerForm (initial = dict (email=user.email))
            order_form              = OrderForm()
            shipping_address_form   = AddressForm (prefix='shipping')
            billing_address_form    = BillingAddressForm (prefix='billing')
            payment_form            = PaymentForm()

        user_form.header += ' (User: ' + user.username + ')'

    return render_to_response ('checkout.html', dict (
            breadcrumbs     = (Breadcrumb ('Checkout', 'Checkout', '/checkout/'),),
            formlist        = (user_form, customer_form, order_form, shipping_address_form, billing_address_form, payment_form),
            totqty          = totqty,
            grandtot        = grandtot,
            summary         = seshelp.cart_summary_table(), # JJW 8/7/15 for consistency in new theme templates
        ), context_instance=RequestContext(request))

from django.conf import settings # importing settings for emails -mani
@login_required
def order (request):
    ses = request.session

    seshelp = SessionHelper (ses)
    totqty, grandtot = seshelp.cart_totals() # TODO: convert these legacy references to use the dict retruned from cart_summary

    order           = ses ['order']
    payment         = ses ['payment']
    payment_data    = ses ['payment_data']
    customer        = ses ['customer']
    billing_address = ses ['billing_address']
    shipping_address = ses ['shipping_address']
    billing_name    = ses ['billing_name']
    gtts            = ses ['gtts']

    ctx = dict (
            email = customer.email,
            order   = order,
            name    =  shipping_address.name,#billing_name, # or customer.name(),
            payment = payment,
            form    = payment_data,
            addr    = "%s / %s  %s" % (billing_address, shipping_address,customer,),
            gtts    = gtts,
            ses         = ses,
            grandtot    = grandtot,
            totqty      = totqty,
            tax         = order.tax,
            shipping    = order.shipping,
        )

    if trace: print 'ORDER BEFORE:', order.id, customer.id, customer.user_id

    customer.save()
    shipping_address.save()

    order.ship_to_address = shipping_address
    if shipping_address.type != 'both':
        billing_address.save()
        order.bill_to_address = billing_address
    else:
        order.bill_to_address = shipping_address

    order.save()
    payment.order = order
    payment.save()

    # not sure why I need to to do this, COW semantics on save, maybe?
    ses ['order'] = order
    ses ['payment'] = payment


    # send secure order email to Joe

    if trace_order:
        print 'ORDER AFTER COMMIT:', order.id, customer.id, customer.user_id
        print 'Sending secure email w/order data'
        try:
            print order_email.render (Context (ctx))
        except Exception, e:
            print e
            print order_email
            print ctx
            raise e

    send_mail ("%s Secure order info #%s" % (settings.HNN[0],order.id),
        # 'order email.render: "%s" end order email!' % order_email.render (ctx),
        order_email.render (Context (ctx)),
        settings.ORDER_FROM_EMAIL,
        settings.SECURE_ORDER_EMAIL, # 'max@eracks.com'],
    )   #, fail_silently=False, attachments=None, context=None)
    # getting emails from settings -mani

    # send customer email too

    text = "Your email confirmation, as PDF and HTML attachments\n\n"
    #html = '<html><body>%s</body></html>' % render_to_string ('_final_cart.html', context_instance=ctx)
    html = render_to_string ('email_order.html', context_instance=Context (ctx))

    #topdf = StringIO()
    #pdf = generate_pdf('_final_cart.html').getvalue()  #, topdf)
    pdf = generate_pdf('email_order.html', context=ctx).getvalue()  #, topdf)
    #rslt = pisaDocument (html, topdf)  #, result)
    #if rslt.err:
    #    text += '\n\nPDF error: %s' % cgi.escape(html)
    #    pdf = text
    #else:
    #    pdf = topdf.getvalue()

    #return HttpResponse (topdf.getvalue(), mimetype='application/pdf')

    #creating a list to append the orders email list
    order_email_list = [customer.email or customer.user.email] + settings.ORDER_EMAIL
    msg = EmailMultiAlternatives ('Your %s eracks order #%s' % (settings.HNN[0],order.id),
        text,  # nope: '',  # let's try attaching the text,
        settings.ORDER_FROM_EMAIL,
        order_email_list
    )
    # getting emails from settings -mani

    msg.attach_alternative (html, "text/html")
    #msg.attach_alternative (text, "text/plain")
    msg.attach ('eRacks_Order_#%s.pdf' % order.id, pdf, "application/pdf")
    msg.send()


    # Redirect after POST

    return HttpResponseRedirect('/checkout/ordered/')


@login_required
def ordered (request):
    ses     = request.session
    seshelp = SessionHelper (ses)
    totqty, grandtot = seshelp.cart_totals() # TODO: convert these legacy references to use the dict retruned from cart_summary
    order   = ses.get ('order')
    payment = ses.get ('payment')
    gtts    = ses.get ('gtts')

    if not order:
        return HttpResponseRedirect ('/cart/')

    #ses ['cart'] = []
    ##del ses ['order']

    return render_to_response ('ordered.html', dict (
            breadcrumbs     = ( Breadcrumb ('Checkout', 'Checkout', '/checkout/'),
                                Breadcrumb ('Order', 'Order', '/checkout/order/'),
                              ),
            ses             = ses,
            totqty          = totqty,
            grandtot        = grandtot,
            tax             = order.tax,
            shipping        = order.shipping,
            gtts            = gtts,
            order           = order,
            payment         = payment,
        ), context_instance=RequestContext(request))
