# order-cart.py, reads order table

import datetime
import sys, os

from pprint import pprint
from collections import OrderedDict

#sys.path.insert ('/home/joe/eracks10/apps')
os.environ ['DJANGO_SETTINGS'] = '/home/joe/eracks10/settings.py'

#from home.helpers import SessionHelper
from orders.models import Order

#o = Order.objects.get (pk=55397)
o = Order.objects.order_by ('-created') [0]

cart = o.cart.replace ("': <", "': '<").replace ('\\n','').replace ('\\r','').replace (">,", ">',").replace (">}",">'}")
cart = eval (cart)

prod = cart [0]
#print prod ['sku'], prod.keys()

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

p = Prod (prod)

#print p.__dict__.keys()
#print p.options()
#pprint (p.opts)

print
print 'Order #', o.id

a = o.ship_to_address

print
print 'Ship to:'
print a.name
print a.address1
if a.address2: print a.address2
print a.city, a.state
print a.zip, a.country
print
print 'eRacks/%s' % p.name
print
print p.all_choices()
print
print 'Order Notes:', p.notes
print
print "Weight:", p.weight, 'lbs'
print 'Requested shipping:', o.shipping_method
print 'Preferred shipper:', o.preferred_shipper
print
print "Base Price: $%0.2F" % float(p.baseprice)
print "Price as configured: $%0.2F" % float(p.totprice)
print "Our estimated base cost: $%0.2F" % float(p.cost)


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

