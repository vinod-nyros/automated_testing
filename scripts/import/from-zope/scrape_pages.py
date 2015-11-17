# nope, doesn't work:
# coding: utf-8

# but this does:
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from pyquery import PyQuery
import html5lib
from lxml import etree, html
from urllib2 import urlopen

from tidylib import tidy_document

from django.template.defaultfilters import slugify
from django.db.utils import IntegrityError

from utils import create_or_update

from scrape_utils import no_namespaces #, no_fonts


#### globals

url = 'http://eracks.com/'

teeth = 0   # whether to write scraped images
dbteeth = 1  # whether to update db
trace = 0

if dbteeth:
    from quickpages.models import QuickPage


#### functions

def getimage (src, target):
    if trace: print src, target

    if src.startswith('/'):
        src = 'http://eracks.com' + src  #.replace (' ','%20')
    elif src.startswith('gnw_cs_logo'):
        src = 'http://eracks.com/press/' + src

    print 'GETTING IMAGE:', src

    f = urlopen (src)
    info = f.info()
    if trace: print info
    fname = slugify (src.split ('/') [-1]) + '.' + info.getsubtype()
    path = '/home/joe/django_eracks/apps/home/static/images/%s/%s' % (target, fname)
    if teeth: open (path, 'wb').write (f.read())
    return '/images/%s/%s' % (target, fname)  # url for retrieval


# to get rid of xmlns:... bs:
#objectify.deannotate(root, xsi_nil=True)
#etree.cleanup_namespaces(root)

def scrape (slug, url, name, title=None):
    f = urlopen (url)
    doc = f.read()

    doc, errs = tidy_document(doc,
        options = {
            'output-html':1,
            #'indent':1,
            'clean':1,
            'drop-font-tags':1,
        }
    )
    if errs:
        #raise Exception, errs
        print errs

    doc = html5lib.parse(doc, treebuilder='lxml')  # this didn't work, but above three lines did: encoding='utf-8',
    html.xhtml_to_html (doc)
    jQuery = PyQuery([doc])

    td = jQuery ('td#content')
    assert len (td) == 1

    for img in td ('img'):
        #print 'img:', PyQuery (img)
        img = PyQuery (img)
        src = img.attr('src')
        #alt = img.attr('alt')

        #if src.startswith ('/image'):
        rslt = getimage (src, slug.split ('/')[0])
        img.attr ('src', rslt)
        if trace: print rslt

    #td =
    #no_fonts (td)

    # need to fix links here

    content = PyQuery (td [0])
    #content = content.html()
    content = no_namespaces (content.html())

    print slug, content [:60]  #.html()  # [:60]

    if dbteeth:
        #q, created = QuickPage.objects.get_or_create (

        qp, created = create_or_update (QuickPage, keys = dict(slug = slug), fields = dict(
            name = name,
            title = title if title else name,
            content = content,
            #defaults = dict (sortorder = sortorder),
        ))

        #try:
        #    q.save()
        #except IntegrityError, e:
        #    print e


#### Main

# not used, has old slideshow & stuff:
#scrape ('home', "http://eracks.com/", 'Home')

# not used, replaced by new dynamic products page:
#scrape ('showroom', "http://eracks.com/showroom", 'Product Showroom')

# replaced, hand-edited May 012
#scrape ('partners', "http://eracks.com/partners", 'Partners')

# replaced w/dynamic:
#scrape #('customers', "http://eracks.com/customers", 'Customers')

# no - hand edited May 012
#scrape ('corporate', "http://eracks.com/corporate", 'Corporate')

# handled elsewhere
#scrape #("http://blog.eracks.com"> Blog

# hand-edited May 012
#scrape ('contact-us', "http://eracks.com/contact.html", 'Contact us', title="1-714-532-5322, info@eracks.com")

# heve to pre-delete if uncommmenting these - minimal changes / additions 10/21/12 JJW, add templates, etc
#scrape ('services', "http://eracks.com/services", 'Services')
#scrape ('faq', "http://eracks.com/faq", 'FAQ', title='Frequently Asked Questions')
#scrape ('press', "http://eracks.com/press", 'Press')
#scrape ('privacy-and-legal', "http://eracks.com/policies/legal.html", "Privacy and Legal", title="Privacy, Security, and Legal")
#scrape ('rackmount-servers', 'http://eracks.com/rackmount-servers', 'Rackmount Server Basics')
#scrape ('open-source-links', 'http://eracks.com/links.html', 'Open Source Links')

# done 10/21/12 JJW
#scrape ('warranty-and-order', 'http://eracks.com/policies/orderinfo.html', 'Warranty and Order Policies')

