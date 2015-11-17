# nope, doesn't work:
# coding: utf-8

# but this does:
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import datetime
from pyquery import PyQuery
import html5lib
from lxml import etree, html
from urllib2 import urlopen
from urlparse import urlparse
from urllib import unquote

from django.template.defaultfilters import slugify

#from django_eracks.apps.legacy.models import Categories


#### globals

url = 'http://eracks.com/'

teeth = 1   # whether to write scraped images


#### functions

def getimage (src):
    f = urlopen (src)
    info = f.info()
    fname = slugify (src.split ('/') [-1]) 
    ext = '.' + info.getsubtype()
    
    if not fname.endswith (ext):
        fname += ext

    path = '/home/joe/Projects/django_eracks/static/images/logos/' + fname 

    if teeth: 
        open (path, 'wb').write (f.read())

    return '/images/logos/' + fname  # url for retrieval


#### main

f = urlopen (url)
doc = html5lib.parse(f, treebuilder='lxml')  # this didn't work, but above three lines did: encoding='utf-8',
html.xhtml_to_html (doc)
jQuery = PyQuery([doc])

 
for img in jQuery ('tr#header img'):    
    img = PyQuery (img)
    src = img.attr('src')
    alt = img.attr('alt')

    if src.startswith ('/image'):
        print getimage ('http://eracks.com/' + src)


