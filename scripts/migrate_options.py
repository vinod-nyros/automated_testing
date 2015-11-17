#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__='''

Restate / Migrate Options - 

OK - The goal:
- a few sets of options for common scenarios / models
- no more POCs
- clean up legacy choices (Fedora 7?!)
- arch linux
- 2x ubustudio for desktops [Z]
- "Other (please enter in 'Notes' field)" [Z]

Different OS needs:
- NAS - includes FreeNAS, eg
- Desktop (Can still include server offerings? n - notes field)
  - Zenbook - reduced compatibilty?  Can't just use Desktop? Y
- Server (Can still include desktop offerings)

- Studio OSes? added to Desktop - separate option?
- Firewall OS option?
So can we combine them?

On PO: 
- single should be checked, but
- should include "None - treated w/ubuntu"

Perhaps we should have a specifiable 'none' choice?

Should the sub-decription-less OS option have everything?  Or be one of the subcats?
'''

import os, sys

# env PYTHONPATH=$DIR/apps/:$DIR/../:$DIR DJANGO_SETTINGS_MODULE=eracks.settings python "$@"

def ensure_path (s):
    if not s in sys.path: sys.path.append (s)

parent  = os.path.abspath(os.path.dirname (__file__))
project = os.path.abspath(os.path.dirname (parent))
ensure_path (project)
ensure_path (os.path.join (project, 'apps'))

#if __name__ == "__main__":

os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "eracks.settings")

import django

#from django.db import connection, transaction, IntegrityError
#from django.utils.encoding import smart_str, smart_unicode

from products.models import Product, Option, Choice, Prodopt, Prodoptchoice

desktops = 'AMDESK ASERIES BOOQ DESQ iDESQ3 iDESQ5 iDESQ7 LEAF QFX QUBE SILENCE ARESPRO ARESPRO12 ARESPRO16 KING HUMBOLDT ADELIE ZENBOOK13 ZENBOOK ZENBOOK15'.split()

teeth = 1

django.setup()
OSes = Prodopt.objects.filter (product__published=True, option__name='Operating System')

#print Product.objects.published().count()
print OSes.count(), 'Victory, for now!'

nas_os_option=Option.objects.get (name="Operating System", usage_notes="NAS")
desktop_os_option=Option.objects.get (name="Operating System", usage_notes="Desktop/Notebook")
server_os_option=Option.objects.get (name="Operating System", usage_notes="Server")

print nas_os_option
print desktop_os_option
print server_os_option

for po in OSes:
  print 'Processing', po.product.sku

  #print po.choices.all()
  print po.choices.count()
  if teeth:
    print po.choices.clear()
    #print po.choices.all()
    print po.choices.count()

  if po.product.sku.startswith ('NAS'):
    print 'Setting NAS OS'
    po.option = nas_os_option
  elif po.product.sku in desktops:
    print 'Setting Desktop OS'
    po.option = desktop_os_option
  else: 
    print 'Setting Server OS'
    po.option = server_os_option

  if teeth:
    po.required = True
    po.save()

  print po, 'Complete'



print '\nGtr 0\n'

for os in OSes:
  if os.choices.count():
    print os.product, os.option.pk, os.choices.count()

print OSes.filter (choices__gt=0).count()  # nope, 1492 - counts the total of all the POCs
print OSes.filter (choices__isnull=False).count()  # nope, still 1492
print OSes.exclude (choices__isnull=True).count()  # 70 - off by 1, really 71 printed - QFX

print '\nEql 0\n'

for os in OSes:
  if os.choices.count() == 0:
    print os.product, os.option.pk, os.choices.count()

#print OSes.filter (choices=0).count()  # nope, 0
#print OSes.filter (choices=[]).count()  # nope, has to be int
print OSes.filter (choices__isnull=True).count()

print OSes.filter (choices__isnull=True)

print '\nDone'


sys.exit()

# OK test:

aseries = OSes.filter (product__sku='ASERIES')[0]
print aseries
print aseries.choices.all()
print aseries.choices.count()
print aseries.choices.clear()
print aseries.choices.all()
print aseries.choices.count()

#print aseries.remove (server_os_option)
#print aseries.add (desktop_os_option)
aseries.option = desktop_os_option
aseries.required = True
aseries.save()
print aseries

#print project
#print sys.path
sys.exit()



#### loop thru opts, build list of unique sets of choices by product:

def first_cut():
    prods = {}
    opts = []

    for o in Option.objects.all():
        for po in Prodopt.objects.filter(option=o):
            choices = tuple(sorted(po.choices.values_list('id',flat=True)))
            prod = po.product.sku
            opts += [(choices, '%s:%s'%(o.name,prod))]

    for line in sorted(opts):
        print line

    #import pprint
    #pprint.pprint (sorted(opts))


#for p in Product.objects.all():
#  prods [p.sku] = {} 
#  for po in Prodopt.objects.filter (product=p):
#    prods[p.sku] [str(po)] = 1



##### main

if __name__ == '__main__':
    # 280 tot
    #>>> uppers = [p for p in Product.objects.all() if p.sku.isupper()]
    #>>> lowers = [p for p in Product.objects.all() if p.sku.islower()]
    #>>> for p in [p for p in Product.objects.all() if not p.current in ['t','T']]:
    #190:
    #>>> nonactive = [p for p in Product.objects.all() if not p.current in ['t','T']]
    #90:>>> Product.objects.filter (current__in=['T','t']).count()
    pass



from pprint import pprint, pformat

for o in Option.objects.all():
    choicedict = {}
    for po in Prodopt.objects.filter(option=o):
        choices = list(sorted([c.name for c in po.choices.all()]))
        if po.product.current in ['t','T']:
            choicedict [`choices`] = (choicedict [`choices`] + [po.product.sku]) if `choices` in choicedict.keys() else [po.product.sku]
    #optdict += [(choices, '%s:%s'%(o.name,p.sku))]
    print 'OPTION:', o.name, ':'
    for k,v in choicedict.items():
        print '  CHOICES:', pformat (eval(k), indent=4)
        print '  PRODUCTS:', pformat (v, indent=4)



import sys
sys.exit()


for p in Product.objects.filter (current__in=['T','t']):
    for o in p.options.all():
        choicedict = {}
        for po in Prodopt.objects.filter(option=o, product=p):
            choices = list(sorted([c.name for c in po.choices.all()]))
            choicedict [`choices`] = (choicedict [`choices`] + [p.sku]) if `choices` in choicedict.keys() else [p.sku]
        #optdict += [(choices, '%s:%s'%(o.name,p.sku))]
        print 'OPTION:', o.name, ':'
        for k,v in choicedict.items():
            print '  CHOICES:'
            pprint (eval(k), indent=4)
            print '  PRODUCTS:'
            pprint (v)
            



opts=[]
opsdict = {}

for p in Product.objects.filter (current__in=['T','t']):
    for o in p.options.all():
        for po in Prodopt.objects.filter(option=o, product=p):
            choices = list(sorted([c.name for c in po.choices.all()]))
            opts += [(choices, '%s:%s'%(o.name,p.sku))]

for choices, optprod in opts:
    if `choices` in opsdict:
        opsdict [`choices`] += [optprod]
    else:
        opsdict [`choices`] = [optprod]

for k in opsdict.keys():
    print 'CHOICES LIST:', pprint  (eval(k), indent=4), ':'
    print 'OPTION:PRODUCT:', pprint (opsdict [k], indent=4)


no='''
opts=[]
for p in Product.objects.filter (current__in=['T','t']):
    for o in p.options.all():
        for po in Prodopt.objects.filter(option=o, product=p):
            choices = tuple(sorted(po.choices.values_list('id',flat=True)))
            opts += [(choices, '%s:%s'%(o.name,p.sku))]
opsdict=dict(opts)


opts = []
for o in Option.objects.all():
    for po in Prodopt.objects.filter(option=o):
        choices = tuple(sorted(po.choices.values_list('id',flat=True)))
        if p.current in ['t','T']:
        opts += [(choices, '%s:%s'%(o.name,p.sku))]

'''
