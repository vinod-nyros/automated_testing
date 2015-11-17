
lineitems = int (lineitems)

# id is always first
columns = '''id title email
shiptype shipname shiporg shipaddr1 shipaddr2 shipcity shipstate shipzip shipcountry shipregn shipphone shipper shipmethod shiprate shipcost shippay shipprice shipacct shipincl
billtype billname billorg billaddr1 billaddr2 billcity billstate billzip billcountry billregn billphone billfax billinitials billemail
billsame iagree
reftyp refsrc refnum approved_date saleinitials
paymeth payterms payinitials cclast4 ccmonth ccyear ccauthnum cc_cvv cc_corp_pin cc_charged_date cc_initials
taxcounty taxrate salestax
instr orderdate orderstatus ordernum internalnotes oldnotes adjustments adjustamt costofgoods
tracknumbers shipdate shipinitials'''.split()

''' example:
addorder (id=22148,title="chris@ctpllc.com",billtype="billus",email="chris@ctpllc.com",shipmethod="FedEx Standard Overnight",shiprate="1.0",
shipcost="0.0",shipcountry="US",cclast4="3475",billname="Christopher Reade",shipzip="70115",ccyear="2004",shipcity="New Orleans",billcity="new orleans",
shipname="Christopher Reade",instr="['Please cell 504.299.8333 x201 to confirm']",ccmonth="4",shipstate="LA",shipphone="504.299.8333",
shiptype="shipus",billstate="LA",billzip="70115",paymeth="byccard",shipaddr1="1515 Poydras Street",shiporg="CTPLLC",
billaddr1="3952 camp street",orderdate="2003/06/15 19:38:01 GMT-7",ccauthnum="586888",adjustments="['']",
internalnotes="['Need damage details to submit claim to shipper.  -Liz', 'Sent email 6/16 and left phone message 6/17
re: need CVV number to process order.', '', 'Wrong mobos came in 7/7. New mobos due 7/8.', '',
"JJW 10/7/04 - closed - don't know why it was still RMA."]",adjustamt="0.0",orderstatus="closed",index="order",ordernum="22148",cc_cvv="",
cc_corp_pin="",cc_charged_date="6/23/03",cc_initials="Liz",shipper="fedex1a",tracknumbers="['792293818522', '792293818500']",
shipdate="7/23/03",shipinitials="MKM" )
'''

#from types import ListType, TupleType

def qt (s):
    #if isinstance (s, (list, tuple)):
    #if isinstance (s, (ListType, TupleType)):
    #if same_type (s, (list, tuple)):
    #if isinstance (s, (type ([]), type (()))):
    if same_type (s, []) or same_type (s, ()):
        s = '|'.join (s)
    s = str(s)
    s = s.replace ('"', '\\"')
    s = s.replace (',','\,')
    #if 'PO 471335' in s:
    #    raise (s + s.replace ('"','AHA'))
    return s

def checkfolder (fold):
  id = fold.id

  if str (id).isdigit():
    if int(id) < 999:
      if lineitems:
        #print '# processing lineitem', id
        #minitem = min (int(id), minitem)
        #maxitem = max (int(id), maxitem)
        #pairs = ['addline (id=' + id]
        pass
    else:
      if not lineitems:
        props = dict ([(k,v) for k,v in fold.propertyItems()])
        print '%s,' % id, ', '.join (['"%s"' % qt (props.get (k, '')) for k in columns [1:]]),

        # now check we got all of them:
        for k in columns [1:] + ['index']:
            props.pop (k, '')

        if props:
            raise `props`

    '''
    for d in fold.objectValues ('DTML Document'):
      id = d.id
      if callable (id):  id = id()

      pairs = ['additem (id=' + id]

      for k,v in d.propertyItems():
        pairs += ['%s="%s"' % (k,qt(v))]

      print ','.join (pairs), ')'
      '''

  # Recurse - (postorder traversal!)
  #if id not in ['archived', 'archived2001', 'archived2002', 'archived2003', 'archived2004', 'archived2005']:
  for f in fold.objectValues ('Folder'):
      result = checkfolder (f)
      if result:
          print result

  if printed:
      return printed


print '<pre>'
print ', '.join (columns)
print checkfolder (context.orders)  #  ['30487']),
return printed
