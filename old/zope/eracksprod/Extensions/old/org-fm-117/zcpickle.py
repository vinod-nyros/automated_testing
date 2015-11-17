import mymodules

import cPickle, string  # , os, urllib, sys, stat, time, tags, updater, ccards, sendorder2
#from myutil import Dict

#Reload (mymodules)  

class zcPickle: # zConfig pickle
  def __init__ (self, pkl):
    if type (pkl) == type ({}):
      self.pkl = pkl
    else:  # it's a pathname
      self.pkl = getpickle (self, pkl)

  __allow_access_to_unprotected_subobjects__ = 1

  #def __getitem__ (self, k):
  #   return getattr (self, k)

  def env (self):       return self.pkl.get ('request.environ', {}).items()
  def form (self):      return self.pkl.get ('request.form', {}).items()
  def prod (self):      return self.pkl.get ('prod', {}).items()
  def checkout (self):  return self.pkl.get ('checkout', {}).items()
  def cart (self):      return self.pkl.get ('cart', {}).items()
  def wish (self):      return self.pkl.get ('wish', {}).items()

  def ordernum (self):  return self.pkl.get (checkout(), 'ordnum', '')

def zcpickle (pkl): return zcPickle (pkl)

def getpickle (self, path):
  f = open (path)
  pkl  = cPickle.load (f)
  f.close()
  return pkl

def reprses (self):
  ses = self.session
  return repr (ses._v_data)

def evalses (self, ses):
  self.session.update (eval (ses))
  return 'OK'


class zcPickle2:  # zConfig pickle, return pseudo Dict classes
  def __init__ (self, pkl):
    if type (pkl) == type ({}):
      self.pkl = pkl
    else:  # it's a pathname
      self.pkl = getpickle (self, pkl)

  __allow_access_to_unprotected_subobjects__ = 1

  #def env (self):       return Dict (self.pkl.get ('request.environ', {}))
  #def form (self):      return Dict (self.pkl.get ('request.form', {}))
  #def prod (self):      return Dict (self.pkl.get ('prod', {}))
  #def checkout (self):  return Dict (self.pkl.get ('checkout', {}))
  #def cart (self):      return Dict (self.pkl.get ('cart', {}))
  #def wish (self):      return Dict (self.pkl.get ('wish', {}))

  def env (self):       return self.pkl.get ('request.environ', {})
  def form (self):      return self.pkl.get ('request.form', {})
  def prod (self):      return self.pkl.get ('prod', {})
  def checkout (self):  return self.pkl.get ('checkout', {})
  def cart (self):      return self.pkl.get ('cart', {})
  def wish (self):      return self.pkl.get ('wish', {})

  def envitems (self):       return self.env().items()
  def formitems (self):      return self.form().items()
  def proditems (self):      return self.prod().items()
  def checkoutitems (self):  return self.checkout().items()
  def cartitems (self):      return self.cart().items()
  def wishitems (self):      return self.wish().items()


def zcpickle2 (pkl): return zcPickle2 (pkl)


def propids (self, filter):
  '''iterate thru contents of folder and return list of properties held by all the objects (filter) in the folder.'''

  #docs = self.objectItems ('DTML Document')
  docs = self.objectValues (filter)

  ids = []
  
  for doc in docs:
    newids = doc.propertyIds()
  
    for newid in newids:
      if not newid in ids:
        ids.append (newid)
      
  return ids


def deeppropids (self, filter):
  '''recursively iterate thru contents of folder and return list of properties held by all the objects (docs) in the folder.'''

  ids = propids (self, filter)

  folds = self.objectValues ('Folder')

  for fold in folds:
    newids = deeppropids (fold, filter)

    for newid in newids:
      if not newid in ids:
        ids.append (newid)

  return ids


def propvalcounts (self):
  '''count the occurrences of each prop value in a list of docs'''
  
  docs = self.objectValues (filter)

  counts = {}  

  for doc in docs:
    vals = doc.propertyValues()

    for val in vals:
      counts [val] += 1

  return counts


def propvalcounts1 (self, filter):
  '''count the occurrences of each prop value in a list of docs, in 1 level of folders'''

  counts = {}

  folds = self.objectValues ('Folder')

  for fold in folds:
    docs = fold.objectValues (filter)

    for doc in docs:
      vals = doc.propertyValues()

      #return vals

      for val in vals:
        if counts.has_key (val):
          counts [val] += 1
        else:
          counts [val] = 1

  return counts


def addOrder (self):
  req = self.REQUEST
  #ses = self.session
  bp = self.basepath
  id = self.id()
  order = string.split (id, '.') [0]
  result = 'initted'

  p = zcPickle2 (bp + '/' + id)
  prod = p.prod()
  proditems = p.proditems()
  checkout = p.checkout()
  checkoutitems = p.checkoutitems()
  cart = p.cart()
  cartitems = p.cartitems()

  if not checkout or not order:
    return 'invalid pickle'

  try:
    self.manage_addFolder (order, checkout ['email'])
    result = '%s added' % order
  except:
    result = "(Couldn't add folder - Already present?)"

  # return 'self:' + `self`, 'PARENTS [-1]:' + `self.test3 [order]` #`req.PARENTS [-1]`

  fold = self.test3 [order]

  for coi in checkoutitems:
    if coi [1]:
      try:
        fold.manage_addProperty (coi [0], coi [1], 'string')
      except:
        result += '\n Couldnt set %s to %s - already done?      ' % (optname, choicename)

  for i in cart.items():
    #self [id].manage_addDocument (i [0], i [1] [sku])
    #self [id].manage_addDocument (i [0], i [1])

    item = i [1]

    try:
      fold.manage_addDTMLDocument (i [0], item ['sku'])
    except:
      result += "\n(Couldn't add DTML doc %s - Already present?)" % i [0]

    doc = fold [str (i [0])]
    result += '\n %s added' % doc.id()

    for opt in item ['opts'].values():
      selected = opt ['selectedchoiceid']
      choices = opt ['choices']

      choice = choices [selected]
      choicename = choice ['Choices']
      optname = string.replace (opt ['Option'], ' ', '_')

      try:
        doc.manage_addProperty (optname, choicename, 'string')
        result += '\n %s set to %s' % (optname, choicename)
      except:
        result += '\n Couldnt set %s to %s - already done?      ' % (optname, choicename)

  return 'OK ' + result  # + `fold ['1']`


def addprop (o, prop, val, type):
  try:
    o.manage_addProperty (prop, val, type)
    return '\n %s set to %s' % (prop, val)
  except:
    return '\n Couldnt set %s to %s - already done?' % (prop, val)


def addOrder2 (self):	# assumes called fm localFS .pkl item
  req = self.REQUEST
  bp = self.path
  id = self.id
  order = string.split (id, '.') [0]
  result = 'initted'

  p = zcPickle2 (bp)
  prod = p.prod()
  proditems = p.proditems()
  checkout = p.checkout()
  checkoutitems = p.checkoutitems()
  cart = p.cart()
  cartitems = p.cartitems()

  if not checkout or not order:
    return 'invalid pickle'

  try:
    self.parent.root.manage_addFolder (order, checkout ['email'])
    result = '%s added' % order
  except:
    result = "(Couldn't add folder - Already present?)"

  fold = self.parent.REQUEST.PARENTS[0] [order]

  for id, item in checkoutitems:
    if item:	# and id [-4:] != 'info':
      if id == 'instr':       
        result += addprop (fold, id, item, 'lines')
      else:
        result += addprop (fold, id, item, 'string')

  result += addprop (fold, 'orderdate',	self.mtime, 'date')
  #result += addprop (fold, 'invoicedate', '', 'date')
  #result += addprop (fold, 'shipdate', '', 'date')
  ##result += addprop (fold, 'paiddate', 0, 'date')
  ##result += addprop (fold, 'printeddate', 0, 'date')
  result += addprop (fold, 'ccauthnum', 0, 'int')

  if int (order) < 11294:
    result += addprop (fold, 'orderstatus', 'closed', 'statuses')
  else:
    result += addprop (fold, 'orderstatus', 'open', 'statuses')

  for id, item in cartitems:		# (id, obj) tuple
    try:
      fold.manage_addDTMLDocument (id, item ['sku'])
      result += '\n %s added' % doc.id()
    except:
      result += "\n(Couldn't add DTML doc %s - Already present?)" % id

    doc = fold [str (id)]

    result += addprop (doc, 'summary', 	item ['summary'], 	'lines')
    result += addprop (doc, 'qty', 	item ['qty'], 		'int')
    result += addprop (doc, 'baseprice',item ['baseprice'], 	'float')
    result += addprop (doc, 'asconfig', item ['totprice'], 	'float')
    result += addprop (doc, 'totprice', item ['totprice'] * item ['qty'], 'float')
    result += addprop (doc, 'notes', 	item.get ('notes', ''),	'lines')
    #result += addprop (doc, 'shipdate', 0, 'date')
    result += addprop (doc, 'shipper',  '', 'shippers')
    result += addprop (doc, 'tracknum', '', 'string')

    for opt in item ['opts'].values():
      selected = opt ['selectedchoiceid']
      choices = opt ['choices']

      choice = choices [selected]
      choicename = choice ['Choices']
      optname = string.replace (opt ['Option'], ' ', '_')

      result += addprop (doc, optname, choicename, 'string')

  return 'OK ' + result


def addOrders (self):	# assumes called fm localFS item itself
  result = ''
  for o in self.orders.fileValues ('*.pkl'):
    result += addOrder2 (o) + '\n' #'<br><br>'
  return result    
  
  # old:
  lst = []
  for i in self.fileIds ('*.pkl'):
    lst.append (i)
  return `lst`    
  

#def partslist (self):  
#  list = []
#
#  folds = self.objectItems ('Folder')
#  for id, fold in folds:
#    if fold.orderstatus in ['open']:
#      docs = fold.objectItems ('DTML Document')
#      for id, doc in docs:
#        #list += context.propertyIds()
#        list += doc.propertyItems()
#
#  return list


def setProperty (self, id, value):
  return self._setProperty (id, value)

def updateProperty (self, id, value):
  return self._updateProperty (id, value)

def evalProperty (self, id, default=''):
  prop = self.getProperty (id, '')
  if prop:
    if prop [:1] == '=':
      return int (eval (prop [1:], globals(), self.__dict__))
      #return int (eval (prop [1:], self.__dict__))
      #return eval (prop [1:], self.__dict__, self.REQUEST.PARENTS [0].__dict__)
      #return eval (prop [1:], locals(), self.namespace, self.__dict__)
    else:
      return prop
  else:
    return default
    
def sumProperties (self, col, rowstart, rowend):
  tot = 0
  for i in range (rowstart, rowend+1):
    tot += self [col + str (i)]
  return tot
