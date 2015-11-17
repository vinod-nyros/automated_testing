#__debug__ = 1

import mymodules  # must be first, sets paths

import myutil, tags, catax, statecodes, countrycodes, ccards, renderer, sendorder
from myutil import *
from tags import *
#from statecodes import statelist
#from countrycodes import countrylist2
#from catax import calist

from string import *
import os, cPickle, DateTime

#raise Exception ('dir (catax): ' + `dir (catax)`)
#raise Exception ('dir (countrycodes): ' + `dir (countrycodes)`)

### fns which should be in the dict object to start with

def has_value (dct, itm):
  for o in dct.values():
    if o == itm:
      return o

def indexof (dct, itm):
  vals = dct.values()
  for i in range (len (vals)):
    if vals[i] == itm:
      return i

def keyof (dct, itm):
  items = dct.items()
  for i in range (len (items)):
    if items [i] [1] == itm:
      return items [i] [0]

def nameof (var):
  # return keyof (vars(), var)  returns 'var' (!)
  return keyof (globals(), var)


### misc lists used by field defs

ships =    ( ( "('Ground',1.0)", 'UPS Ground'),  # note about insured
             ( "('3day',1.8)",   '3-day (UPS or FedEx)'),
             ( "('2day',2.4)",   '2-day (UPS Blue or FedEx)'),
             ( "('1day',3.5)",   'Next Day (UPS Red or FedEx)'), 
             ( "('IntlEcon',3.0)",  'International Economy (5-7 days)'), 
             ( "('IntlExpr',4.5)",  'International Express (2-3 days)') )

ccmonths = \
         ( ( 1, 'Jan'), 
           ( 2, 'Feb'),
           ( 3, 'Mar'),
           ( 4, 'Apr'),
           ( 5, 'May'),
           ( 6, 'Jun'),
           ( 7, 'Jul'),
           ( 8, 'Aug'),
           ( 9, 'Sep'),
           ( 10, 'Oct'),
           ( 11, 'Nov'),
           ( 12, 'Dec') )

ccyears = \
         ( ( 2001, 2001),
           ( 2002, 2002), 
           ( 2003, 2003), 
           ( 2004, 2004), 
           ( 2005, 2005), 
           ( 2006, 2006), 
           ( 2007, 2007), 
           ( 2008, 2008), 
           ( 2009, 2009) )

### shorter names for defs tables below

states   = statecodes.statelist
#countries= mycodes.statelist2 
countries= countrycodes.countrylist
taxes    = catax.calist

### consts and field defs

boxcolor = '#c4c4ff'
blue     = '#efefff'
grey     = '#dedede'
#white    = '#ffffff'
#red      = '#ff0000'
pink     = '#880000'
#green    = '#00ff00'
#darkgreen= '#008800'

green    = 'green'
darkgreen= 'darkgreen'
red      = 'red'
white    = 'white'

### field definitions for forms - parsed at module load time - 1st line is for form itself
#
#                               d
#                               e
#                               f
#                               a   r
#                               u   e
#                               l   q    addl 
# class  | fld name |  parent | t | d |  data | field/form label | instr (instructions)           | paren/link
#                                                                                              
orgdefs='''\
form    | orginfo   |         |   |   |       | Original Info    | Complete Your Original Info:   |  for form: dbtable? what else? buttons? 
#                                             
email   | email     |         |   | 1 |       | Your Email       | Enter your email address, here |  
pw      | password  |         |   |   |       | Your Password    | Enter your password, here      | 
button  | login     |         |   |   |       | Login            | Login and retrieve account info| 
confpw  | password2 |         |   |   |       | Confirm Password | Confirm your password, here    | 
phone   | phone     |         |   |   |       | Your Phone       | Enter your primary phone number| 
phone   | phone2    |         |   |   |       | Alt Phone        | Alternate phone (cell, pager)  | 
text    | name      |         |   | 1 |       | Your Name        | Enter your name, here          | 
choice  | shipstate |         |   | 1 | states| State            | Enter state, province, or region|
rgroup  | paymeth   |         |   |   |       | Payment Method   | Choose your payment method     |
 radio   | byccard  | paymeth | 1 | 1 |       | Credit Card      | Number %s Expiry %s %s Visa/MC/Amex/Discover <img height=20 src="images/ccards4.gif"> | 
 radio   | bypo     | paymeth |   |   |       | Purchase Order   | Company purchase order (PO) requires PO number, above |
 radio   | bycheck  | paymeth |   |   |       | Check            | Pay by company check (will delay shipping)        | 
 radio   | bywire   | paymeth |   |   |       | Wire Transfer    | Pay by wire transfer (will require instructions)  | 
  ccard  | ccnum    | byccard |   |   |       | Number           | <img src="images/ccards4.gif"> |                
  choice | ccmonth  | byccard |   |   | ccmonths | Expiry Month  | Expiration date month          |                
  choice | ccyear   | byccard |   |   | ccyears  | Expiry Month  | Expiration date year           |                
checkbox | cbox     |         |   |   |      | Different Billing | Check to enter a separate billing address |     
inbutton | updorg   |         |   |   |      | Update this section | Click to update this section |                
outbutton| editorg  |         |   |   |      | Edit this section | Click to edit this section     | 
#checkbox| cbox2    |         |   |   |      | Different Billing | Check to enter a separate billing address |     
'''

shipdefs='''\
form    | shipinfo  |         |   |   |       | Shipping Info   | Enter your shipping address:          |
text    | shipname  |         |   | 1 |       | Full Name       | Person's full name to ship to         |
text    | shiporg   |         |   |   |       | Organization    | Organization, blank if none           |
email   | email     |         |   | 1 |       | eMail address   | Complete eMail address (name@domain.com) |  
phone   | shipphone |         |   |   |       | Phone number    | Phone number with area code           |  required for expedited shipping
text    | shipaddr1 |         |   | 1 |       | Address 1       | Shipping address (number, street)     |
text    | shipaddr2 |         |   |   |       | Address 2       | Suite, dept, mail drop, or add'l info |
text    | shipcity  |         |   | 1 |       | City            | City name                             |
zip     | shipzip   |         |   | 1 |       | Zip Code        | Zip or Postal Code              | 
rgroup  | shiptype  |         |   | 1 |       | Shipping Type   | Choose your shipping type       | 
 radio  | shipus    | shiptype| 1 |   |       | US              | <b>State:</b> %s                | 
  shstch| shipstate | shipus  |   |   | states| State           | State                           |
 radio  | shipintl  | shiptype|   |   |       | Int'l           | <b>Country:</b> %s<br>Province/Region: %s | 
  shcnch|shipcountry|shipintl|   |  |countries| Country        | Country for International shipments    |
  text  | shipregn  | shipintl|   |   |       | Region          | Province or Region              |  
# zip   | shippost  | shipintl|   | 1 |       | Postal Code     | Postal Code                     | 
checkbox| billsame  |         | 1 |   |       | Billing is same | My billing / credit card information is the same as my shipping information |
#inbutton| updship  |         |   |   |       | Update this section | Click to update this section      |                
#outbutton| editship |         |   |   |       | Edit this section   | Click to edit this section        | 
'''

billdefs='''\
form    | billinfo  |         | 1 |   |       | Billing Info    | Enter your credit card / billing address, if different than above: |
#onchkbox | billsame |         | 1 |   |       | Same            | My billing address is the same as my shipping address |     
breqtxt | billname  |         |   |   |       | Full Name       | Person's full name to bill to         |
text    | billorg   |         |   |   |       | Organization    | Organization, blank if none           |
breqtxt | billaddr1 |         |   |   |       | Address 1       | billing address (number, street)      |
text    | billaddr2 |         |   |   |       | Address 2       | Suite, dept, mail drop, or add'l info |
breqtxt | billcity  |         |   |   |       | City            | City name                             |
breqzip | billzip   |         |   |   |       | Zip Code        | Zip or postal code                    | 
rgroup  | billtype  |         |   | 1 |       | Billing Type    | Choose your billing type        |
 radio  | billus    | billtype| 1 |   |       | US              | <b>State:</b> %s                |
  bistch| billstate | billus  |   |   | states| State           | State                           |
 radio  | billintl  | billtype|   |   |       | Int'l           | <b>Country:</b>%s<br>Province/Region: %s |
  bicnch|billcountry|billintl|   |  |countries| Country        | Country for International billing |
  text  | billregn  | billintl|   |   |       | Region          | Province or Region              |
#inbutton | updbill  |         |   |   |       | Update this section | Click to update this section      |                
#outbutton| editbill |         |   |   |       | Edit this section   | Click to edit this section        | 
'''

orderdefs='''\
form     | ordinfo  |         |   |   |       | Order Info       | Complete your order info:                  |
ordlabel | ordtotal |         |   |   |       | Total            | Your order is for %s, US$%8.2f total, before tax & shipping | 
text     | refnum   |         |   |   |       | Reference number | Purchase order (PO) or reference number    |
ship     | shipmeth |         |   | 1 | ships | Shipping method  | Standard/expedited/international shipping | Notes
tax      | tax      |         |   |   | taxes | Sales tax (CA only) | California shipping recipients choose your county | 
textarea | instr    |         |   |   |       | Special Instructions| Any special notes or instructions regarding your order | 
#inbutton| updord   |         |   |   |       | Update this section | Click to update this section      |                
#outbutton| editord  |         |   |   |       | Edit this section   | Click to edit this section        | 
'''

paydefs = '''\
form     | payinfo  |         |   |   |       | Payment Info     | Complete your payment info:    |
rgroup   | paymeth  |         |   |   |       | Payment Method   | Choose your payment method     |
 radio   | byccard  | paymeth | 1 |   |       | Credit Card      | Number %s Expiry %s %s Visa/MC/Amex/Discover <img height=20 src="images/ccards4.gif"> | 
 radio   | bypo     | paymeth |   |   |       | Purchase Order   | Company purchase order (PO) requires PO number, above | requires credit approval
 radio   | bycheck  | paymeth |   |   |       | Check            | Pay by company check (will delay shipping)        | 
 radio   | bywire   | paymeth |   |   |       | Wire Transfer    | Pay by wire transfer (will require instructions)  | 
  ccard  | ccnum    | byccard |   |   |       | Number           | <img src="images/ccards4.gif"> |                
  inchoice| ccmonth | byccard |   |   | ccmonths | Expiry Month  | Expiration date month          |                
  inchoice| ccyear  | byccard |   |   | ccyears  | Expiry Month  | Expiration date year           |                
#inbutton| updpay   |         |   |   |       | Update this section | Click to update this section      |                
#outbutton| editpay  |         |   |   |       | Edit this section   | Click to edit this section        | 
'''

persdefs='''\
form    | persinfo  |         |   |   |       | Personal Info    | Enter your personal info:             | only email is required
text    | name      |         |   |   |       | Your Name        | Your full name (first, middle, last)  | if different than shipto
email   | email     |         |   | 1 |       | Your eMail       | Your complete eMail address (name@domain.com) |  
#pw      | password  |         |   |   |       | Your Password    | Password for new or existing accounts | optional
#inbutton | login    |         |   |   |       | Login            | Login and retrieve account info       | 
#confpw  | password2 |         |   |   |       | Confirm Password | Confirm your new password, here       | 
phone   | phone     |         |   |   |       | Your Phone       | Your primary phone number             | 
phone   | phone2    |         |   |   |       | Alt Phone        | Alternate phone (cell, pager, etc)    | 
#inbutton| updpers  |         |   |   |       | Update this section | Click to update this section       |                
outbutton| editpers |         |   |   |       | Edit this section   | Click to edit this section         | 
'''

### read field defs (above) and return field list of tuples

def fieldlist (defs):
  lines = split (defs, '\n')
  
  tbl = []

  for line in lines:
    #if len (line) > 0 and line [:1] != '#':
    if line and line [:1] != '#':
      items = split (line, '|')

      lst = []

      for i in items:
        lst.append (strip (i))

      tbl.append (lst)

  return tbl


### initialize / parse fields into lists

orglist  = fieldlist (orgdefs)
shiplist = fieldlist (shipdefs)
billlist = fieldlist (billdefs)
paylist  = fieldlist (paydefs)
ordlist  = fieldlist (orderdefs)

### reload dependent modules if I reload - forces reload in Zope

reload (mymodules)  
reload (ccards)  
reload (statecodes)  
reload (countrycodes)  
reload (myutil)  
reload (tags)  
reload (catax) 
reload (renderer)
# reload (updater)  this should go into mymodules..
reload (sendorder)

### exports to zope

def shipinfo (self): return form (shiplist).handler (self)
def billinfo (self): return form (billlist).handler (self)
def payinfo  (self): return form (paylist).handler (self)
def ordinfo  (self): return form (ordlist).handler (self)

def pageinfo (self): return page().handler (self)

### my font tags & tag extensions - myutils? another layer?

#sansserif = 'Tahoma,Helvetica,sans-serif'
sansserif = 'Verdana,Helvetica,sans-serif'

def font1 (s):
  return font (s, size=1, face=sansserif)

def font2 (s):
  return font (s, size=2, face=sansserif)

def font3 (s):
  return font (s, size=3, face=sansserif)

def font4 (s):
  return font (s, size=4, face=sansserif)

def font5 (s):
  return font (s, size=5, face=sansserif)

def font6 (s):
  return font (s, size=6, face=sansserif)

def font7 (s):
  return font (s, size=7, face=sansserif)

def redfont1 (s):
  return font (s, size=1, face=sansserif, color=red)

def redfont2 (s):
  return font (s, size=2, face=sansserif, color=red)

def greenfont3 (s):
  return font (s, size=3, face=sansserif, color=darkgreen)

def greenfont4 (s):
  return font (s, size=4, face=sansserif, color=darkgreen)

def greenfont7 (s):
  return font (s, size=7, face=sansserif, color=darkgreen)


### field classes - contained by form class

class field:
  '''
  fields initialized by form reader:  
  name          internal name - appears in request, session
  dbname        database field name - often same as name
  dbtable       originating database table
  label         label for form (left column, typically)
  instr         instructions for filling in the field, notes, optional link
  default       initial value
  required      whether the field is required
  data          additional data (optional)
  
  class members:
  persistent    true ==> store the field's name/value in the session
  intheform     true ==> add this field to the form's list of fields to handle

  fields initialized in init:
  value         the value from the request or session
  error         the error message, if any
  frm           the owning form which manages this field
  parent        nestor
  kids          list of nestee's
  rendered      whether this field has been rendered already - used by form

  methods:
  get()         get value from request or session
  check()       do edits
  render/in/out renders the object to html - for input, or output
  '''

  persistent = 1
  intheform = 1

  def __init__ (self, frm):
    self.error = '' #None prints as 'None'
    self.value = '' #None
    self.frm = frm
    self.parent = None
    self.kids = []
    self.rendered = 0
    # other fields initialized by form reader

  def renderin (self): return 'renderin missing!' # pass
  #def renderout (self): return 'renderout missing!' # pass
  def check (self, req): pass

  def get (self, req, ses):
    if req and req.has_key (self.name):  # no - let this override the session # and req [name]:
      self.value = strip (req [self.name])
    elif ses and ses.has_key (self.name):
      self.value = ses [self.name]  # bombs on tuples caused by duplicate form field names - "read-only character buffer, list"
      req [self.name] = self.value  # put it in request so other editors can find it
    else:
      self.value = ''

  def renderout (self):
    return str (self.value)

  def render (self):
    self.rendered = 1

    if self.frm.ok:
      rfield = self.renderout()
    else:
      rfield = self.renderin()

    if not rfield:  # no rows for blank fields
      return ''

    left = font2 (self.label)
    middle = font2 (rfield)
    
    if self.frm.ok:      # render for output - no instructions column, not editable
      cells = td (left, middle)
      return self.frm.nextrow (cells) 
    elif self.required:
      left = bold (left)
    
    right = ''
    if self.instr:
      right = self.instr
        
    if self.link:
      right = right + link ("#%s" % self.name, '(%s)' % self.link)

    if right:
      cells = td (left, middle, font1 (right))
    else:
      cells = td (left) + td (middle, colspan=2)

    return self.frm.nextrow (cells) 


class inputf (field):
  def renderin (self):
    checked = iff (self.value or self.default, 'checked', '')

    if self.value:
      s = input (checked, name=self.name, type=self.inputtype, value=self.value)
    else:
      s = input (checked, name=self.name, type=self.inputtype)

    if self.error:
      return redfont1 (s + bold (self.error))
    else:
      return s

class text (field):
  def renderin (self):
    if self.value:
      s = input (name=self.name, value=self.value)  # default type is 'text', so don't use it
    else:
      s = input (name=self.name)

    if self.error:
      return redfont1 (s + bold (self.error))
    else:
      return s


class textarea (field):
  def renderin (self):
    s = font2 (tags.textarea (self.value, rows=2, cols=60, name=self.name))  # '<font face="arial,helvetica,sans-serif" size="2"><textarea rows="2" cols="60" name="notes"></textarea></font>'

    if self.error:
      return redfont1 (s + bold (self.error))
    else:
      return s
  
  def renderout (self):
    return replace (field.renderout (self), '\n', '<br>')


class number (text):
  def check (self, req):
    self.error = ''

    if upper (self.value) != lower (self.value): 
      self.error = 'Improperly formed number'  # should check for nonnum chars, too

    return self.error


class zip (text):
  def check (self, req):
    self.error = ''

    # only allow numbers for US shipments
    if req.shiptype == 'shipus' and upper (self.value) != lower (self.value):
      self.error = 'Improperly formed number'  # should check for nonnum chars, too

    return self.error


class label (field):
  def renderin (self): return self.renderout()


class ordlabel (label):
  def renderout (self): 
    (itms, tot) = renderer.cartcontents (self.frm.zope)
    itms = '%s item%s' % (itms, iff (itms==1, '', 's'))
    s = self.instr % (itms, tot)
    self.instr = ''  # so no 3rd column!
    return font4 (s)

    #return s % (greenfont3 (str (itms)), greenfont3 (str (tot)))


class email (text):
  def check (self, req):
    self.error = ''

    if find (self.value, '@') < 0 or find (self.value, '.') < 0:
      self.error = 'Improperly formed email address'

    return self.error


class ccard (text):
  def check (self, req):
    self.error = ''

    if req.paymeth != 'byccard':
      return ''

    self.value = ccards.numbersOnly (self.value)
    dt = DateTime.DateTime()

    if self.value:     
      if upper (self.value) != lower (self.value): 
        self.error = 'Improperly formed credit card number'  # should check for nonnum chars, too
      elif not ccards.validate (self.value):
        self.error = 'Invalid %s number' % ccards.vendor (self.value) 
      elif ccards.vendor (self.value) not in ('MasterCard', 'Visa', 'Amex', 'Discover'):
        self.error = 'We only accept Visa, MasterCard, Discover, and Amex'
      elif int (req.ccyear or '0') <= dt.year() and int (req.ccmonth or '0') < dt.month():
        #raise Exception (req.ccyear, req.ccmonth, dt.year(), dt.month(), dt)
        self.error = 'Expired card'

    return self.error

  def renderout (self):
    if self.value:
      return '%s card ending in %i' % (ccards.vendor (self.value), long (self.value) % 10000)
    else:
      return ''

  # now done w/rendered flag - def render (self): return ''  # since this has to be in the form, but is displayed by parent


class pw (inputf):
  inputtype='password'

  def check (self, req):
    self.error = ''

    if len (self.value) < 6:
      self.error = 'Password must be at least 6 characters long'
    return self.error

  def renderout (self):  return ''  # don't show at all! could use 'outputtype' or something... '********'


class confpw (pw):
  def check (self, req):
    self.error = ''

    if len (self.value) < 6:
      self.error =  'Confirm Password must be at least 6 characters long'
    elif req.has_key ('password') and req ['password'] != self.value:
      self.error = 'Confirm Password does not match your password'

    return self.error


class button (inputf):
  inputtype='submit'
  persistent = 0

  def renderin (self):
    self.value = self.label
    return inputf.renderin (self)

  def renderout (self): return self.renderin()


class inbutton (button):
  def renderin (self): return button.renderin (self)
  def renderout (self): return ''

  def action (self, req):      # check and turn on frm.ok if passes edits
    #assert not self.frm.ok,  'not self.frm.ok'
    
    if self.frm.check (req):
      self.frm.ok = 1


class outbutton (button):
  def renderin (self): return ''
  
  def renderout (self): 
    self.value = self.instr
    return inputf.renderin (self)

  def action (self, req):      # turn off ok and allow form to reappear in edit mode
    self.frm.ok = 0            # action is really an 'onFieldReceived' event
  

class phone (text):
  def check (self, req):
    self.error = ''
    if upper (self.value) != lower (self.value): 
      self.error = 'Improperly formed phone number'
    return self.error


class choice (field):
  def renderin (self):
    s = select (option (self.data, selected=self.value), name=self.name)  

    if self.error:
      return redfont1 (s + bold (self.error))
    else:
      return s


class inchoice (choice):
  def renderout (self): return ''

  #def get (self, req, ses):
  #  field.get (self, req, ses)
  #  raise Exception (self.name, self.value)

  #def renderin (self):
  #  s = select (option (self.data, selected=str (self.value)), name=self.name)  
  #  raise Exception (self.name, self.value, s)


class tax (choice):
  def check (self, req):
    self.error = ''
    if req.shipstate == 'CA' and not self.value:  # self.value == '': 
      self.error = 'CA shipments must choose CA county (sales tax rate)'
    return self.error

  def renderout (self): 
    if self.value:
      tax, county = eval (self.value)
      return '%s county, %s %%' % (county, float (tax))
    else:
      return ''


class ship (choice):    
  def renderout (self): 
    if self.value:
      return '%s, $%s' % eval (self.value)
    else:
      return ''

  def check (self, req):
    self.error = ''

    if req.shiptype != 'shipus' and not self.value [2:6] == 'Intl':
      self.error = 'International shipments must choose international shipping option'

    return self.error

  
class checkbox (inputf):
  inputtype='checkbox'
  
  def __init__ (self, frm):
    inputf.__init__ (self, frm)
    self.usedefault = 1

  def renderin (self):
    checked = iff (self.value or (self.usedefault and self.default), 'checked', '')

    if self.value:
      s = input (checked, name=self.name, type=self.inputtype, value=self.value)
    else:
      s = input (checked, name=self.name, type=self.inputtype)

    s = s + self.instr
    self.instr = ''
    return s
    
  def renderout (self):
    return input (name=self.name, type='hidden', value=self.value) + iff (self.value, 'yes', 'no')

  #def action (self, req):          # action is really an 'onFieldReceived' event, so not called when field not there
  #  if self.frm.fromuser and not req.has_key (self.name):
  #    self.value = 0

  #def onFormReceived (self, req):   # fix how the checkbox loses state due to not appearing in req
  #  if self.frm.fromuser and not req.has_key (self.name):
  #    self.value = 0   

  def get (self, req, ses):
    if self.frm.fromuser and not req.has_key (self.name):  # checkbox is not returned in form results if unchecked!
      req [self.name] = '' #0                              # so put it in
      self.value = '' #0                                   # and set it manually (not really necessary, the parent get() will do that anyway)

    if ses.has_key (self.name):                            # if it's in the session, then it's not new, so don't use the default
      self.usedefault = 0

    return field.get (self, req, ses)
  

class onchkbox (checkbox):
  def renderout (self):
    return self.renderin()


class outchkbox (checkbox):
  def renderin (self): return ''
  
  def renderout (self):
    return checkbox.renderin (self)


class radio (inputf):
  intheform = 0
  inputtype='radio'
  
  def renderin (self):
    checked = iff (self.checked, 'checked', '')    # self.checked is set by rgroup

    if self.value:
      s = input (checked, name=self.name, type=self.inputtype, value=self.value)
    else:
      s = input (checked, name=self.name, type=self.inputtype)

    self.label = s + self.label

    if self.kids:
      lst = []

      for f in self.kids:
        f.rendered = 1
        lst.append (f.renderin())    # fill 2nd column with nested field(s), if there

      s = self.instr % tuple(lst)
    else:
       s = self.instr                 # fill 2nd column with usual description

    self.instr = ''
    return s

  def renderout (self): 
    if self.data:
      return self.data.renderout()  
    else:
      return ''


class rgroup (field):
  def render (self):
    self.rendered = 1

    if self.frm.ok:
      return self.renderout()

    s = ''
    for f in self.kids:
      f.value = f.name
      f.name = self.name
      #f.checked = iff (self.frm.fromuser, self.value == f.value, f.default)
      f.checked = iff (self.value, self.value == f.value, f.default)
      f.frm = self.frm		# so it can find nextrow(), ok, etc
      s = s + f.render()
    
    return s

  def renderout (self):
    for f in self.kids:
      if f.name == self.value:
        self.value = f.label
            
    return field.renderout (self)


class shstch (choice):  # shipto state choice edits
  def check (self, req):
    self.error = ''
    if req.shiptype == 'shipus' and not req.shipstate:
      self.error = 'US shipments must choose state'
    return self.error


class shcnch (choice):  # shipto country choice edits
  def get (self, req, ses):
    if req.has_key ('shiptype') and req.shiptype != 'shipus':
      req.shipstate='sdetrgsdgwetg'
      #raise Exception (req.shipstate) 
      #ses.shipstate=''
    return choice.get (self, req, ses)

  def check (self, req):
    self.error = ''
    if req.shiptype != 'shipus':
      if not req.shipcountry: 
        self.error = 'International shipments must choose country'
    return self.error


class bistch (choice):  # billto state choice edits
  def check (self, req):
    self.error = ''
    if not req.billsame and req.billtype == 'billus' and not req.billstate:
      self.error = 'US billing must choose state'
    return self.error


class bicnch (choice):  # billto country choice edits
  def check (self, req):
    self.error = ''
    if not req.billsame and req.billtype != 'billus':
      req.billstate=''
      #self.session.billstate=''
      if not req.billcountry:
        self.error = 'International billing must choose country'
    return self.error


class breqtxt (text):
  def get (self, req, ses):
    if req.has_key ('billsame'):
      self.required = not req.billsame
    return text.get (self, req, ses)


class breqzip (zip):
  def get (self, req, ses):
    if req.has_key ('billsame'):
      self.required = not req.billsame
    return zip.get (self, req, ses)

 

### fields (plural) class, here? to read in and maintain stuff? UserList or UserDict?


### form class - container for fields, renders, checks, handler, etc.

class form:
  ''' 
  fields        list of fields - used for managing fields
  fielddict     dict of fields - used for looking up parents/kids, later retrieval
  name          internal name - 
  error         string of first error encountered
  ok            flag saying that the form has passed edits - stored in session as formname=1
  init          reads in fields, sets up list
  get()         gets fields from request or session
  check()       check edits of fields
  saveit()      save to session
  nextrow()     alternates blue/white - called by field to render the row
  render()      render to html, each field at a time
  actions()     calls field.action, if any - generally used for buttons
  handler()     external interface, called from zope page, manages state
  '''

  def __init__ (self, flist):  # this isn't multitask/thread safe, here - OK, now its ok JJW
    self.fields = []  
    self.error = ''
    self.ok = 0         
    self.debug = ''

    self.fielddict = {}  # can't use __dict__, it collides with the normal self.member mechanism - unless you ensure no collisions!
    
    for (clas, nam, parent, default, required, data, label, instr, link) in flist:
      if clas == self.__class__.__name__:      # could use 'factory' class here, too
        f = self
      else:
        f = globals() [clas] (self)  # classes [clas] ()

        if f.intheform:
          self.fields.append (f)     # this is how the form handles the fields

        self.fielddict [nam] = f      # this is how the parents are located, and how form.field is used, later

        if parent: 
          f.parent = self.fielddict [parent]
          f.parent.kids.append (f)

      f.default  = default
      f.required = required
      f.frm      = self   # this is used for the field to find the form's state to render properly, like ok and nextrow
      f.name     = nam
      f.dbname   = nam
      f.label    = label
      f.instr    = instr
      f.link     = link
      if data and globals().has_key (data): 
        f.data   = globals() [data]

  def bug (self, *args):
    for a in args:
      self.debug = self.debug + '%s: %s<br>' % (hq (repr (a)), str (a))   # could use file & line number, here, optionally trace to file
  

  def get (self, req, ses):    # check source of data - 4 places to get values: none (new form), db (retrieve), session (redisplay), req (form submit)  
    self.ok = ses.has_key (self.name) and ses [self.name]
    self.fromuser = req.has_key (self.name) # and req [self.name] # could also do from=0 db=1 user=2 session=3 etc

    for f in self.fields:      
      f.get (req, ses)

    return self.fromuser


  def check (self, req):
    self.error = ''

    for f in self.fields:
      #if f.fromuser:
      if f.required and not f.value:   # this should be in f.check()
        f.error = '%s is required' % f.label
      else:
        f.check (req)

      self.error = self.error or f.error        # keep 1st one

    #self.bug (self.error)

    return not self.error                       # no error ==> ok


  def saveit (self, ses):                       # save is a reserved word
    for f in self.fields:
      if f.persistent:
        ses [f.name] = f.value   


  def nextrow (self, cells):
    #self.clr = iff (self.clr==blue, white, blue)
    return tr (cells, bgcolor=self.clr) + '\n'

  
  def render (self):
    self.clr = white

    if self.error: 
    #  self.clr = blue   # start on white cell if error
      content = self.nextrow (td (redfont2 (bold (self.error)), colspan=3))
    else:
    #  self.clr = white    # for nextrow - start on blue cell
      content = ''        # could put table header here

    for f in self.fields:  
      if not f.rendered:
        content = content + f.render()

    if self.ok:
      top = font3 (self.label)
    else:
      top = font3 (self.instr) + iff (self.link, font2 (link ('#%s' % self.name, '(%s)' % self.link)), '') 
  
    top = td (top, align='center') # , colspan=3)
    top = tr (top, align='left', bgcolor=blue) + input (type='hidden', name=self.name, value=self.ok)
             
    return table (top + tr (td (table (content, cellpadding=1, cellspacing=0, border=0))), cellpadding=1, cellspacing=0, border=0, width='100%')


  def actions (self, req):  #, action):
    for f in self.fields:      
      #if hasattr (f, action):
      #  f [action] (req)
      if req.has_key (f.name) and hasattr (f, 'action'):
        #self.bug ('%s' % f.name)
        f.action (req)   # action is really 'onFieldReceived'
      

  def handler (self, zope):
    req = zope.REQUEST
    ses = zope.session
    chk = {}
    if ses.has_key ('checkout'): chk = ses ['checkout']
    self.zope = zope
    
    #if chk.has_key [self.name]:
    #  (self.ok, self.fromuser) = chk [self.name]

    #self.bug (self.default, self.fromuser)

    if self.get (req, chk): 
      #self.req = req       # gotta put this in there, now, so inbutton.action() can see it. no - pass it.
      self.actions (req)    # inbutton calls check
    elif self.default:      # 'default' for forms means default to rolled-up
      self.ok = 1

    if self.ok:
      self.saveit (chk)

    chk [self.name] = self.ok
    ses ['checkout'] = chk
    #self.debug = self.debug + `chk`
    return self.render() + self.debug


### misc tags used by page class

def tdf (*args, **kw):
  s = ''
  for arg in args:
    s = s + apply (td, [font2 (arg)], kw)
  return s

def thf (*args, **kw):
  s = ''
  for arg in args:
    s = s + apply (th, [font2 (arg)], kw)
  return s

def trtdf (*args, **kw):
  s = ''
  for arg in args:
    s = s + apply (tr, [apply (tdf, [arg], kw)], kw)
  return s
  
def trthf (*args, **kw):
  s = ''
  for arg in args:
    s = s + apply (tr, [apply (thf, [arg], kw)], kw)
  return s


### page class - handles all the forms at once

class page:
  def invoicegrid (self, cart, ordfrm):   # all the '...grid' funcs also render a text version for email - should be more O-O!
    grid = tr (thf ('Line', 'Qty', 'Model', 'Description', 'Price', 'Total'), bgcolor="#efefff")
    text = '\n'

    if cart:
      lines = cart.keys()
      lines.reverse()
      tot = num = lbs = 0

      for line in lines:
        prod  = Dict (cart [line])
        sku   = prod.sku
        model = prod.Product
        desc  = prod.summary
        qty   = prod.qty
        price = prod.totprice
	weight= prod.weight
        ext   = price * qty

        grid = grid + tr (tdf (line, qty, model, desc) + tdf ('$%5.2f' % price, '$%5.2f' % ext, align='right'))
        text = text + 'Line: %s\nQty: %s\nModel: %s\nDescription: %s\nPrice: %s each\nTotal price: %s\n\n' % (line, qty, model, desc, price, ext)

        tot = tot + ext
        num = num + qty
        lbs = lbs + weight * qty
    else:
      grid = grid + tr (tdf ('Your cart is empty', align='center'))
      return table (grid, border=0, cellspacing=0, width='100%')
      #raise Exception ('Empty cart')

    ### add tax, shipping, total

    ord = Dict (ordfrm.fielddict)

    tax, county    = eval (ord.tax.value or '[0, ""]')
    meth, shipping = eval (ord.shipmeth.value) 
    #shipping = shipping * num
    shipping = max (5, lbs * shipping) 
    taxdollars = tot * (float (tax) / 100)

    grandtot = tot + taxdollars + shipping

    shiplabel= 'Shipping (%s)' % meth
    totlabel = 'Grand Total'

    if tax:
      taxlabel = 'Sales Tax %5.2f%% (CA %s County)' % (tax, county)
      grid = grid + tr (tdf (taxlabel,  colspan=5, align='right') + tdf ('$%5.2f' % taxdollars, align='right'))
      text = text + '%s: %5.2f%%\n' % (taxlabel, tax)

    grid = grid + tr (tdf (shiplabel, colspan=5, align='right') + tdf ('$%5.2f' % shipping, align='right'))
    grid = grid + tr (thf (totlabel,  colspan=5, align='right') + thf ('$%8.2f' % grandtot, align='right'))
    text = text + '%s: $%5.2f\n' % (shiplabel, shipping)
    text = text + '%s: $%8.2f\n' % (totlabel, grandtot)

    self.ordertext = self.ordertext + text
    return table (grid, border=0, cellspacing=0, width='100%')


  def ordgrid (self, ordfrm, payfrm, orderno):  # PO, ord date, orderno (step 3 only), email, paymeth, special instr - future: cust no, invoice no, etc
    ord = Dict (ordfrm.fielddict)
    pay = Dict (payfrm.fielddict)
    
    if pay.paymeth.value == 'byccard':
      meth = pay.ccnum.renderout()
    else:
      meth = pay.paymeth.renderout()

    pairs = [('Reference/PO number', ord.refnum.value), 
             ('Order Date', now()), 
             ('Payment method', meth), 
             ('Special instructions', ord.instr.value)]

    if orderno:
      pairs.insert (0, ('Order number', orderno))

    header = []
    cells = []
    text = '\n'

    for name, value in pairs:
      #if name == 'Special instructions': value = replace (value, '\n', '<br>')
      header.append (name)
      cells.append (value)
      text = text + '%s: %s\n' % (name, value)

    kw = { 'align' : 'center' }

    grid = tr (apply (thf, header, kw), bgcolor="#efefff") + tr (apply (tdf, cells, kw))
    self.ordertext = self.ordertext + text
    return table (grid, border=0, cellpadding=3, cellspacing=0, width='100%')


  def shipgrid (self, shipform):
    ship = Dict (shipform.fielddict)  # magic
    name = ship.shipname.value
    org  = ship.shiporg.value
    email= ship.email.value
    phone= ship.shipphone.value
    addr = ship.shipaddr1.value + ' ' + ship.shipaddr2.value
    cs   = ship.shipcity.value + ', ' + ship.shipstate.value or ship.shipregn.value
    zc   = ship.shipzip.value + ' ' + ship.shipcountry.value or 'US'

    self.ordertext = self.ordertext + '\nShip To: %s\n%s\n%s\n%s\n%s\n%s\n%s\n' % (name, org, email, addr, cs, zc, phone)

    return table (trthf ('Ship To:', bgcolor="#efefff") + \
                  trtdf (name, org, email, addr, cs, zc, phone), border=0, cellspacing=0, width='100%')


  def billgrid (self, shipform, billform):
    ship = Dict (shipform.fielddict)  # magic
    bill = Dict (billform.fielddict)  # magic
    if ship.billsame.value:
      name = ship.shipname.value
      org  = ship.shiporg.value
      addr = ship.shipaddr1.value + ' ' + ship.shipaddr2.value
      cs   = ship.shipcity.value + ', ' + ship.shipstate.value or ship.shipregn.value
      zc   = ship.shipzip.value + ' ' + ship.shipcountry.value or 'US'
    else:
      name = bill.billname.value
      org  = bill.billorg.value
      addr = bill.billaddr1.value + ' ' + bill.billaddr2.value
      cs   = bill.billcity.value + ', ' + bill.billstate.value or bill.billregn.value
      zc   = bill.billzip.value + ' ' + bill.billcountry.value or 'US'

    self.ordertext = self.ordertext + '\nBill To: %s\n%s\n%s\n%s\n%s\n' % (name, org, addr, cs, zc)

    return table (trthf ('Bill To:', bgcolor="#efefff") + \
                  trtdf (name, org, addr, cs, zc), border=0, cellspacing=0, width='100%')


  def saveorder (self, ses, cust, payfrm, orderno):
    zopeorders = os.path.join (mymodules.orderpath, str (orderno))
    txt = self.ordertext
    htm = self.orderhtml
    us  = 'orders@eracks.net'
    #us  = 'info@eracks.com'

    pay = Dict (payfrm.fielddict)
    
    ccard = ''     
    if pay.paymeth.value == 'byccard':
      ccard = 'ccard: %s %s/%s' % (pay.ccnum.value, pay.ccmonth.value, pay.ccyear.value)
    
    htm = html (body ('%s<br>%s' % (ccard, htm), bgcolor=white))

    f = open (zopeorders + '.html', 'w')
    f.write (htm) 
    f.close()

    f = open (zopeorders + '.pkl', 'wb')
    cPickle.dump (ses._v_data, f) 
    f.close()

    url = mymodules.orderhost + '/%s.html' % orderno

    sendorder.asyncsendorder (us, us, 'Order #%s received' % orderno, 
                'Order number is #%s:\n\n%s\n' % (orderno, url))

    # should call dtml email template, here...

    # calling these one right after the other almost certainly causes the log records to be intermixed in the log file...
    # if not other disastrous results, too..

    #body = 
    #zope.email = email
    #zope.orderno = orderno
    #zope.url = url
    #body = zope.emails.orderemail (zope)  

    sendorder.asyncsendorder (cust, us, 'Your order #%s' % orderno, 
                'Thank you for your order. Your order number is #%s.\n It is now being processed.\n%s' % (orderno, txt))


  def rendergrids (self, ship, bill, ord, pay, cart, orderno):
    self.ordertext = ''

    gship = self.shipgrid (ship)                 # order matters, as these generate self.ordertext !
    gbill = self.billgrid (ship, bill)
    gord  = self.ordgrid (ord, pay, orderno)
    ginv  = self.invoicegrid (cart, ord)

    self.orderhtml = table (tr (td (gship, gbill)) + \
                            tr (td (gord, colspan=2)) + \
                            tr (td (ginv, colspan=2)), border=1, cellpadding=0, cellspacing=5)
    return self.orderhtml


  def handler (self, zope):
    req = zope.REQUEST
    ses = zope.session
    chk = {}
    if ses.has_key ('checkout'): chk = ses ['checkout']
    cart = ses ['cart']
    
    ord  = form (ordlist)
    ship = form (shiplist)
    bill = form (billlist)
    pay  = form (paylist) 

    
    kids = (ord, ship, bill, pay)  # order is important!

    ok = 1

    for f in kids:
      f.zope = zope

      #if f.get (req, chk):
      #  f.actions (req, 1, 'onFormReceived')

      if f.get (req, chk):
        f.ok = f.check (req)

      #  if f.check (req):
      #    f.ok = 1
      #  else: pass
      #elif f.default:
      #  f.ok = 1         # here, interpret form.default to mean NO form, at first

      f.actions (req)    # really an 'onFieldReceived' event

      if f.ok:
        f.saveit (chk)
  
      chk [f.name] = f.ok

      if not f.ok:
        ok = 0


    # 3 states/steps:
    #  1:entering - not ok
    #  2:reviewing - ok
    #  3:done
   
    if ok: step = 2
    else: step = 1

    if ok and req.has_key ('enterinfo.x'):      # back up from 2 to 1
      step = 1
    elif ok and req.has_key ('revieworder.x'):  # go forward from 1 to 2
      step = 2
    elif ok and req.has_key ('placeorder.x'):   # go forward from 2 to 3, place order
      step = 3

    s = ''
    shipfields = Dict (ship.fielddict)
    billsame   = shipfields.billsame.value
    email      = shipfields.email.value

    if step == 1:    
      for f in kids:
        if f != bill or not billsame:   
          f.ok = 0   # always render for input on step 1
          s = s + trtdf (f.render() + f.debug)

      s = table (s, border=1, cellpadding=0, cellspacing=5)
  
      stp = zope.step1 (zope)  
      s = stp + s + stp + zope.checkout_faq (zope)

    elif step == 2:            # ship to, bill to, cartgrid, tax, shipping, total, paymeth
      s = self.rendergrids (ship, bill, ord, pay, cart, 0)

      stp = zope.step2 (zope)  
      s = stp + s + stp 

    elif step ==3:
      url = mymodules.securehost + '/checkout?session=%s' % ses.getName()
      orderno = zope.sql.getNextId()[0].nextval

      s = self.rendergrids (ship, bill, ord, pay, cart, orderno)

      zope.email = email
      zope.orderno = orderno
      zope.url = url
      stp = zope.step3 (zope)  

      self.saveorder (ses, email, pay, orderno)
      s = stp + s
      ses ['cart'] = {}  # empty cart, now

    ses ['checkout'] = chk
    return s



### main (for testing and development)

if __name__ == "__main__":

  ### generate stubs for info links

  def gen (flist):
    for (clas, nam, parent, default, required, data, label, instr, link) in flist:
      if link: print para ('blurb for "%s" goes here' % label, id=nam)

  def genall():
    gen (shiplist)
    gen (billlist)
    #gen (perslist)
    gen (paylist)
    gen (ordlist)

  #genall()

  #print select (option (ccmonths, selected=2), name='blah')  # works, w/int!
  #print select (option (ccmonths, selected='2'), name='blah')  # nope - OK fixed, now; normalize to strings in tags.option  
  #import sys
  #sys.exit()
 
  import urllib
  u = urllib.urlopen ('http://joe:semaj@eracks733:8080/eRacks/compile')
  print u.read()
  #if find (u.read(), 'compiled OK'):
  #  print 'OK'

  u.close()


  from UserDict import UserDict

  class Req (UserDict):
    form = {}

  slf = UserDict() # {}
  req = Req()
  req.data = {'name':'joe', 'email':'safasdf' }
  #req.__dict__ =  {'name':'joe', 'email':'safasdf', 'form' : {} }  # req.data
  
  #print `orglist`

  for f in orglist: # .values():
    #req [f.name] = ''
    req [f[1]] = ''
  
  for f in paylist:
    req [f[1]] = ''
  
  req ['password'] = 'asfv'
  req ['password2'] = 'wefvwefvwevwef'
  req ['ccnum'] = '4128 130 446 045 '
  req ['shipmeth'] = "('next day', '85')"
  req.ccyear = '2001'
  req.ccmonth = '2'
  req.paymeth = 'byccard'
  slf.REQUEST = req
  slf.session = {'checkout': {}, 'cart': {}}
  slf.aq_parent = slf
  slf.images = slf  # { 'pix' : '1-pixel transparent image', 'viewcart' : 'cart image' }
  slf.viewcart = 'image'
  slf.revieworder = 'image'

  def step (self):
    return 'step number'

  slf.step1 = step
  slf.step2 = step
  slf.step3 = step
  slf.checkout_faq = step
  
  shipinfo (slf)
  billinfo (slf)
  #persinfo (slf)
  payinfo (slf)
  ordinfo (slf)
  #orginfo (slf)
  pageinfo (slf)
  #ses = slf.session ['checkout']
  #print `ses`
  #print `req`
  #print join ( split (`globals()`, ','), '\n')

