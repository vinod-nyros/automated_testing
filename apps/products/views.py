# -*- coding: utf-8 -*-

import os

try:
    import json
except ImportError:
    import simplejson as json

from django import forms
#from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext  # Template, Context,
from django.utils.safestring import mark_safe
from django.template.defaultfilters import slugify
from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User

from utils import minitags as tags
from utils import Breadcrumb
from home.helpers import SessionHelper, Prod
from home.views import create_new_user
from orders.views import add_to_cart
from products.models import Product, Categories


class ProductSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Product.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.updated


#### Globals and utility functions

product_breadcrumb = Breadcrumb ('Products', 'eRacks Products', '/products/')

#@cache_function
def product_photos (product):
    return product.images.published()  #### HERE - either return just the fname tail, or change the template!

    # see also scripts/photos/import_photos for a smarter algorithm, and brahms too :)
    # but now, we just use the DB

    folder = os.path.join (settings.STATIC_ROOT, 'images','products', product.slug)
    try:
        #return os.listdir (folder)
        return  [f for f in os.listdir (folder)
                  if os.path.isfile (os.path.join (folder, f))
                  and os.stat (os.path.join (folder, f)).st_size > 22000  # TODO: check here for in images and unpublished
                ]
    except Exception, e:
        print e
        return []


#### Quote email template

quote_cart_request_email_template = '''
{s.HOST_NAME} Quote Request:

Dear {u} (eMail: {u.email}),

You have requested a quote - a summary of your quote request is attached.

An eRacks representative will get back to you shortly with your private online quote.

Best regards,
eRacks Systems

'''

quote_product_request_email_template = '''
{s.HOST_NAME} Quote Request:

Dear {u} (eMail: {u.email}),

You have requested a product quote for: {p.name}

Options and Choices:

{p.options_choices_as_txt}

Notes: {p.notes}

Base price: ${p.baseprice:.2f}
Price with requested configuration: ${p.totprice:.2f}
Shipping Weight: {p.weight} lbs

An eRacks representative will get back to you shortly with your private online quote.

Best Regards,
eRacks Systems

'''



#### Get-a-Quote related

def send_quote_email(req, user):
  print 'send_quote_email'
  ses = req.session
  seshelp = SessionHelper (ses)
  seshelp.update (req, called_from_cart=True)
  prod = ses.get ('prod', None)

  text = quote_product_request_email_template.format (u=user, s=settings, p=Prod(prod))

  # these lines add to cart before sending it - use with other template above, call from cart page:
  #html = '<html><body>%s</body></html>' % render_to_string ('_final_cart.html', context_instance=ctx)
  #ses ['cart'] = ses.get ('cart', []) + [prod]
  #ses ['prod'] = {}
  #html = seshelp.cart_details()
  #print 'SESHELP', seshelp.cart_summary(), seshelp.cart_details()

  quote_email_list = [user.email] + settings.ORDER_EMAIL
  msg = EmailMultiAlternatives ('Your %s eracks quote request' % settings.HNN[0],
      text,  # nope: '',  # let's try attaching the text,
      settings.ORDER_FROM_EMAIL,
      quote_email_list
  )

  #msg.attach_alternative (html, "text/html")
  print 'send_quote_email'
  print 'haijaisjaisjak'
  print '****************settings.ORDER_FROM_EMAIL,'
  print user.email
  msg.send()


def emailForm (req):  # inner form to access request
  class EmailForm(forms.Form):
    email = forms.EmailField(max_length=128, required=False)
    print '****************test_1'
    def clean(self):
      cleaned_data = super(EmailForm, self).clean()
      email = cleaned_data.get("email")
      print 'emailentered'
      print '************'
      print email
      if email:
        users = User.objects.filter (email__iexact=email)
        print 'users********************'
        print users
        if users:
          user=users [0]
        else:
          user, pw = create_new_user (self, req)
      else:
        user = req.user

        if not user.is_authenticated():
          #self.add_error ('email',
          raise forms.ValidationError ("You must either be logged in, or enter an email address to receive your quote")

      print 'USER', user, user.is_authenticated()
      send_quote_email (req, user)

  return EmailForm


#### View functions

def config (request, legacy_category=None):  # redirect legacy Zope URLs to new product page
    sku = request.GET.get ('sku')

    if legacy_category:
        category = slugify (legacy_category)
    else:
        product = Product.objects.filter (sku=sku)
        if product:
            category = product [0].category.slug
        else:
            raise Http404

    return HttpResponseRedirect ('/products/%s/%s' % (category, sku))


#def products (request):  # really categories
#    categories = Categories.objects.published()
#
#    return render_to_response('products.html', dict (
#            title="eRacks Product Categories",
#            categories=categories,
#            breadcrumbs=(product_breadcrumb,),
#        ), context_instance=RequestContext(request))


def categories (request):
    categories = Categories.objects.published()

    return render_to_response('categories.html', dict (
            title="eRacks Product Categories",
            categories=categories,
            breadcrumbs=(product_breadcrumb,),
        ), context_instance=RequestContext(request))


def category (request, category):
    categories = Categories.objects.published().filter (slug=category)

    if not categories:
        categories = Categories.objects.published().filter (name__iexact=category)
        if categories:
            return HttpResponseRedirect ('/products/%s/' % categories [0].slug)

    if not categories:
        raise Http404, "Unknown Category"  # allows for redirect lookup too

    category = categories [0]

    breadcrumbs = (
        product_breadcrumb,
        category
    )

    return render_to_response('category.html', dict (
            title=category.title or category.name,
            category=category,
            breadcrumbs=breadcrumbs,
            meta_title=category.meta_title,
            meta_keywords=category.meta_keywords,
            meta_description=category.meta_description,
        ), context_instance=RequestContext(request))


def product (request, category, sku):
    products = Product.objects.filter (sku__iexact=sku)

    if products:
        product = products [0]
        if product.sku != sku:
            return HttpResponseRedirect (product.url)
        if product.category.slug != category:
            return HttpResponseRedirect (product.url)
    else:
        raise Http404, "Unknown Product"

    edit = request.GET.get ('edit', None)

    ses_helper = SessionHelper (request.session)

    if not edit:
        ses_helper.fill (product)
    else:
        assert request.session.get ('prod', None)

    post = request.POST #.copy()  # make it mutable to add sku

    if post:  # only for small subform(s) like email quote and future wishlist
        if post.get ('quote', None):     # send quote request to admin & user both, save in quotes
          print 'POST', post
          emailform=emailForm(request)(post)
          if emailform.is_valid():
            messages.success (request, 'Your quote request has been sent')

        elif post.get ('wishlist', None):     # Add reference to this product in user's wishlist
            raise Exception ('Implement Wishlist!')
        else:
          add_to_cart (request)
          return HttpResponseRedirect('/cart/')

    else:
      emailform = emailForm(request)()

    breadcrumbs = (
        product_breadcrumb,
        product.category,
        product,
    )

    photos_list = [str(t) for t in product_photos (product)]
    photos = mark_safe ('\n'.join (photos_list))

    return render_to_response ('product.html', dict (
            title=product.title or product.name,
            product=product,
            breadcrumbs=breadcrumbs,
            meta_title=product.meta_title,
            meta_keywords=product.meta_keywords,
            meta_description=product.meta_description,
            photos=photos,
            photos_list=photos_list,
            emailform=emailform,
            js_bottom=mark_safe (tags.script (config_grid_js, type='text/javascript')),
        ), context_instance=RequestContext(request))



#### Ajax views and supporting

#@is_ajax or ajax_required...
def update_grid (request):
    ses_helper = SessionHelper (request.session)
    results = ses_helper.update (request)
    return HttpResponse (json.dumps (results), content_type='application/json')


#### configgrid view with js

config_grid_js='''
function update_config (e) {
    console.log ($('.configform').serialize());
    if (e) {
        console.log ('ITEM CHANGED:');
        console.log (e.currentTarget);
        console.log ($(e.target).find ('option:selected'));
    }

    $.post ("/products/update_grid/", $('.configform').serialize(), function(json) {
        console.log (json);
        $('#config_summary .price b').html ('$' + json.price);
        $('#config_summary .summary').html ('<b>Configuration Summary:</b><br>' + json.summary);

        $.each(json.optchoices, function(key, val) {  // it's an array, so keys are 0
            console.log (key, val);
            console.log ('#' + val.optid + ' .info');
            if (val.choicename)
                $('#' + val.optid + ' .info').html (val.choicename);
            if (val.choiceblurb)
                $('#' + val.optid + ' .info').attr ('title', val.choiceblurb);
            //if (val.optprice)
            $('#' + val.optid + ' .optprice').html ('$' + val.optprice);
        });
    }).error (function(err) {
        console.log ('post error:' + err);
        window.location.reload();   // likely the back button, prod is no longer there, so reload
    });
}

$(document).ready(function() { // JJW changed this to load 1/10/13, was firing before GET completed, causing inv inx
//$(document).load(function() {  // nope, doesn't fire at all now :(
    //update_config();

    $('.configgrid select[name="choiceid"]').change (update_config);
    $('.configgrid select[name="choiceqty"]').change (update_config);
});
'''

