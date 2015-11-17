#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding: utf-8

#nope, with or without the $0, just hangs :
#!/usr/bin/env DJANGO_SETTINGS_MODULE=wtp.settings PYTHONPATH=/home/joe/Clients/WTP/wtp:/home/joe/Clients/WTP python $0


##### set up django environment

import sys, os
# nope: have to modify sys.path directy, since this only works b4 startup:
#os.environ ['PYTHONPATH'] = "/home/joe/Clients/WTP/wtp:/home/joe/Clients/WTP"
os.environ ['DJANGO_SETTINGS_MODULE'] = "eracks9.settings"
nodes = os.path.dirname (os.path.abspath (sys.argv [0])).split ('/')
print os.path.dirname (os.path.abspath (__file__))
#print nodes # , '/'.join (nodes [:-2]), '/'.join (nodes [:-3])
#sys.path.insert (0, '/'.join (nodes [:-3]))
sys.path.insert (0, '/'.join (nodes [:-2]))  # assumes this file is in <proj>/scripts
#print sys.path


##### main

from django.db import connection, transaction, IntegrityError
from django.utils.encoding import smart_str, smart_unicode

from eracks9.apps.legacy.models import Product, Option, Choice, Prodopt, Prodoptchoice


#### fix the utf8 choices problem

#cursor = connection.cursor()
#cursor.execute("SELECT name from choices where name ilike '%%red hat%%';")
#cursor.execute("SELECT name from choices limit 2;")
#print dir(cursor)
#print cursor.__dict__
#print dir(cursor.__dict__['cursor'])
#rows = cursor.fetchall()
#print len (rows)

#for r in rows:
#  print r


#### loop thru opts, build list of unique sets of choices by product:

prods = {}
opts = []

for o in Option.objects.all():
  for po in Prodopt.objects.filter(option=o):
    choices = tuple(sorted(po.choices.values_list('id',flat=True)))
    prod = po.product.sku
    opts += [(choices, '%s:%s'%(o.name,prod))]

for line in sorted(opts):
  print line


#for p in Product.objects.all():
#  prods [p.sku] = {} 
#  for po in Prodopt.objects.filter (product=p):
#    prods[p.sku] [str(po)] = 1

#import pprint
#pprint.pprint (sorted(opts))
