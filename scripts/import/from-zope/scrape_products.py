# nope, doesn't work:
# coding: utf-8

# but this does:
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import datetime
from pyquery import PyQuery
import html5lib
from lxml import etree, html
from urllib2 import urlopen
from urlparse import urlparse
from urllib import unquote

from django.template.defaultfilters import slugify


#### globals

url = 'http://eracks.com/'

trace   = 0
testing = 0
teeth   = 0   # whether to write scraped images
dbteeth = 1   # whether to update db

if dbteeth:
    from products.models import Product


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

    path = '/home/joe/django_eracks/apps/products/static/images/%s/%s' % (target, fname)

    try:
        os.makedirs (os.path.dirname (path))
    except Exception, e:
        if trace: print e

    if teeth:
        open (path, 'wb').write (f.read())

    return '/images/%s/%s' % (target, fname)    # url for retrieval


def scrape_photos (parent, url, slug):
    try:
        f = urlopen (url)
    except:
        if '/' in url:
            url = 'http://eracks.com' + url.replace (' ','%20')
        else:
            url = parent.rsplit ('/', 1) [0] + '/' + url
        print 'Retrying:', url
        try:
            f = urlopen (url)
        except Exception, e:
            print 'GIVING UP:', e, url
            return

    doc = html5lib.parse(f, treebuilder='lxml')  # this didn't work, but above three lines did: encoding='utf-8',
    html.xhtml_to_html (doc)
    jQuery = PyQuery([doc])
    content = jQuery ('td#content')

    images = content ('img')

    for image in images:
        img = PyQuery (image)
        src = img.attr('src')
        newsrc = getimage (src, 'products/' + slug)
        img.attr ('src', newsrc)
        print 'photo:', newsrc


def scrape_product (url, category_slug):
    f = urlopen (url)
    doc = html5lib.parse(f, treebuilder='lxml', namespaceHTMLElements=False)  # this didn't work, but above three lines did: encoding='utf-8',
    html.xhtml_to_html (doc)
    jQuery = PyQuery([doc])
    #content = jQuery ('td#content table').eq(0)
    content = jQuery ('td#content')
    content ('form').remove()

    # used to do this, but some models (eg blades) don't have tables:
    #content = jQuery ('td#content table td').eq (0)

    #if content.is_('table'):
    #    content = content ('table td').eq (0)

    # nope, this was too simplistic - let's take apart the tables - see below in final save
    # nope, this doens't work either. I give up.

    skus = find_sku.findall (url)
    sku = skus [0]
    slug = slugify (sku)

    print sku

    '''
    if sku in ['ESERVE',
     'NAS6X',
     'NAS16X',
     'PREMIUM',
     'TWINSERVE',
     'PREMIUM2',
     'SANDYCORE',
     'i7CORE',
     'i7SHORT',]:
        print 'Skipping..'
        return
    #elif testing and sku != 'NAS12':
    #    print 'Skipping due to testing..'
    #    return
    '''

    content ('.small').filter (lambda notused:
         PyQuery (this).text().startswith ("Per single unit, this configuration's price")).remove()
    content ('.small').filter (lambda notused:
         PyQuery (this).text().startswith ("The base price with this configuration is")).remove()
    content ('.small').filter (lambda notused:
         PyQuery (this).text().startswith ("All eRacks systems come with a Standard")).remove()
    content ('.small').filter (lambda notused:
         PyQuery (this).text().startswith ("The price differences between the default")).remove()
    content ('.small').filter (lambda notused:
         PyQuery (this).text().startswith ("Contact eRacks to inquire about leasing")).remove()

    content ('form').remove()

    content ('#pricetext').remove()
    content ('#warrantynote').remove()
    content ('#closenote').remove()

    xbig = content ('.xbig')
    if xbig:
        xbig ('a').remove()
        inner = xbig.html().replace (':','').strip()
        xbig.replaceWith ('<h5 class=xbig>%s</h5>' % inner)
        print 'xbig replaced:', inner

    font = content('font[size=4], font[size=5]')
    if font:
        font ('a').remove()
        inner = font.text().replace (':','').strip()
        font.replaceWith ('<h5 class="product">%s</h5>' % inner)
        print 'font replaced:', inner

    if testing:
        print
        print sku, 'content:'
        print content.html()

    links = content ('a')
    images = content ('img')

    for link in links:
        a = PyQuery (link)
        href = a.attr('href')

        if href:
            if '?' in href:
                href = href.split('?')[0] # doesn't this get rid of all get parms?
                a.attr ('href', href)

            linkskus = find_sku.findall (href)  # That this is looking for?!!
        else:
            print "Empty Link:", a.html()
            linkskus=[]
            print content.html()

        if linkskus:
            linksku = linkskus [0]
            a.attr ('href', '/products/%s/%s/' % (category_slug, linksku))
            print 'New link:', a.attr('href')
        elif href.startswith ('/Legacy'):
            linksku = slugify (href.split ('/') [-1])
            a.attr ('href', '/products/%s/%s/' % (category_slug, linksku))
            print 'New link:', a.attr('href')
        elif 'ore photos' in a.text():
            print 'Scraping:', href
            scrape_photos (url, href, slug)
            #print 'Removing link (scraped):', href
            #a.remove()
            print 'Updating "more photos" link:', href
            a.attr ('href', '#photos')
            a.attr ('onclick', '$("#photos-tab").click();')
        elif href.endswith ('_photos'):
            print 'Scraping:', href
            scrape_photos (url, href, slug)
            print 'Updating "<prod>_photos" link:', href
            a.attr ('href', '#photos')
            a.attr ('onclick', '$("#photos-tab").click();')

    for image in images:
        img = PyQuery (image)
        src = img.attr('src')
        newsrc = getimage (src, 'products/' + slug)
        img.attr ('src', newsrc)
        print 'image:', newsrc

    if dbteeth:
        #prod, created = Product.objects.get_or_create (sku=sku)  # prods are already in the db, silly!
        prod = Product.objects.get (sku=sku)
        prod.comments = prod.comments + '\n\nScraped from Zope as of ' + str(datetime.date.today())
        #prod.description = content.text() + '<br>'.join ([PyQuery(c).html() for c in content ('td')])  # content.html()
        prod.description = content.html()
        # save image(s):
        # prod.image =
        # prod.images.add (name, title, src, etc)
        prod.save()
        print '..saved.'


def scrape_category (url, title):
    category_slug = slugify (title)

    #if testing and category_slug != 'storage-servers-nas':
    #    return

    try:
        f = urlopen (url)
    except ValueError:
        if trace: print 'Retrying:', url
        url = 'http://eracks.com' + url.replace (' ','%20')
        if trace: print 'As:', url
        f = urlopen (url)

    doc = html5lib.parse(f, treebuilder='lxml', namespaceHTMLElements=False)  # this didn't work, but above three lines did: encoding='utf-8',
    html.xhtml_to_html (doc)
    jQuery = PyQuery([doc])

    prods = jQuery ('#products a').filter (lambda not_used: 'config?sku=' in PyQuery(this).attr('href'))

    for a in prods:
        scrape_product (PyQuery(a).attr ('href'), category_slug)


#### main

import re
#find_sku = re.compile ('config\?sku=(\w+)')  # \w doesn't do dashes
find_sku = re.compile ('config\?sku=([^&]+)')  # \&.*

#print find_sku.search ('/products/Enterprise%20Servers/config?sku=ENTERPRISE&session=11706171452858578')
#print find_sku.findall ('/products/Enterprise%20Servers/config?sku=ENTERPRISE&session=11706171452858578')
#print find_sku.findall ('/products/Enterprise%20Servers/config?sku=ENTER_PR-ISE')
#sys.exit()

if testing:
    url = 'http://eracks.com/products/Storage%20Servers%20-%20NAS/config?sku=NAS12'
    #url = 'http://eracks.com/products/Blade%20Servers/config?sku=XBLADE'
    print find_sku.findall (url)
    scrape_product (url, 'storage-servers-nas')
    sys.exit()


f = urlopen (url)
doc = html5lib.parse(f, treebuilder='lxml', namespaceHTMLElements=False)  # this didn't work, but above three lines did: encoding='utf-8',
html.xhtml_to_html (doc)
jQuery = PyQuery([doc])


for a in jQuery ('#products a'):  #  [-1:]:  # skip 'Legacy' at the end
    a = PyQuery (a)

    title = a.text()
    href = a.attr ('href')

    print  'Working on:', slugify (title), title #, href
    scrape_category (href, title)
    print 'Done:', title
    print


