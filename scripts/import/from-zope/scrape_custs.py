# nope, doesn't work:
# coding: utf-8

# but this does:
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from pyquery import PyQuery
import html5lib
from lxml import etree, html
from urllib2 import urlopen # 2 as urlopen

from django_eracks.apps.customers.models import CustomerImage


## globals

url = 'http://eracks.com/customers'

teeth = 0   # whether to write scraped images


## main

f = urlopen (url)

doc = html5lib.parse(f, treebuilder='lxml')  # this didn't work, but above three lines did: encoding='utf-8',

print html.xhtml_to_html (doc)

jQuery = PyQuery([doc])


def getimage (src):
    f = urlopen (src)
    info = f.info()
    fname = src.split ('/') [-1] + '.' + info.getsubtype()
    path = '/home/joe/Projects/django_eracks/static/images/customers/' + fname 
    if teeth: open (path, 'wb').write (f.read())
    return '/images/customers/' + fname  # url for retrieval

 
href = src = caption = loc = title = ''
sortorder = 100

for td in jQuery ('td#content table td table tr td'):
    #print 'TD:', PyQuery (td).html()
    td = PyQuery (td)
    
    if not href:    href = td('a').attr('href')
    if not src:     src  = td('img').attr ('src')
    if not title:   title = td('img').attr ('title')
    if not caption: caption = td('b').html()
    td('b').remove()
    if not loc:     loc = td('font').text()

    if (href and src and caption and loc):  # title is optional
        #upd db here, getimage
        url = getimage (src)
        print href, src, url, title, caption, loc
        c, created = CustomerImage.objects.get_or_create (
            image = url,
            link  = href,
            title = title if title else '',
            caption = caption,
            location = loc,
            defaults = dict (sortorder = sortorder),
        )
        c.sortorder = sortorder
        c.save()
                        
        href = src = caption = loc = title = ''
        sortorder += 10


