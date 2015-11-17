#!/usr/bin/env python
# coding: utf-8

import sys

print "name,comment,cost,choicecategory,blurb,supplier,price,multiplier,published,sortorder"

for line in [l for l in sys.stdin] [1:]:
    #print ','.join ('"%s"' % t.strip() for t in line.split ('|') if t.strip())
    toks = [t.strip() for t in line.split ('|') if t.strip()]

    #print toks

    name = toks [1].replace ('Intel® Xeon® Processor','Intel Xeon').replace ('®','')

    comment = "Scraped from ark, %s: %s" % (toks [2], toks [3])

    blurb = "%s cores, %s" % (toks [4], toks [5])

    cost = toks [6].split (':') [-1].strip('$ ')

    choicecategory = sys.argv [1]

    print ','.join ('"%s"' % t for t in (name, comment, cost, choicecategory, blurb, '', '', '', True, 1300))

sys.exit(0)
