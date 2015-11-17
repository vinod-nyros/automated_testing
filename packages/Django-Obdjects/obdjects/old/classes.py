import re, os
from inspect import isfunction, getmembers, ismethod, isclass #, getclasstree 
from copy import deepcopy
from pprint import pformat
from operator import isMappingType

from django.http import HttpResponse
from django.template import Context, Template
from django.template.defaultfilters import slugify
from django.utils import simplejson as json

from eracks.obdjects.models import Snippet # , Site, Page

from BeautifulSoup import BeautifulSoup
from minitags import script, ul, li, a as link, h1
#tr, td, a as link, p as para, ul, li, h1,h2, form, treo, table, tr, td, th, img, div
#from eracks.products.models import Product, Category

# TODO:
#  build members list, exclude _, instantiate classes
# fix URLs to not instantiate multiple copies - build urlbuilder or dispatcher into views or produts/urls
# js reverse / hash dict, early / late binding


# OK, quickie class hierarchy:
# WebObdj - abstr base - ABC
#   has call, render
#   takes template
#   takes js members
# WebSnippet -
#   subobject,
#   has parent,
#   renders partial/string,
#   adds js to parent, or exposes js to parent
#   takes call (self, req, ses, **kw)
# WebPage -
#   has doctype,base
#   adds on render,
#   is full page,
#   renders httpresp,
#   integrates header_... etc, inserts js, css, meta
#   takes call (self, rew, **kw)
# Javascript - instead of, or inh from, WebSnippet?
#   place - header, top, bot, footer, current/inplace


trace = 0

def islist (x):
  if not isinstance (x, (str, unicode)) and (isinstance (x, (list, tuple))): return True

# todo: implmentore full-feaured Javascript class
def js_tags (files=None, tag=None, txt=None):
    rslts = []

    if files:   # one or a list of files
        if not islist (files):
            files = [files]
        rslts += [script ('', type="text/javascript", src=j) for j in files]

    if tag:     # already has script tag
        rslts += [tag]

    if txt:     # inner js, needs script tag
        rslts += [script (txt, type="text/javascript")]

    return '\n'.join (rslts)


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
    # WARNING: Don't we want to double-up the %s => %%?

    # could do it this way:
    #for k in 'doctype base title meta header_extras footer_extras'.split():
    #  if k in kw:
    #    v = kw.pop (k)

    self.replaceIds (**kw)
    #if trace: print 'TEMPLATE:', `self`

# finish / uncomment this, to make it more workalike with django, zope templates
#  def render (self, **context):
#    #if trace: print context
#    #return str (self.replaceIds (**context))  # whoops! let's try this:
#    return str (self) % context


class WebObdject (object):
  _root    = ''     # '/be/sure/to/set/a/file/system/base/location/if/desired'
  _template = ''     # joined with _root
  _late_binding = True  # _debug, too
  _prepared = False
  _template_class = StoneSoupTemplate
  _url = None

  base     = ''     # '/relative/or/absolute/url/base/location'
  doctype  = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">'
  header_extras = ''
  footer_extras = ''
  js = ''
  css = ''

  def __init__ (self, **kw):
    if trace: print 'INIT:', self.__class__.__name__, ':',
    self._data = {}
    #self._urls = [getattr (self.url, self.__class__.__name__.lower() HERE ]
    self._urls = [] # self._url + registerObdjects (self)

    for nam,cls in iterObdjects (self, (WebSnippet,)):  #  DbSnippet)):
      if trace: print '%s/%s' % (self.__class__.__name__, nam),
      inst = cls()
      inst.name = nam.lower() # shouldn't this be where we call .lower()? lets try it - JJW 1/9/9
      self.__dict__ [nam.lower()] = inst
      self._urls += [inst._url]

    for nam,inst in kw:  # assume obj is already instantiated, or is fn, literal, etc
      if trace: print 'kw %s/%s' % (self.__class__.__name__, nam),
      #inst.name = nam # assume already lowercase
      self.__dict__ [nam] = inst
      #self._urls += [inst._url]

    if trace: print

    if not self._late_binding:
      self._prepare()

  @property
  def _name (self):
    # not necessary, this is the default behavior!
    #if not hasattr (self.__class__, '_name'):  # allow local override with _name = 'blah'
    return slugify (self.__class__.__name__)

  # some parms, like base, doctype, css, and js, are completed at prepare time, rather than at render-time -
  # we might want to move the js stuff to render-time, for header_js, footer_js, header_bottom, header_extras, etc
  def _prepare (self):
    if trace: print 'PREPARE:', self.__class__.__name__
    #print 'CONTENT:', getattr (self, 'content', 'Not there!')

    # first set up template
    if self._template:
      self._template = self._template_class (path = os.path.join (self._root, self._template))

    # prepare ids list to advise tempalte of the fields to accept
    ids = [k for k,v in iterMembers (self)]

    #print 'K,V', [(k,len(`v`)) for k,v in iterMembers (self)]
    # now prepare / compile template as needed
    prep = getattr (self._template, 'prepare', None)
    if prep: prep (ids)  # compiles, for MLT, eg

    # These could be moved into a class - HeaderItems?
    #headx = []
    #footx = []

    # now bind my header/footer js.css - NOTE: v2.0 implem: these can be late-bound, too, depending on if they are callable
    for k,v in iterMembers (self):
      if k in ['js','css'] or k.startswith ('header_'):
        #print 'MY HEADER XTRAS', v
        self.header_extras += v
        #if not v in headx: headx += v if islist (v) else [v]
      if k.startswith ('footer_'):
        self.footer_extras += v
        #if not v in footx: footx += v if islist (v) else [v]

    # now bind the *members'* header/footer js.css
    for k,v in iterMembers (self):
      if isinstance (v, WebObdject):  # hasattr (v, '_prepared'):
        if not v._prepared: v._prepare()
      # skip js, css - we only need these iff fns want to add .js to themselves - maybe 2.0
      if hasattr (v, 'header_extras') and v.header_extras:  # extra check is for soup, hasattr always returns true
        #print 'HEADER XTRAS', v.header_extras
        self.header_extras += v.header_extras
      if hasattr (v, 'footer_extras') and v.footer_extras:
        #print 'FOOTER XTRAS', v.footer_extras
        self.footer_extras += v.footer_extras

    #set self.head/footer_items fm headx & footx here

    # now set up data array
    self._data = dict ((k,v) for k,v in iterMembers (self))

    # expose methods after data dict build:
    #self.render = self._render
    #self.prepare = self._prepare

    if trace: print 'PREPARED:', self.__class__.__name__, [(k,len(`v`)) for k,v in self._data.items()] 
    self._prepared = True
    return self # chainable


  def _host (self, req):
    pfx = 'https://' if req.is_secure() else 'http://'
    return pfx + req.get_host()

  # not used at the moment
  #def _render (self): # called by __call__ after ctx dict setup
  #  if not self._prepared: _prepare()

  def __call__ (self, req, **kw):
    if not self._prepared: self._prepare()

    if not self.base:
      #self.base = req.get_host() nope, unless we stop using _data and use iterMembers
      self._data ['base'] = self._host (req)

    if req.is_ajax():  # and hasattr (self, '_ajax'):
      try:
        rslt = self._ajax (req, req.session, **kw)
        if isMappingType (rslt):
          # text/plain is seen by jQuery as 'string', app/json too, app/javascript nfg too
          # , mimetype="application/javascript") looks like we'll have to do it in the js
          return HttpResponse (json.JSONEncoder().encode(rslt))
        else:
          return HttpResponse (rslt)
      except Exception, e:
        return HttpResponse (e) # should return alert script, here!

    return HttpResponse (self.doctype + self._render (req, req.session, **kw))

  def _render (self, req, ses, **kw):  # full-render dispatcher w/template
    s = unicode(self._template)
    dct = dict([(k,v(req,req.session,**kw) if callable(v) else v)
                  for k,v in self._data.iteritems()]) # if not k in ['template']])

    if trace: print 'CALL', self.__class__.__name__ # , ' content: ', `self.content` [:80]
    if trace: print 'DCT', pformat (dct.keys()), 'BASE', dct['base'] #, 'HDR', dct['header_extras']
    return s % dct
    #return HttpResponse (self.doctype + s % dct)


  def _ajax (self, req, ses, **kw):  # ajax dispatcher
    #c = getattr (self, 'content', getattr (self, '_content', None))
    #if c: return c (req, ses, **kw)  # takes 3, not 4 args - must be bound already!
    if hasattr (self, 'content'): return self.content (req, ses, **kw)
    if hasattr (self, '_content'): return self._content (req, ses, **kw)
    return h1 ('Subclass must provide _ajax or content method, or _content')

  def _ajax_old (self, req, tail):  # ajax dispatcher
    #print 'AJAX', `self`
    fn = getattr (self, tail)  # for now, assume it's only the func name / id
    if isclass (fn) and issubclass (fn, WebObdject):
      fn = fn(self)
    return HttpResponse (fn (req, req.session, tail=tail))


class WebSnippet (WebObdject):  # assumes instantiated by outer shell class
  _url = (r'^test2/$', 'eracks.products.jquerytest.jquerytestpage2')  # dummy for now
  #def prepare (self): pass

  def __call__ (self, req, ses=None, **kw):
    if not self._prepared: self._prepare()

    if req.is_ajax() and hasattr (self, '_ajax'):
      return self._ajax (req, ses or req.session, **kw)

    return self._render (req, ses or req.session, **kw)


class WebPage (WebObdject):  # for inh tree
  pass


#class DbSnippet (Snippet):  # cant do this, collides with the Django machinery, which uses the same technique (!):
  # Error when calling the metaclass bases:
  #   unbound method _prepare() must be called with Distributors instance as first argument (got nothing instead)

class DbSnippet (object):  # Mixin, designed to be nested in MenuSnippet, OR mixed in with UserPage - JJW
  #def __init__ (self, nam=None):
    #if nam: self.name = nam
  def _get (self):
    #print 'INIT/PREPARE!', slugify (self.name)
    try:
      snippet = Snippet.objects.get (slug=slugify (self.name))  # should clean up _name vs name refs
      #print 'FOUND!', snippet.title
      self.title = snippet.title
      self._body = snippet.body
      self.js = snippet.js # later, move to lists, reduced at final prepare: [snippet.js]
      self.css = snippet.css # ditto
      # meta:
      self.header_extras = '\n'.join ([m.as_tag for m in snippet.meta.all()])
      self._url = snippet.get_absolute_url()
      self._snippet = snippet
    except Exception, e:
      self._snippet = None
      self.title = 'Page not found'
      self._body = `e`
      self._url = '/%s/' % getattr (self, 'name', getattr (self, '_name', 'none'))  # '%s/%s/' % (self.base, self.name)
      #print self.content, self.name

  def content (self, req, ses, **parms):
    if not hasattr (self, '_body'): self._get()
    return self._body
'''

  @property
  def _url (self):  # need to distinguish btw incoming & outgoing urls!
    #return r'^%s/$' % self.name
    #if hasattr (self, 'name'):  # otherwise error in getmembers, due to the property being accessed before name is set
    if self.snippet:
      return snippet.get_absolute_url()
    else:
      return '/%s/' % self.name  # '%s/%s/' % (self.base, self.name)


class DbSnippet (WebSnippet):  # designed to be nested in MenuSnippet - JJW
  #_late_binding = True

  #def _prepare (self): pass  # late_binding needs work..
  def _prepare (self):
    print 'PREPARE!'
    try: snippet = Snippet.objects.get (name=slugify (self.name))  # should clean up _name vs name refs
    except: 
      self.title = 'Page not found'
      self.content = 'Empty Page'
      print self.content
      return

    self.title = snippet.title
    self.content = snippet.body
    if self.js: self.js += snippet.js # later, move to lists, reduced at final prepare: [snippet.js]
    if self.css: self.css += snippet.css # ditto
    # meta:
    self.header_extras += '\n'.join ([m.as_tag for m in snippet.meta.all()])
    WebSnippet._prepare (self)

  @property
  def _url (self):  # need to distinguish btw incoming & outgoing urls!
    #return r'^%s/$' % self.name
    if hasattr (self, 'name'):  # otherwise error in getmembers, due to the property being accessed before name is set
      return '%s/%s/' % (self.base, self.name)

  def _ajax (self, req, ses, **kw):
    return self.content

  def _render (self, req, ses, **kw):
    #self.prepare2()
    return HttpResponse (self.content)
'''

class WebMenu (WebSnippet):  # takes list of pages, renders menu
  _pages = []  # by list
  _tag = ''       # by tag - NYI

  def __init__ (self, tag=None, pages=None, words=None, format='_as_ul'):
    if words: self._pages = words.split()
    elif pages: self._pages = pages
    elif tag: self._tag = tag

    if format: self._format = format
    #thedict = self.__dict__
    #theclassdict = self.__class__.__dict__
    #self._render = self.__class__.__dict__ [render]
    WebSnippet.__init__(self)

  def _prepare (self):
    if self._tag:
      from tagging.models import Tag, TaggedItem
      tag = Tag.objects.get(name=self._tag)
      lst = TaggedItem.objects.get_by_model (Snippet, tag)
    else:
      # easy way, but capitalization difficulties:
      lst = Snippet.objects.filter (name__in=[p for p in self._pages])

    self._links = [link (o.name, href=o.url, title=o.title) for o in lst]
    #WebSnippet._prepare (self)
    return self # make chainable

  def _as_middot (self, *args, **kw):
    return '&middot;'.join (self._links)

  def _as_ul (self, *args, **kw):
    return ul (li (self._links))

  def _render (self, req, ses, **kw):
    return self.__class__.__dict__ [self._format](self)


#Yuk!
class MenuSnippet (WebSnippet):  # takes list of pages & creates nested DbSnippets - JJW
  _pagelist = []

  def NO__init__ (self): #, pagelist):
    WebSnippet.__init__ (self)

    if trace: print 'PAGELIST:', self._pagelist
    if self._pagelist:  # allows for future manual setting of pl
      for x in range (len(self._pagelist)):
	nam = self._pagelist [x]
        nam = slugify (nam)
        obj = DbSnippet()
        obj.name = nam
	if trace: print 'NAM:', nam
        self._pagelist [x] = nam,obj
    if trace: print 'PAGELIST:', self._pagelist
    return
    
    # old:
    
    #for snpt in Snippet.objects.get (tag__in=[self._name]):
    #  self.__dict__ [snpt.name] = DbSnippet
    for nam in self._pagelist:
      #Snippet.objects.get (name=nam) defer!
      self.__dict__ [nam] = DbSnippet

    WebSnippet.__init__ (self)

  def _prepare (self):
    if self._prepared:
      if trace: print 'ALREADY PREPARED!'
      return

    if trace: print 'PAGELIST:', self._pagelist
    if self._pagelist:  # allows for future manual setting of pl
      pl = []
      for p in self._pagelist:
        o = DbSnippet()
        o.name = slugify (p)
        pl.append((p,o))
    self._pagelist = pl
    if trace: print 'NEW PAGELIST:', self._pagelist

    for p,o in self._pagelist: 
      o._get()
      if trace: print o.name, o.title, o._body
    WebSnippet._prepare (self)

  def _as_middot (self):
    #dct = self.__dict__
    #lst = [(p,self.__dict__ [slugify(p)]) for p in self.pagelist]
    return '&middot;'.join ([link (p, href=o._url, title=o.title) for p,o in self._pagelist])

  def _as_ul (self):
    #lst = [(p,self.__dict__ [slugify(p)]) for p in self.pagelist]
    return ul (li ([link (p, href=o._url, title=o.title) for p,o in self._pagelist]))

  def _render (self, req, ses, **kw):
    #return ul (li ([link (k,v.url) for k,v in iterMembers (self)]))
    #return ul (li ([link (p,href=self.__dict__ [slugify(p)]._url) for p in self.pagelist]))
    return self._as_ul()

# - - - - -

def iterMembers (container):  # iter thru class Members, module contents, etc returning only members
    for k,v in getmembers (container):  # , not isclass): nope, negation doesn't work
      if k.startswith ('_'):
          continue

      if not isclass (v):
        yield k,v

def iterObdjects (container, types=(WebObdject,)):  # iter thru class Members, module contents, etc returning only classes
    for k,v in getmembers (container, isclass):
      if k.startswith ('_'):
          continue

      #if isclass (v) and issubclass (v, types):
      if issubclass (v, types):
        assert v
        yield k,v

# - - - - -

# nr yet
def registerObdjects (container):
  if trace: print 'IN NEWER REGOBJS' # , `container`
  for k,v in container.items():
    if isclass (v) and issubclass (v, WebObdject):
      if trace: print 'REGged:', k
