# nope, doesn't work:
# coding: utf-8

# but this does:
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#import os
#import datetime
from pyquery import PyQuery
import html5lib
from lxml import etree, html
from urllib2 import urlopen
#from urlparse import urlparse
#from urllib import unquote

from django.template.defaultfilters import slugify
from django.contrib.redirects.models import Redirect

from utils import create_or_update


#### globals

url = 'http://eracks.com/press'

trace = 0

teeth = 1   # whether to write scraped images
dbteeth = 1  # whether to update db

if dbteeth:
    from quickpages.models import QuickPage

'''
#### functions

def getimage (src, target):
    try:
        f = urlopen (src)
    except ValueError:
        if trace: print 'Retrying:', src
        src = 'http://eracks.com' + src.replace (' ','%20')
        if trace: print 'As:', src
        f = urlopen (src)

    info = f.info()
    fname = slugify (src.split ('/') [-1])
    ext = '.' + info.getsubtype()

    if not fname.endswith (ext):
        fname += ext

    path = '/home/joe/Projects/django_eracks/apps/products/static/images/%s/%s' % (target, fname)

    try:
        os.makedirs (os.path.dirname (path))
    except Exception, e:
        if trace: print e

    if teeth:
        open (path, 'wb').write (f.read())

    return '/images/%s/%s' % (target, fname)    # url for retrieval


def scrape_category (url, title):
    category_slug = slugify (title)

    try:
        f = urlopen (url)
    except ValueError:
        if trace: print 'Retrying:', url
        url = 'http://eracks.com' + url.replace (' ','%20')
        if trace: print 'As:', url
        f = urlopen (url)

    doc = html5lib.parse(f, treebuilder='lxml')  # this didn't work, but above three lines did: encoding='utf-8',
    html.xhtml_to_html (doc)
    jQuery = PyQuery([doc])

    page_title =  jQuery ('title').text()

    if page_title.startswith ("eRacks Open Source Systems: "):
        page_title = page_title.partition ("eRacks Open Source Systems: ") [-1]

    if page_title.startswith ("eRacks "):
        page_title = page_title.partition ("eRacks ") [-1]

    content = jQuery ('td#content')
    links = content ('a')
    images = content ('img')

    for link in links:
        a = PyQuery (link)
        href = a.attr('href')
        skus = find_sku.findall (href)

        if skus:
            sku = skus [0]
            a.attr ('href', '/%s/%s/' % (category_slug, slugify (sku)))
        elif href.startswith ('/Legacy'):
            sku = slugify (href.split ('/') [-1])
            a.attr ('href', '/%s/%s/' % (category_slug, slugify (sku)))

        print 'link:', a.attr('href')

    for image in images:
        img = PyQuery (image)
        src = img.attr('src')
        newsrc = getimage (src, 'categories/' + category_slug)
        img.attr ('src', newsrc)
        print 'image:', newsrc

    description = content.html()
    if trace: print description

    if dbteeth:
        cat = Categories.objects.get (name=title)
        cat.comments = cat.comments + '\n\nScraped from Zope as of ' + str(datetime.date.today())
        cat.description = description
        cat.title = page_title
        cat.save()
        print '..saved.'

'''

def scrape_redirect (fm, to):
    redir, created = create_or_update (Redirect, keys = dict(old_path = fm, site_id=1), fields = dict(new_path = to))
    print redir


#### main

import re
find_sku = re.compile ('config\?sku=(.*)\&.*')


from scrape_pages import scrape

f = urlopen (url)
doc = html5lib.parse(f, treebuilder='lxml')  # this didn't work, but above three lines did: encoding='utf-8',
html.xhtml_to_html (doc)
jQuery = PyQuery([doc])


for a in jQuery ('td#content table td[colspan=2] a'):
    a = PyQuery (a)

    title = a.text()
    href = 'http://eracks.com/press/' + a.attr ('href')
    redirected_href = '/press/' + a.attr ('href')
    slug = 'press/' + slugify (title)

    print  'Working on:', slug, title, href
    #scrape_category (href, title)
    scrape_redirect (redirected_href, '/' + slug)
    #scrape (slug, href, title)

    print 'Done:', title
    print


