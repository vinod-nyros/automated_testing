## Import_photos.py - imports photos by product dir into database, making a guess at include vs exclude

import sys, os
import argparse
from pprint import pprint
from myproject import settings

#from home.helpers import SessionHelper
#from orders.models import Order
from products.models import Product, Categories, CategoryImage, ProductImage

trace = 0

parser = argparse.ArgumentParser (description = 'Check, List, and update Product photos and their directories')

#print Order.objects.count()
print 'Total products:', Product.objects.count()
print 'Published products:', Product.objects.filter(published=True).count()
print


## Move to utils.photos.py

def fsize (fname):
    if os.path.isfile (fname):
        return os.stat (fname).st_size

def is_autocreated (fname, flist):
  '''
    Filter out dup filenames that end in:
      _admin_thumbnail
      _big
      _large
      _medium
      _small
      _thumbnail
      .[png,jpeg,jpg]
  '''
  f, ext = fname.rsplit ('.', 1)
  toks = f.split ('_')

  if len (toks) < 2:
    if trace: print 'toks:', toks
    #return toks [0] + '.' + ext
    return False

  # don't really need this, already checking for _thumbnail
  #if toks [-2] == 'admin' and toks [-1] == 'thumbnail':
  #  if trace: print '_'.join (toks [:-2]) + '.' + ext
  #  return ('_'.join (toks [:-2]) + '.' + ext) in flist

  if toks [-1] in ('big', 'large', 'medium', 'small', 'thumbnail'):  # and toks 0..-3 match...
    if trace: print '_'.join (toks [:-1]) + '.' + ext
    # this was orignally to make sure that there wasnt' a real, non-autocreated photo ending in these - bucket :)
    #return ('_'.join (toks [:-1]) + '.' + ext) in flist
    return True

  return False


## classes

class ProdPhotos:
  no_dir_count = 0
  unpub_count = 0

  def product_photos (self, product):
    folder = os.path.join (settings.STATIC_ROOT, 'images','products', product.slug)

    try:
        flist = [(f, fsize (os.path.join (folder, f))) for f in os.listdir (folder)]
        return [(os.path.join ('images','products', product.slug, f), fsiz) for f,fsiz in flist if fsiz]
    except Exception, e:
        self.no_dir_count += 1
        print e
        #assert product.published is False
        return []

  def product_loop (self):
    "Generator, loops on product and returns lists of files in static prod photo dir"

    for p in Product.objects.published():  # all():
      r = self.product_photos (p)
      if r:
        if trace: print r
        yield p, r
      else:
        if p.published:
          print 'No dir for published prod:', p



## Main

pp = ProdPhotos()
#pp.product_loop()
#print 'Published prods with no dir:', pp.no_dir_count
#print '\n\n\nNow using generator:'

for prod, photos in pp.product_loop():
  #if prod.sku == 'TWINGUARD.ENT':
  if prod.sku == 'ZENBOOK':
    #photo_list = [f for f,s in photos]
    #if trace: pprint (photo_list)

    for photo, siz in photos:
      if trace: print photo, is_autocreated (photo, []) # photo_list)

      if not is_autocreated (photo, []):  # photo_list):
        if prod.images.filter (image__iexact=photo):
          print photo, 'DUP'
        else:
          print 'Creating:', photo, siz
          i = ProductImage (image=photo, product=prod, published = (siz > 5000))
          i.save()
          #prod.images.add (i)
          #prod.save()

print
print 'Published prods with no dir:', pp.no_dir_count




# TODO: Count the dirs with/without a prod, and prods with/without a dir, and which ones are published...

# then upd db tables with the actual imges
# and add exclude field
# and pre-populate exclude with under 22K (Or whatever it was)

