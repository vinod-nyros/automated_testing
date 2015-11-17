#!/usr/bin/env python
# coding: utf-8

import sys

comment_template='''\
Scraped from Passmark: {url}
Name: {name}
Rank: {rank}
G3DMark: {mark}
G2DMark: {g2d}
Num Samples: {samples}
Price: {price}
'''

blurb_template='''\
{name}:
G3D Mark score: {mark}
G2D Mark scrore: {g2d}
'''

choicecategory = sys.argv [1]
url = sys.argv [2]

print "name,comment,cost,choicecategory,blurb,supplier,price,multiplier,published,sortorder"

for line in [l for l in sys.stdin] [1:]:
    #print ','.join ('"%s"' % t.strip() for t in line.split ('|') if t.strip())
    toks = [t.strip() for t in line.split ('|') if t.strip()]

    #print toks
    #name = toks [1].replace ('Intel® Xeon® Processor','Intel Xeon').replace ('®','')

    name, mark, price, rank, g2d, samples = toks
    row = dict(name=name, mark=mark, price=price, rank=rank, g2d=g2d, samples=samples, url=url)

    sortorder = int (rank)
    comment =  comment_template.format (**row)
    blurb = blurb_template.format (**row)
    cost = price.strip('$* ').replace (',','')

    if price.endswith ('*'):
      comment += 'Price is last known price'


    print ','.join ('"%s"' % t for t in (name, comment, cost, choicecategory, blurb, '', '', '', True, sortorder))

sys.exit(0)
