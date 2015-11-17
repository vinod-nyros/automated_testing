#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.db import connection, transaction, IntegrityError
from django.utils.encoding import smart_str, smart_unicode

from eracks9.apps.legacy.models import Product, Option, Choice, Prodopt, Prodoptchoice


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