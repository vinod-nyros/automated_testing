
from myconfig import *
from myutil import *
from tags import tagimp
import urllib                   # for quote
import urlparse                 # for getsecurehost
import string                   # for getsecurehost

from copy import deepcopy       # JJW 8/22/3 for deepcopy changes, below

### generic callsql proc, returns two dictionaries in 2D

def callsql (self, sql):
  assert callable (sql) == hasattr (sql, '__call__'), "callable (sql) == hasattr (sql, '__call__')"

  if hasattr (sql, '__call__'):
    r = sql()
  else:
    r = sql

  names = r._names
  idname = names [0] # use 1st one

  dict = {}

  for row in r:
    subdict={}

    for i in range (len (names)):
      subdict [names [i]] = row [i]

    dict [row [idname]] = subdict

  return dict


### cache product configs here - build it as needed in getpoc

prods = {}     # { 'NAT', getpoc ('NAT'), ... }


### getpoc - get Product, Options & Choices - fills session w/3-deep outline of dicts fm 3 sqls
#
# JJW 8/22/03 great candidate for stproc in pgsql! even callsql can be in there!

def getpoc (self, sku):
  #if prods.has_key (sku):
  #  self.session ['prod'] = copy.deepcopy (prods [sku])
  #  return sku
  
  getProduct = self.sql.getProduct
  getProductOptions = self.sql.getProductOptions
  getOptionChoices = self.sql.getOptionChoices

  #sku = self.id #PARENTS [0] nope - see below
  #sku = str (self.this().__name__) #REQUEST.steps [-1]
  #sku = self.REQUEST.steps [-1] works!
  #sku = self.REQUEST.get ('sku', 'NAT')
  prod = callsql (self, getProduct (sku=sku)) # baseprice, name, id, etc

  if len (prod):
    prodid = prod.keys()[0]
    prod = prod.values()[0]
    opts = callsql (self, getProductOptions (prodid=prodid)) # option ids, name, (defaultchoice?)
  else:
    opts = {}

  for opt in opts.values():
    choices = callsql (self, getOptionChoices (prodid=prodid, optid=opt['optid']))  # option choices, pricedelta, defaultchoice
    opt ['choices'] = choices

  prod ['opts'] = opts
  prod ['sku'] = sku
  prod ['qty'] = 1  
  prod ['totprice'] = prod ['baseprice']
  prod ['notes'] = ''
  
  #if not prod.has_key ('weight'): prod ['weight'] = 25  # default system weight
  if not prod.has_key ('weight'): prod ['weight'] = 40  # default system weight
  
  self.session ['prod'] = prod
  #prods [sku] = copy.deepcopy (prod)
  return sku # self.id nope - returns folder id even for doc, unless passed 'this()', which then can't find session


def getsku (self):  # called by product dtml, calls getpoc
  ses = self.session
  req = self.REQUEST
  return getpoc (self, req.steps [-1])


### sesurl (should be called seslink) - return formatted <a ...>...</a> tag

# host = 0 ==> don't prepend host 
# host = 1 ==> prepend standardhost 
# host = 2 ==> prepend securehost, unconditionally append session

def sesurl (ses, req, url, host=0):                     # called fm here
  if host == 1:
    #standardhost = getstandardhost (req.SERVER_URL)	# formerly mymodules.standardhost
    url = '%s/%s' % (standardhost, url)
  elif host == 2:
    #securehost = getsecurehost (req.SERVER_URL)		# formerly mymodules.securehost
    url = '%s/%s' % (securehost, url)

  if req.environ.has_key('HTTP_COOKIE'): # JJW 8/16/3 - https name now matches http name, so no need for this: and host != 2:  
    # Client accepts cookies, so just return url. If the client accepts cookies but there's no cookie set for our domain, 
    # this will mistake the client as non-cookie-enabled, so it sends the ?session=<session> once needlessly the first time.
    return url
  else:
    if '?' in url:
      return '%s&%s=%s'%(url, ses.cookie_name, ses.getName())
    else:
      return '%s?%s=%s'%(url, ses.cookie_name, ses.getName())


def seslink (self, href, text, **kw):                   # called fm dtml as 'sesurl' (should be changed to seslink!)
  #kw ['href'] = self.session.url (href)
  kw ['href'] = sesurl (self.session, self.REQUEST, href)
  return tagimp ('a', text, kw)

def rootlink (self, href, text, **kw):                  # called fm dtml
  rootpath = self.REQUEST.SERVER_URL  # formerly mymodules.rootpath
  href = '%s/%s' % (rootpath, href)
  kw ['href'] = sesurl (self.session, self.REQUEST, href)
  return tagimp ('a', text, kw)

def securelink (self, href, text, **kw):                # called fm dtml 
  kw ['href'] = sesurl (self.session, self.REQUEST, href, 2)
  return tagimp ('a', text, kw)

def standardlink (self, href, text, **kw):              # called fm dtml 
  kw ['href'] = sesurl (self.session, self.REQUEST, href, 1)
  return tagimp ('a', text, kw)

def ishttps (req):
  #return find (req.URL, 'https', 0, 6) >= 0
  #return find (req.URL, '/SSL') >= 0                    # also, the HTTP_VIA field looks promising: 1.0 *.securepages.org:443 
  #return find (req.get_header ('HTTP_VIA'), ':443') >= 0 # the HTTP_VIA header looks like: 1.0 *.securepages.org:443    
  # NOTE: 7/02 JJW - HTTP_VIA no longer contains the :443!
  # JJW 8/16/3 - shorten to 'secure'

  via = string.lower (req.get_header ('HTTP_VIA') or '')
  
  if via:
    return find (via, ':443') >= 0 or find (via, 'secure') >= 0
  else:
    return 0

#def iscobranded (req, brand):
#  return find (req.get_header ('HTTP_VIA'), brand) > 0

def iswww (req):
  #via = req.get_header ('HTTP_VIA')), 'www.') > 0
  return find (string.lower (req.get_header ('HTTP_VIA') or ''), 'www.') > 0

def has2sessions (req):
  cookies = req.get_header ('HTTP_COOKIE')
  if cookies:
    req ['cookies'] = cookies
    first = find (cookies, 'session')
    req ['first'] = first
    if first >= 0:
      req ['second'] = find (cookies [first + 7:], 'session')
      return find (cookies [first + 7:], 'session') >= 0
  return 0
  

### update - called from standard_html_header, updates state with form vars, redirects, etc

def update (self):
  ses = self.session
  req = self.REQUEST
  ses ['request.environ'] = req.environ  # __dict__.values()  # {1:2, 2:3, 3:4} works..
  ses ['request.form']    = req.form   
  #standardhost = getstandardhost (req.SERVER_URL)    # formerly mymodules.standardhost
  #securehost   = getsecurehost   (req.SERVER_URL)    # formerly mymodules.securehost

  req ['updaterv'] = 1.5

#  if ishttps (req): 
#    ses._v_SessionUIDChanged = 1   # this forces the client to save the 'new' session to the eracks.securepages.org domain
#    #req.RESPONSE.base = securehost 
#  elif iswww (req):

  if iswww (req):
# elif find (string.lower (req.SERVER_URL), 'www.') >= 0: 
#    req.RESPONSE.redirect (standardhost)
    req.RESPONSE.base = standardhost 

#  req.RESPONSE.base = ''           # this is necessary so that in production, a 'base' tag is not set with 127.0.0.1 in it.  
#                                   # See BaseRequest.setBase, insertBase, & traverse

  ip = req ['HTTP_X_FORWARDED_FOR']
  if ip:
    if ip in self.fakepage.thelist:  # ['68.5.76.230', '1.2.3.4']:  # , nix, brett, ale, bots, etc]:
      #req.RESPONSE.redirect ('http://216.39.99.117')   # 'some old site or mit.edu')
      req.RESPONSE.setStatus (404)
      req.RESPONSE.setHeader ('Content-Type', 'text/html')
      req.RESPONSE.write (self.fakepage())  #'')
      return ''

  agt = req ['HTTP_USER_AGENT']
  if agt:
    # use fakepage.agentlist, but whether to find, match, or regex?
    #if agt.find ('Gecko'):
    #  req.RESPONSE.write ('aha')
    #  return ''
    pass
      
  if has2sessions (req):
    req.RESPONSE.expireCookie ('session', domain='www.eracks.com', path='/')
    req.RESPONSE.redirect (standardhost)
    req ['extra cookie erased'] = 1

  if hasattr (req, 'emptycart'):
    #ses.clear()  # wipes cart, config, wishlist, checkout, everything
    ses ['cart'] = {}
    getpoc (self, 'NAS')
 
  elif hasattr (req, 'edit'):  # point session.prod to cart line to edit - assumes valid cart
    cart = ses ['cart']
    edit = int (req.edit)
    #return `edit` + ' keys:' + hq (`cart.keys()`)
    ses ['prod'] = cart [edit]
  
  elif hasattr (req, 'updqty'):  # update quantities in shopping cart
    cart = ses ['cart']
        
    newqties = req ['updqty']
    ordlines = req ['ordlin']

    if type (ordlines) == type (''):
      linecount = 1
      ordlines = (ordlines,)
      if type (newqties) == type (''):   # netscape/mozilla also add the button's 'value' prop to the list, since it has the same name (unfortunately).
        newqties = (newqties,)
    else:   # its already a list
      linecount = len (ordlines)   
     
    #req.form ['linecount'] = linecount #for debugging

    for i in range (linecount):
      qtystr = newqties [i]
      if len (qtystr):  # solves 0 vs null problem
        newqty = int (qtystr)
        ordline = int (ordlines [i])
        cart [ordline] ['qty'] = newqty

    # now delete qty 0 items and maintain correct lineitem numbers

    vals = cart.values()
    vals.reverse()
    cart = {}
    newline = 1
    for lineitem in vals:
      if lineitem ['qty'] > 0:
        cart [newline] = lineitem
        newline += 1
    
    ses ['cart'] = cart
  
  elif hasattr (req, 'choiceid'):  # came from detail form, update the choices - assumes valid prod
    prod     = ses ['prod']
    opts     = prod ['opts']
    totprice = prod ['baseprice']
    summary  = ''

    if type (req.choiceid) != type([]):
      req.choiceid = [req.choiceid]

    for tuple in req.choiceid:     # update user selections, total price, summary
      optid, userchoiceid = eval (str (tuple))
      opt = opts [optid]
      opt ['selectedchoiceid'] = userchoiceid
      defaultchoiceid  = opt ['defaultchoiceid']
      choices = opt ['choices']
      choice = choices [userchoiceid]
      totprice = totprice + choice ['pricedelta']
      if defaultchoiceid != userchoiceid:
        desc = choice ['Choices']
        summary = summary + iff (summary, ', ' + desc, desc)

    if not summary:
      summary = 'Default Configuration'

    if hasattr (req, 'notes') and req.notes:
      summary = summary + ' notes:' + req.notes

    prod ['totprice'] = totprice   # save back to the session
    prod ['summary']  = summary
    prod ['notes']    = req.notes

    if hasattr (req, 'addtocart.x'):  # assumes valid prod, and updated totprice and summary - must be called fm form!
      prod2 = deepcopy (prod)             # JJW chgd fm copy to deepcopy 8/22/3
      prod2 ['opts'] = deepcopy (opts)    # JJW chgd fm copy to deepcopy 8/22/3
      #cart = ses ['cart'] or {}
      cart = iff (ses ['cart'], ses ['cart'], {})
      cart [len(cart)+1] = prod2
      ses ['cart'] = cart
      req.RESPONSE.redirect (ses.url (standardhost + '/cart'))
    elif hasattr (req, 'saveconfig.x'):  # wishlist - same as cart, for now
      prod2 = deepcopy (prod)             # JJW chgd fm copy to deepcopy 8/22/3
      prod2 ['opts'] = deepcopy (opts)    # JJW chgd fm copy to deepcopy 8/22/3
      wish = iff (ses ['wish'], ses ['wish'], {})
      wish [len(wish)+1] = prod2
      ses ['wish'] = wish
    elif hasattr (req, 'viewcart.x'):
      req.RESPONSE.redirect (ses.url (standardhost + '/cart'))
    elif hasattr (req, 'quotethissystem.x'):
      req.RESPONSE.redirect (ses.url (standardhost + '/quotes'))
    elif hasattr (req, 'checkout.x'):
      req.RESPONSE.redirect (sesurl (ses, req, 'checkout', 2))
    elif hasattr (req, 'resetconfig.x'):  # assumes valid prod, gets sku fm there
      prod = ses ['prod']
      sku  = prod ['sku']
      ses ['prod'] = {}
      getpoc (self, sku) 
    else:
      assert hasattr (req, 'updateconfig.x'), "hasattr (req, 'updateconfig.x')"  # only other choice! maybe use this for update cart after edit

  elif hasattr (req, 'viewcart.x'):     # clicking view cart from checkout will hit this
    req.RESPONSE.redirect (ses.url (standardhost + '/cart'))

  elif hasattr (req, 'quotethissystem.x'):
    req.RESPONSE.redirect (ses.url (standardhost + '/quotes'))

  elif hasattr (req, 'addtocart.x'):    # it's a retail (standalone) sku
      prod = {'opts':{}}
      prod ['sku']=req.sku
      prod ['Product']='eRacks/' + req.sku  # this should be eliminated in renderer (Line 381) and checkout9
      prod ['summary']=req.summary
      prod ['notes']   = req.notes  # JJW 8/22/3
      prod ['category']=req.category
      prod ['qty']=int (req.qty)
      prod ['baseprice']=float (req.baseprice)
      prod ['totprice']= req.baseprice         # ditto with this duplication
      prod ['weight'] = req.weight
      cart = iff (ses ['cart'], ses ['cart'], {})
      cart [len(cart)+1] = prod
      ses ['cart'] = cart
      req.RESPONSE.redirect (ses.url (standardhost + '/cart'))

  elif hasattr (req, 'sku'):  # fill session with fresh config
    if hasattr (req, 'zopeprods'):  # allow for sw config
      prod = ses ['prod']
      zprods = req.zopeprods
      if type (zprods) == type ([]):
        zprods = '\n'.join (zprods)
      prod ['notes'] = prod ['notes'] + 'Install Zope products:\n' + zprods 
    else:
      sku = req.sku # ['sku']
      getpoc (self, sku)
      #return ses ['prod'] ['sku']

  elif hasattr (req, 'continueshopping.x'):   # clicking continueshopping fm checkout will hit this
    req.RESPONSE.redirect (ses.url (standardhost + '/config'))


### main (for testing and development)

if __name__ == "__main__":
  import urllib
  u = urllib.urlopen ('http://joe:semaj@eracks733:8080/eRacks/compile')
  print u.read()
  #if find (u.read(), 'compiled OK'):
  #  print 'OK'

  u.close()


  import traceback

  def stk (self):
    return str (traceback.format_stack()) # + '\n' + str (traceback.format_tb())

