#!/usr/bin/env python
# coding: utf-8

import sys

vid_comment_template='''\
Scraped from Passmark: {url}
Name: {name}
Rank: {rank}
G3DMark: {mark}
G2DMark: {g2d}
Num Samples: {samples}
Price: {price}
'''

vid_blurb_template='''\
{name}:
G3D Mark score: {mark}
G2D Mark scrore: {g2d}
'''


HERE - WIP, need to refactor into class - 10/23/15 JJW


#### Modulification 10/19/15 JJW

def format_and_list_choice_dicts (fname, choicecategory, url, comment_template, blurb_template, n=0):  # returns list of up to n (key, fields-dict) tuples
  f = open (fname)
  rslt = []

  for line in [l for l in f] [1:]:
      toks = [t.strip() for t in line.split ('|') if t.strip()]

      name, mark, price, rank, g2d, samples = toks
      row = dict(name=name, mark=mark, price=price, rank=rank, g2d=g2d, samples=samples, url=url)

      sortorder = int (rank)
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

      name, mark, price, rank, g2d, samples = toks
      row = dict(name=name, mark=mark, price=price, rank=rank, g2d=g2d, samples=samples, url=url)

      sortorder = int (rank)
      comment =  comment_template.format (**row)
      blurb = blurb_template.format (**row)
      cost = price.strip('$* ').replace (',','')

      if price.endswith ('*'):
        comment += 'Price is last known price'


      print ','.join ('"%s"' % t for t in (name, comment, cost, choicecategory, blurb, '', '', '', True, sortorder))

