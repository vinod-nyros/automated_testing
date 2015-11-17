### #!/usr/local/bin/python

import mymodules
import os, cPickle, urllib, sys, stat, time, tags, updater, ccards, sendorder2

ordersdir = '/usr/local/www/securepages/orders/'

reload (mymodules)  
reload (tags)  
reload (updater)
reload (ccards) 
reload (sendorder2)

### orders

def orders (self):
  #ses = self.session
  req = self.REQUEST
  
  if hasattr (req, 'order'):
    if hasattr (req, 'emailtemplate'):
      if hasattr (req, 'sendemail'):
        return sendEmail (self)

      return showEmail (self)

    return showOrder (self, req ['order'])

  return listOrders (self)


### sendEmail

def sendEmail (self):
  req  = self.REQUEST
  order = req ['order']
  emailtemplate = req ['emailtemplate']

  if hasattr (req, 'emailbody'):
    emailbody = req.emailbody
  elif hasattr (self, 'emailbody'):
    emailbody = self.emailbody
  else:
    emailbody = self.emails [emailtemplate] (self)

  return sendorder2.asyncsendorder (self.email, 'orders@eracks.com', emailbody)


### showEmail

def showEmail (self):
  req   = self.REQUEST
  order = req ['order']
  emailtemplate = req ['emailtemplate']

  f     = open (os.path.join (ordersdir, order))
  pkl   = cPickle.load (f)
  f.close()

  checkout = pkl ['checkout']

  for item in checkout.items():         # propagate contents of checkout onto me so dtml can find
    k,v = item
    setattr (self, k, v)

  self.ordnum    = os.path.splitext (order) [0]
#  self.shipper  = eval (self.shipmeth) [0]
  self.tracknum  = req.tracknum
  self.shipper   = self.shippers [req.shipper].title_or_id()
  self.trackurl  = self.shippers [req.shipper] (self)
  self.cctype    = ccards.vendor (self.ccnum)
  self.ccend     = self.ccnum [-4:]
#  self.emailtemplate = emailtemplate  should stay in request
  self.editing   = hasattr (req, 'editemail')
  self.saving    = hasattr (req, 'saveemail')
  
  if hasattr (req, 'emailbody'):
    self.emailbody = req.emailbody
  else:
    self.emailbody = self.emails [emailtemplate] (self)
  
#  return '%s<pre>%s</pre>' % (self.showemailactions (self), self.emails [emailtemplate] (self))  # calling renders content
  return self.showemail (self)  # calling renders content



### showOrder

def showOrder (self, order):
  f    = open (os.path.join (ordersdir, order))
  pkl  = cPickle.load (f)
  f.close()

  #env = pkl ['request.environ']
  #form = pkl ['request.form']
  #prod = pkl ['prod']
  checkout = pkl ['checkout']
  
  cart = pkl ['cart']
  result = tags.bold ('Order Number %s<br>' % os.path.splitext (order) [0])

  self.order = order  # put the order with the ".pkl" ext there..
  result = result + self.listemails (self)
 
  for item in checkout.items():
    k,v = item
    if v != '' and k [-4:] != 'info':
      result = result + '%s: %s<br>' % item

  cartitems = cart.items()
  cartitems.reverse()

  for num, item in cartitems:

    sku       = item ['sku']
    summary   = item ['summary']
    qty       = item ['qty']
    baseprice = item ['baseprice']
    asconfig  = item ['totprice']
    totprice  = asconfig * qty
    
    if hasattr (item, 'notes'): notes = item ['notes']
    else: notes = ''

    result = result + '<br>Line %s: %s<br>'        % (num, sku) + \
                      'Summary : %s<br>'           % summary    + \
                      'Quantity : %s<br>'          % qty        + \
                      'Base Price : $%5.2f<br>'    % baseprice  + \
                      'As Configured : $%5.2f<br>' % asconfig   + \
                      'Total Price : $%5.2f<br>'   % totprice   + \
                      'Notes : %s<br>'             % notes      + \
                      dumpOpts (item ['opts'])

  return result


### listOrders

def listOrders (self):
  files = os.listdir (ordersdir)
  result = ''

  files.sort()

  for file in files:
    ord, ext = os.path.splitext (file)
    fullname = os.path.join (ordersdir, file)

    #if os.path.splitext (file) [1] == '.pkl':

    if ext == '.pkl':
      #mtime = os.stat (fullname) [ST_MTIME]
      mtime = os.path.getmtime (fullname)
      txt = 'Order #%s placed %s' % (ord, time.ctime (mtime))
      result = result + tags.link ('?order=' + file, txt) + \
                        tags.link ('ordersdir/%s.html' % ord, '(html with total)') + '<br>'
  return result


### dumpOpts

def dumpOpts (opts):
  result = ''

  for opt in opts.values():
    choices = opt ['choices']
    default = opt ['defaultchoiceid']
    selected = opt ['selectedchoiceid']
    Option = opt ['Option']
    choice = choices [selected] 
    Choice = choice ['Choices']
    price  = choice ['pricedelta']

    if Choice != 'none':
      result = result + '%s: %s %s<br>' % (Option, Choice, price)

  return result


# - - - - - methods used to extract rioux session - - - - - 

### rioux

def rioux():
  f    = open ('/usr/local/www/securepages/orders/rioux.pkl')
  pkl  = cPickle.load (f)
  f.close()

  return pkl


### isdict

def isdict (d):
  return type (d) == type ({})


# - - - - - methods used for docs - return pydict/list/seq, mark up w/dtml/tal

def proddict (self):
  ses = self.session
  prod = {}
  if ses.has_key ('prod'):  # no get - not quite like a dictionary
    prod = ses ['prod']
  return prod

def prodpairs (self):
  return proddict (self).items()

  prod = {0: 'zero', '1':'one', '2':'two'}
  #return ('sdfg','sdfg','sdfg','eryt')
  return prod.items()

def comparesortorders (o1, o2):
  return int (o1 ['sortorder']) - int (o2 ['sortorder'])

def optpairs (self, prod):
  #return prod.items()
  opts = prod ['opts']

  result = []

  optlist = opts.values()
  optlist.sort (comparesortorders)

  for opt in optlist: # opts.values():
    choices = opt ['choices']
    default = opt ['defaultchoiceid']
    selected = opt ['selectedchoiceid']
    Option = opt ['Option']
    choice = choices [selected] 
    Choice = choice ['Choices']
    price  = choice ['pricedelta']

    result.append ((Option, Choice))

  return result


### main (for testing and development)

if __name__ == "__main__":
  def dumppkl():
    f    = open ('7198.pkl')
    pkl  = cPickle.load (f)
    f.close()

    for k in pkl.keys():
      v = pkl [k]
      print k, ':', 
      if type (v) is type ({}):  #DictType:
        print ''
        for kk in v.keys():
          vv = v [kk]
          print ' ', kk, ':', 
          if type (vv) is type ({}): 
            print ''
            for kkk in vv.keys():
              vvv = vv [kkk]
              print '   ', kkk, ':', `vvv`
          else:   
            print `vv`
      else:
        print `v`

  #dumppkl()
  #sys.exit()

  zopedir = '/usr/local/Zope-2.2.5/Extensions'

  def atswisa (cmd):
    cmd = replace (cmd, '"', '\\"')
    cmd = 'c:/pscp/plink.exe -ssh -pw semaj joe@216.39.99.117 ' + cmd
    #print cmd
    os.system (cmd)

  def getswisa (filenames):  
    os.system ('c:/pscp/pscp.exe -pw semaj joe@216.39.99.117:%s .' % filenames)
  
  def putswisa (filenames):  
    #os.system ('c:/pscp/pscp.exe -pw semaj %s joe@216.39.99.117:%s' % (filenames, zopedir))
    os.system ('c:/pscp/pscp.exe -pw 2BorNot2 %s root@216.39.99.117:%s' % (filenames, zopedir))

  #putswisa ('checkout9.py')
  #putswisa ('renderer.py')
  #getswisa ('updater.py')
  #putswisa ('updater.py')
  putswisa ('admin.py')
  #putswisa ('sendorder2.py')
 
  print 'File(s) put'

  import urllib
  #u = urllib.urlopen ('http://joe:semaj@www.eracks.com/admin/orders/manage_edit?title=&function=orders&module=admin')
  u = urllib.urlopen ('http://joe:semaj@www.eracks.com/compile')
  print u.read()
  u.close()


### old & test stuff

"""
def dummy():
  import traceback

  def stk (self):
    return str (traceback.format_stack()) # + '\n' + str (traceback.format_tb())


fullOpts (prod ['opts'])

for item in cart.values():
  print item ['sku'], ':'
  fullOpts (item ['opts'])

#opts = prod ['opts']

#for opt in opts.items():
#  print `opt`

  #for choice in choices.items():
  #  print `choice`

#('choices', {1023: {'Choices': '17" Monitor', 'choiceid': 1023, 'pricedelta': 280.0}, 30: {'Choices': 'none', 'choiceid': 30, 'pricedelta': 0.0}, 32: {'Choices': '15" Monitor', 'choiceid': 32, 'pricedelta': 200.0}, 1025: {'Choices': '19" Optiquest Q95 .23 Monitor', 'choiceid': 1025, 'pricedelta': 480.0}, 1024: {'Choices': '17" Optiquest Q71 .27 Monitor', 'choiceid': 1024, 'pricedelta': 320.0}})
#('defaultchoiceid', 30)
#('Option', 'Monitor')
#('selectedchoiceid', 30)
#('optid', 11)

sys.exit()

for k in pkl.keys():
  v = pkl [k]
  print k, ':', 
  if type (v) is type ({}):  #DictType:
    print ''
    for kk in v.keys():
      vv = v [kk]
      print ' ', kk, ':', 
      if type (vv) is type ({}): 
        print ''
        for kkk in vv.keys():
          vvv = vv [kkk]
          print '   ', kkk, ':', `vvv`
      else:   
        print `vv`
  else:
    print `v`

#print `pkl`


cart = pkl ['cart'] 

item1 = cart [1]

#  self.mto ='Blah!'
#  result = result + tags.link (seslink (self.emails.test (self), 'test email') renders email content into link (!)
#  result = result + updater.standardlink (self, self.emails.test.id(), 'test email')  works, leaves out folder
#  result = result + updater.standardlink (self, self.emails.test.getPhysicalPath(), 'test email')


  #for email in self.emails.objectValues():
    #href = '?order=%s&email=%s' % (order, email.id())
    #text = 'Send email: ' + email.title_or_id()
    #updater.seslink (self, href, text)  
    #result = result + tags.input (email.title_or_id(), type='radio')

#  for optx in opts.keys():
#    opt = opts [optx]

#  result = result + tags.select (tags.option (self.emails.objectValues(), selected=email), name='email')  

#  emails = []
#  for k,v in self.emails.objectItems():
#    emails.append (k, v.title_or_id())

#  result = result + '<br><b>Show Prepared Email:</b><br>Shipper:%s<br>Tracking number:%s<br>Template:%s%s<br>' % \
#           (tags.input ('shipper'), \
#            tags.input ('tracknum'), \
#            tags.select (tags.option (emails, selected=k), name='email'), \
#            tags.input (type='submit') )


"""
