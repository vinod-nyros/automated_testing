# nope, doesn't work:
# coding: utf-8

# but this does:
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from BeautifulSoup import BeautifulSoup as soup, Comment, Tag
import urllib

if 1:
  url = 'http://eracks.com/customers'
  print url
  s = urllib.urlopen (url).read()
  s=soup (s)

  cont = s.body

  # extract text and a few select tags:
  snip = ''
  for e in cont.recursiveChildGenerator():
    if isinstance (e, unicode) or \
       isinstance (e, Tag) and (str(e).startswith (u'<a ') or
                                str(e).startswith (u'<b>') or
                                str(e).startswith (u'<img')):

      s = unicode(e)
      if s.strip() or len (e):
        snip += s # unicode(e) # .extract() nope, confuses the generator
      e.contents = []

  print snip



