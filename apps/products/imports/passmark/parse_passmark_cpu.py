#!/usr/bin/env python
# coding: utf-8

import sys

comment_template='''\
Scraped from Passmark: {url}
Name: {name}
Cores: {cores}
Rank: {rank}
PassMark: {mark}
Num Samples: {samples}
Price: {price}
'''

blurb_template='''\
{name}:
Cores: {cores}
PassMark score: {mark}
Rank: {rank}
Samples: {samples}
'''

#### Modulification 10/19/15 JJW

def format_and_list_choice_dicts (fname, choicecategory, url, n=0):  # returns list of up to n (key, fields-dict) tuples
  f = open (fname)
  rslt = []

  for line in [l for l in f] [1:]:
      toks = [t.strip() for t in line.split ('|') if t.strip()]

      name, mark, price, rank, samples, cores, logicalcores = toks
      row = dict(name=name, mark=mark, price=price, rank=rank, samples=samples, cores=cores, url=url)

      #sortorder = int (rank)
      sortorder = int (mark.replace(',',''))
      comment =  comment_template.format (**row)
      blurb = blurb_template.format (**row)
      cost = price.strip('$* ').replace (',','')

      try:
        cost=float(cost)
        published = True
      except:
        cost=0
        published = False

      if price.endswith ('*'):
        comment += 'Price is last known price'

      rslt += [(name, dict(comment=comment, cost=cost, choicecategory=choicecategory, blurb=blurb, published=published, sortorder=sortorder))]

      if n and len (rslt) >= n:
        return rslt

  return rslt


def print_csv (fname, choicecategory, url):
  f = open (fname)

  print "name,comment,cost,choicecategory,blurb,supplier,price,multiplier,published,sortorder"

  for line in [l for l in f] [1:]:
      toks = [t.strip() for t in line.split ('|') if t.strip()]

      #print toks
      #name = toks [1].replace ('Intel® Xeon® Processor','Intel Xeon').replace ('®','')

      name, mark, price, rank, samples, cores, logicalcores = toks
      row = dict(name=name, mark=mark, price=price, rank=rank, samples=samples, cores=cores, url=url)

      #sortorder = int (rank)
      sortorder = int (mark.replace(',',''))
      comment =  comment_template.format (**row)
      blurb = blurb_template.format (**row)
      cost = price.strip('$* ').replace (',','')

      if price.endswith ('*'):
        comment += 'Price is last known price'


      print ','.join ('"%s"' % t for t in (name, comment, cost, choicecategory, blurb, '', '', '', True, sortorder))

