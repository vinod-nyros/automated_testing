import re #, os

from BeautifulSoup import BeautifulSoup

trace = 0


# Name Inspired by the Stone IPA @ Sauce, Gough st, SF CA 11/28/08 - PumpkinSoup?!
class StoneSoupTemplate (BeautifulSoup):  # MlTemplate?
  def __init__ (self, src=None, path=None):
    if path: src = file (path).read()
    src = src.replace('%','%%')
    BeautifulSoup.__init__ (self, src)

  def ids (self, id_or_regex=re.compile(".*")):
    lst = self.findAll (id=id_or_regex)
    return lst

  def id (self, id_to_find):
    lst = self.ids (id_to_find)
    assert len (lst) in (1,0)
    if lst: return lst [0]

  def replaceIds (self, **kw): #def replaceInnerHtml (**kw):
    #if trace: print 'REPLACE IDS', kw.items()
    for k,v in kw.items():
      for id in self.ids (k):
        if trace: print 'REPLACING:', k, v #len (v)
        id.contents = []
        id.append (v)
    return self

  render = replaceIds  # cosmetic, for now

  def prepare (self, ids):  # change to 'compile'!
    if trace: print 'PREPARE SOUP', ids
    if not self.head:
      self.html.insert (0, Tag (self, 'head'))

    if 'base' in ids: # set up base tag - get from request, at render/call-time
      ids.remove ('base')
      if self.base:
        self.base ['href'] = '%(base)s'
      else:
        self.head.insert (0, '<base href="%(base)s" />')

    if 'title' in ids:
      ids.remove ('title')
      if self.title:
        self.title.contents = '%(title)s'
      else:
        self.head.insert (1, '<title>%(title)s</title>')

    # if 'meta' in ids:  # need to enh to deal with meta kw, meta desc, etc

    if 'header_extras' in ids:
      ids.remove ('header_extras')
      self.head.append ('%(header_extras)s')
      # bsoup 3.04 requires this:
      # self.head.insert (99,'%(header_extras)s')
      #print self.head

    if 'footer_extras' in ids:
      ids.remove ('footer_extras')
      self.body.append ('%(footer_extras)s')

    kw = dict ([(id, '%(' + id + ')s') for id in ids])

    # could do it this way:
    #for k in 'doctype base title meta header_extras footer_extras'.split():
    #  if k in kw:
    #    v = kw.pop (k)

    self.replaceIds (**kw)
