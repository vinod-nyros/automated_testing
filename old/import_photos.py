## Import_photos.py - imports photos by product dir into database, making a guess at include vs exclude

import sys, os
import argparse
from pprint import pprint
from myproject import settings

from products.models import Product, Categories, CategoryImage, ProductImage

trace = 0


## Utils - Move to utils.photos.py

def fsize (fname):
    if os.path.isfile (fname):
        return os.stat (fname).st_size

def is_autocreated (fname):  # , flist):
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


## Classes

class ModelPhotos:  # model assumptions:  slug, images w/images_dir
  model = 'Define me in descendant class, along w/Create'
  no_dir_count = 0
  unpub_count = 0

  def __init__ (self):
    #self.model = model
    print 'Total %s:' % self.model.__class__.__name__, self.model.objects.count()
    print 'Published objects:', self.model.objects.filter(published=True).count()
    print

  def model_photos (self, obj):
    "Return contents of object's model's images_dir folder"

    images_dir = str (self.model.images.related.model.images_dir)

    folder = os.path.join (settings.STATIC_ROOT, images_dir, obj.slug)

    try:
      flist = [(f, fsize (os.path.join (folder, f))) for f in os.listdir (folder)]
      return [(os.path.join (images_dir, obj.slug, f), fsiz) for f,fsiz in flist if fsiz]
    except Exception, e:
      self.no_dir_count += 1
      print e
      #assert model.published is False
      return []

  def model_loop (self):
    "Generator, loops on model's published objects and yields / returns lists of files in static images_dir"

    for o in self.model.objects.published():  # all():
      r = self.model_photos (o)  # returns list of (f, siz) tuples
      if r:
        if trace: print r
        yield o, r
      else:
        if o.published:
          print 'No dir for published object:', o

  def photo_loop (self):
    for o, photos in self.model_loop():
        #if o.sku == 'ZENBOOK':
        for f, siz in photos:
          if trace: print f, is_autocreated (f)

          if not is_autocreated (f):
            if o.images.filter (image__iexact=f):
              print f, 'DUP'
            else:
              self.create (o, f, siz)


class ProdPhotos (ModelPhotos):
  model = Product

  def create (self, o, f, siz):
    print 'Creating:', f, siz
    i = ProductImage (image=f, product=o, published = (siz > 5000))
    i.save()


class CatPhotos (ModelPhotos):  # with apologies to Mr. Wishta
  model = Categories

  def create (self, o, f, siz):
    print 'Creating:', f, siz
    i = CategoryImage (image=f, category=o, published = (siz > 5000))
    i.save()


## Main

pp = ProdPhotos()
pp.photo_loop()

print
print 'Published prods with no dir:', pp.no_dir_count




# TODO: Count the dirs with/without a prod, and prods with/without a dir, and which ones are published...

# then upd db tables with the actual imges
# and add exclude field
# and pre-populate exclude with under 22K (Or whatever it was)

