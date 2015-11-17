# restate_products - massage old ancient product descriptions - JJW 10/14/15
#
# 1 Remove table & font tags, comments
# 2 Remove div classes
# 3 Remove h4, h5 containing eRacks/
# 4 Remove img w/link pointing to '#photos'
# 5 Remove txt link(s) to 'more photos'
# 6 add begin & end comments

import re, pyquery
from pprint import pprint
from tidylib import tidy_fragment
from myproject import settings

from products.models import Categories, Product, Option, Choice, ChoiceCategory, Prodoptchoice, Prodopt

from django.utils.html import strip_entities, strip_tags, remove_tags


#### Globals

trace = 0
teeth = 1
show = 0

s = ''    # p.description - main string operated on
d = None  # pq obj of s
p = None  # Product object


#### Restate functions

def remove_tags_and_comments():
  global s
  htmlcomments = re.compile('\<![ \r\n\t]*(--([^\-]|[\r\n]|-[^\-])*--[ \r\n\t]*)\>')

  #print 'BEFORE:', s
  s = remove_tags (s, 'table thead tfoot tbody td tr th font TABLE THEAD TFOOT TBODY TD TR TH FONT center CENTER EM em span SPAN')  # p br div P BR DIV
  s = htmlcomments.sub ('', s)
  s = s.strip('\r\n\t')
  s = s.replace ('&nbsp;','')
  #s, errs = tidy_fragment (s, options= {'indent':1, 'wrap': 120, 'merge-divs': 'yes'})
  if trace: print errs

  return True


def remove_div_classes():  # uses s - a string, creates d, a pq obj
  global d
  d = pyquery.PyQuery(s)
  for tag in ['div[style]', 'span[style]']:
    for i in d(tag):
      style = i.attrib['style']
      if style and not style.startswith ('float:'):
        if trace: print tag, 'style removed:', i.attrib['style']
        del i.attrib ['style']

  d('div').remove_attr('class')

  return True

  #for i in d('div'):
  #  print i.tag, i.attrib


def remove_headings_eracks():
  if d('h4:contains("eRacks/")').text().startswith ('eRacks/'):
    d('h4:contains("eRacks/")').remove()
    return True
  elif d('h5:contains("eRacks/")').text().startswith ('eRacks/'):
    d('h5:contains("eRacks/")').remove()
    return True
  elif d('h5:contains("eRacks/QUIET")'):
    d('h5:contains("eRacks/QUIET")').remove()
    return True
  elif d('h4 :contains("eRacks/")').text().startswith ('eRacks/'):
    d('h4 :contains("eRacks/")').parents('h4').remove()
    return True
  elif d('h5 :contains("eRacks/")').text().startswith ('eRacks/'):
    d('h5 :contains("eRacks/")').parents('h5').remove()
    return True
     #d('h5>strong:contains("eRacks/")').text().startswith ('eRacks/') or\
     #d('h5>span:contains("eRacks/")').text().startswith ('eRacks/') or\
     #d('h5>i:contains("eRacks/")').text().startswith ('eRacks/') or\
     #d('h5>b:contains("eRacks/")').text().startswith ('eRacks/'):
  else:
    print d('h4:contains("eRacks/")').text()
    print d('h5:contains("eRacks/")').text()
    print d('h5>strong:contains("eRacks/")').text()
    print d('h5:contains("eRacks/")').text()
    print 'h5', d('h5')

# To check manually, plus Studio3, etc:
# <img alt="" border="0" height="207" src="/images/products/dmz/dmz_open.jpeg" width="350">
#<img alt="1u-height server, top open" border="0" height="161" src="/images/products/dns/1u_top_off_s.jpeg" width="250">
#<img alt="1u-height server, top open" border="0" height="161" src="/images/products/mail/1u_top_off_s.jpeg" width="250">
#<img alt="1u-height server, top open" border="0" height="161" src="/images/products/nat/1u_top_off_s.jpeg" width="250">
#<img alt="1U GRID Chassis" src="/images/products/quiet/grip.jpeg" style="width:300px">
#<img alt="" border="0" height="193" src="/images/products/quote/custom1.jpeg" title="" width="200">
#<img alt="" border="0" height="500" src="/images/products/rackcabinet/rackcabinet_s.png" title="eRacks/RackCabinet" width="356">
#<img alt="" border="0" height="186" src="/images/products/snort/snort_open.jpeg" title="eRacks/TDA - Thin Dual AMD " width="350">
#<img alt="matched pair VPN 185x70" border="0" height="70" src="/images/products/vpn/dual_1u_s.jpeg" width="185">
# Also fix insecure YouTuibe link:
#<img alt="" border="0" src="/images/products/zenbook/zenbook_400.jpeg" title="eRacks/ZENBOOK">
#<img alt="" border="0" height="118" src="/images/products/railkits/railkit20.jpeg" title="Sliding Rail kit" width="250">
#<img alt="" src="/images/products/zenbook15/zenbook15.jpeg">
remove_images_list = ['/images/products/dmz/dmz_open.jpeg',
    "/images/products/dns/1u_top_off_s.jpeg",
    "/images/products/mail/1u_top_off_s.jpeg",
    "/images/products/nat/1u_top_off_s.jpeg",
    "/images/products/quiet/grip.jpeg",
    "/images/products/quote/custom1.jpeg",
    "/images/products/rackcabinet/rackcabinet_s.png",
    "/images/products/snort/snort_open.jpeg",
    "/images/products/vpn/dual_1u_s.jpeg",
    "/images/products/zenbook/zenbook_400.jpeg",
    "/images/products/railkits/railkit20.jpeg",
    "/images/products/zenbook15/zenbook15.jpeg",
  ]

def remove_img_photos():
  if d('a[href="#photos"] img[src^="/images/products/"]'):
    d('a[href="#photos"] img[src^="/images/products/"]').parents('a[href="#photos"]').remove()
    return True
  elif d('img[title^="%s"]' % p.name):
    d('img[title^="%s"]' % p.name).remove()
    return True
  else:
    for i in remove_images_list:
      if d('img[src="%s"]' % i):
        d('img[src="%s"]' % i).remove()
        return True

  print 'a href photos', d('a[href="#photos"]')
  print 'img[title]', d('img[title]')


def remove_more_photos():
  #if d('a[href="#photos"]').text().lower().startswith ('more photos') or \
  if d('a[href="#photos"]:contains("more photos")'):
    d('a[href="#photos"]:contains("more photos")').remove()
    return True
  if d('a[href="#photos"]:contains("More photos")'):
    d('a[href="#photos"]:contains("More photos")').remove()
    return True
  elif d('a[href="#photos"]:contains("more %s photos")' % p.name):
    d('a[href="#photos"]:contains("more %s photos")' % p.name).remove()
    return True
  elif d('a[href="#photos"] :contains("more photos")'):
    d('a[href="#photos"] :contains("more photos")').parents('a[href="#photos"]').remove()
    return True
  else:
    print '(more) a href photos (not fatal)', d('a[href="#photos"]')
    return True

def add_begin_end_comments ():
  global s
  s = '<!-- BEGIN %s PRODUCT CONTENT -->%s<!--END %s PRODUCT CONTENT -->' % (p.sku, s, p.sku)


#### Main

for p in Product.objects.published().exclude(category__name='Legacy Systems'): #.filter(sku='FLAT'):  # OPT4200 STUDIO3 VALUE PREMIUM FLAT
  s = p.description

  print p.sku,

  if remove_tags_and_comments() and \
     remove_div_classes()       and \
     remove_headings_eracks()   and \
     remove_img_photos()        and \
     remove_more_photos():
    s = str (d)
    add_begin_end_comments()

    if teeth:
      p.description = s
      p.save()
      print 'Saved.'
    else:
      if show:
        print 'AFTER:', s
      else:
        print 'YES'

