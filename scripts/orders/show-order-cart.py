# show-order-cart.py, reads order table - originally from tests/test-order-cart.py 5/24/14 JJW

import datetime
import sys, os

from pprint import pprint
from collections import OrderedDict

#sys.path.insert ('/home/joe/eracks11/apps')
os.environ ['DJANGO_SETTINGS'] = '/home/joe/eracks11/settings.py'

# for 1.7: http://stackoverflow.com/questions/25537905/django-1-7-throws-django-core-exceptions-appregistrynotready-models-arent-load
import django
django.setup()

#from home.helpers import SessionHelper
from orders.models import Order



class Prod (): # dict):
    def __init__ (self, prod):
        self.__dict__.update (prod)
        self.option_list = [Opt (k,v) for k,v in self.opts.items()]
        self.options_by_id = dict ([(o.id, o) for o in self.option_list])

    def options (self):
        for k,v in self.opts.items():
            selectedchoiceid = v ['selectedchoiceid']
            print '%s: %s' % (v ['name'], v ['choices'] [selectedchoiceid])

    def all_choices (self):
        for o in self.option_list:
            selectedchoice = o.choices_by_id [o.selectedchoiceid]
            if o.choiceqty > 1:
                print '%s: %sx %s' % (o.name, o.choiceqty, selectedchoice.name), ("add $%0.2F" % o.price if o.price else '')
            else:
                print '%s: %s' % (o.name, selectedchoice.name), ("add $%0.2F" % o.price if o.price else '')


class Id_dict():
    def __init__ (self, id, dct):
        self.__dict__.update (dct)
        assert self.id == int(id), (self.id, id)

class Opt (Id_dict):
    def __init__ (self, theid, dct):
        theid = theid.split ('_') [0]
        #super(Opt, self).__init__ (theid, dct)
        Id_dict.__init__ (self, theid, dct)
        self.choiceqty = dct.get ('choiceqty', 1)

        self.choice_list = [Choice (k,v) for k,v in self.choices.items()]
        self.choices_by_id = dict ([(c.id, c) for c in self.choice_list])

class Choice (Id_dict):
    pass


def print_order (o):
  print
  print 'Order #', o.id
  print 'eMail', o.customer.email
  print 'eMail2', o.customer.email2
  print 'User eMail', o.customer.user.email

  a = o.ship_to_address
  b = o.bill_to_address

  print
  print 'Ship to:'
  print a.name
  print a.address1
  if a.address2: print a.address2
  print a.city, a.state
  print a.zip, a.country
  print
  print 'Bill to:'
  print b.name
  print b.address1
  if b.address2: print b.address2
  print b.city, b.state
  print b.zip, b.country
  print
  print 'Requested shipping:', o.shipping_method
  print 'Preferred shipper:', o.preferred_shipper


def print_lines (line, prod):
  p = Prod (prod)

  #print p.__dict__.keys()
  #print p.options()
  #pprint (p.opts)

  print
  #print 'eRacks/%s' % p.name
  print 'Line:', line, 'Sku:', p.sku
  print
  print 'choices:', p.all_choices()
  print
  print 'Order line Notes:', p.notes
  print
  print "Weight:", p.weight, 'lbs'
  print
  print "Base Price: $%0.2F" % float(p.baseprice)
  print "Price as configured: $%0.2F" % float(p.totprice)
  #if 'cost' in p:
  if hasattr (p, 'cost'):
    print "Our estimated base cost: $%0.2F" % float(p.cost)


### Main


## Get order number

if len (sys.argv) > 1:
  #print sys.argv [0], len (sys.argv)
  o = Order.objects.get (pk=sys.argv[1])   # 55397)
else:
  orders = Order.objects.order_by ('-created')
  print 'Last 5 orders (in reverse order), using last one:', '\n'.join ([''] + [str(o) for o in orders [:5]])
  #print 'Last 5 orders (in reverse order), using last one:', '\n'.join (orders [:5])
  o = orders [0]


# sometimes need to tweak this line on a per-order basis - should delete or requote / strip prod.desc BEFORE storing in cart :)
#cart = o.cart.replace ("': <", "': '<").replace ('\\n','').replace ('\\r','').replace (">,", ">',").replace (">}",">'}")
cart = o.cart.replace ("': <", "': '<").replace ('\\n','').replace ('\\r','').replace ('>, o', '> o').replace('</a>,','</a>').replace (">,", ">',").replace (">}",">'}")
cart = eval (cart)

print_order (o)

for inx, prod in enumerate (cart):  #  [0]
  print_lines (inx+1, prod)  # ['sku'], prod.keys()




'''
OO breakdown:

- cart
- order
  - shipping
  - line items
    - prod
      - options
        - default vs chosen
    - qty
    - num
    - sumry / desc
    - notes

methods:
to_db
from_db

work_order - - full manifest
invoice
packing list
receipt


'''

