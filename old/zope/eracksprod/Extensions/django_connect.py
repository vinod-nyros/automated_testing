import os, sys
import pprint

from updater import sesurl

os.environ ['DJANGO_SETTINGS_MODULE'] = 'django_eracks.settings'


def reload_django_modules():
    #zip through sys.modules and delete?  bu what about refcount? for now, let's just reload.

    # ok here goes:

    result = 'Deleting all modules that start with "django.":\n\n'
    for nam, mod in sys.modules.items():
        if nam.startswith ('django.') or nam.startswith ('test') or nam.startswith ('eracks9')or nam.startswith ('django_eracks') or nam =='django':
            result += 'deleting %s (%s)\n' % (nam, mod)
            del sys.modules [nam]

    return result

    result = 'Reloading all modules that start with django:\n\n'
    for nam, mod in reversed (sys.modules.items()):
    #for nam, mod in sys.modules.items():
        if nam.startswith ('django') and mod:
            result += 'reloading %s (%s)\n' % (nam, mod)
            try:
                reload (mod)
            except Exception, e:
                result += 'Exception: %s\n' % `e`

    return result


def show_modules():
    return pprint.pformat (sys.modules)


def reload_django_settings():
    import django_eracks
    import django_eracks.settings as settings
    reload (django_eracks)
    reload (django_eracks.apps)
    reload (django_eracks.apps.utils)
    reload (django_eracks.apps.utils.minitags2)
    reload (django_eracks.apps.legacy)
    reload (django_eracks.apps.legacy.models)
    reload (settings)

    from django.conf import settings
    settings._wrapped = None  # force a reload
    settings._setup()  # but do it manually anyway
    #return django_eracks.apps.utils.minitags2.FormattedTagStream
    return pprint.pformat (settings._wrapped.__dict__)


#### product as_content, called by config_django thru external method dev.config_product_page_from_django

def product_as_content (self):
    #from django_eracks.apps.legacy.models import Product
    #import django_eracks.apps.legacy.models 
    #reload (django_eracks.apps.legacy.models)
    ##import django_eracks.apps.legacy.models.Product #as Product

    #reload_django_modules()
    #reload_django_modules()

    #from django_eracks.apps.legacy.models import Product
    #import django_eracks.apps.legacy.models
    #reload (django_eracks.apps.legacy.models)
    import django.db
    from django_eracks.apps.legacy.models import Product

    req = self.REQUEST

    if hasattr (req, 'sku'):
        #sku = 'NAS16X-2'
        sku = req.sku

        #from django.db import connection, transaction
        #cursor = connection.cursor()

        #cursor.execute("SELECT * FROM products WHERE sku = %s", [sku])
        #row = cursor.fetchone()
        #return `row`

        #product = django_eracks.apps.legacy.models.Product.objects.filter (sku=sku)
        product = Product.objects.filter (sku=sku)
        if product:
            product = product [0]
            return product.as_content
        else:
            return "Product not found - 404"
    else:
        return "No Sku - 404"


#### cart_box, rendered by Django (with css, etc)

def getsession (self):
  return getattr (self, 'session', self.aq_parent.session)

def cartcontents (self):
  ses = getsession (self)

  grandtot = 0
  totqty = 0

  if ses.has_key ('cart'):
    cart = ses ['cart']

    for line in cart.values():
      qty = line ['qty']
      totqty = totqty + qty
      grandtot = grandtot + qty * line ['totprice']

  return (totqty, grandtot)


def django_cart_box (self):
    from django_eracks.apps.utils.minitags2 import TagStream

    carturl = sesurl (self.session, self.REQUEST, 'cart', 1)
    checkouturl = sesurl (self.session, self.REQUEST, 'cart', 2)

    (totqty, grandtot) = cartcontents (self)

    if not totqty: return ''

    return TagStream() \
            .div (cls="box xsmall center") \
            .div('Your eRacks cart', cls="boxtitle small") \
            .img (src='/images/cart', alt='Shopping Cart Image') \
            .a(' %i item%s $%8.2f total' % (totqty, 's'*int(totqty!=1), grandtot), href=carturl).br \
            .a ('View Cart', href=carturl) \
            .span (' &middot; ') \
            .a ('Checkout', href=checkouturl) \
            .render()

