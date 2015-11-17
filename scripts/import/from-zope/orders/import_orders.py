# nope, doesn't work:
# coding: utf-8

# but this does:
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import datetime
import csv

from django.template.defaultfilters import slugify

from  parsedatetime import parsedatetime as pdt, parsedatetime_consts as pdc
import time, datetime

#### parsedatetime stuff

# create an instance of Constants class so we can override some of the defaults
c = pdc.Constants()

# create an instance of the Calendar class and pass in our Constants # object instead of letting it create a default
p = pdt.Calendar(c)

# parse "tomorrow" and return the result
#result = p.parse("tomorrow")

# parseDate() is a helper function that bypasses all of the # natural language stuff and just tries to parse basic dates # but using the locale information
#result = p.parseDate("4/4/80")


#### globals

trace = 0
teeth = 1       # whether to get latest extract from zope
dbteeth = 1     # whether to update db

if dbteeth:
    from django_eracks.apps.orders.models import ImportedOrder
    #from utils import setfields


#### main

## todo jjw 6/17/12:
## d get pw via input
## get as far as we can w/dl of both orders and lineitems, then proc them via csv reader

if teeth:
    wget_command = "wget http://joe:%s@www.eracks.com:9080/eracks/admin/extract_orders.csv?lineitems=0"
    wget_ask_command = "wget --ask-password http://joe@www.eracks.com:9080/eracks/admin/extract_orders.csv?lineitems=0"

    try:
        import getpass
        password = getpass.getpass('Enter zope password: ')
        print wget_command % password # '(hidden)'
        print os.system (wget_command % password)
        print 'Done.'
    except Exception, e:
        print 'Exception:', `e`
        print
        print "So don't forget to get the latest with wget first:"
        print wget_command

    fin = open ('extract_orders.csv?lineitems=0')
    fout = open ('extracted_orders.csv', 'w')
    fout.write ('\n'.join ([l for l in fin.read().splitlines() [1:] if l]))
    fout.close()


#reader = csv.reader(open('extracted_orders.csv', 'rb'))  # , delimiter=' ', quotechar='|')
reader = csv.DictReader(open('extracted_orders.csv', 'rb'), doublequote=False, escapechar='\\', skipinitialspace=True )  # , delimiter=' ', quotechar='|')

#print reader.fieldnames

for line in reader:
    ordernum = line ['ordernum']
    d = line ['id']

    #if int (d) < 47000: #43000: #41000: #38000: #34000:  #31900: #31450:  # 28000:  # 27300:  # 26400:  # 24837:
    #    continue

    #if int (d) != 22152: # ESR
    #    continue

    #if int (d) != 25887: # binary.cc
    #    continue

    if int (d) == 47058:
        continue  # skip it, empty order

    print 'importing', d
    assert d == ordernum

    #billtype    = line.get ('billtype', '')
    #billcountry = line.get ('billcountry', '')
    shiptype    = line.get ('shiptype', '')
    shipcountry = line.get ('shipcountry', '')

    #if billtype and billcountry:
    #    assert (billtype=='billus') == (billcountry=='US')  nope - Marc Knoop, Netherlands Antilles nfg

    #if shiptype and shipcountry:
    #    assert (shiptype=='shipus') == (shipcountry=='US') nope - 17155 NY, AE

    if dbteeth:
        #from pprint import pprint
        #pprint (line)

        #line = dict ([(unicode(k).strip(), unicode(v).strip(' "')) for k,v in line.items() if k]) # and 'payinitials' not in k])
        #pprint (line)

        #order, created = ImportedOrder.objects.get_or_create (id=line ['id'], defaults = line)
        #print order, created

        #if not created:
        #    order.update (**line) # might need to go get my utils fn for this

        o = ImportedOrder (id=line.pop('id'))
        o.shiprate = line.pop ('shiprate')
        o.shipcost = line.pop ('shipcost')
        o.ordernum = line.pop ('ordernum')
        o.cc_corp_pin = line.pop ('cc_corp_pin')

        if not o.cc_corp_pin:
            o.cc_corp_pin = None

        o.ccmonth = line.pop ('ccmonth')

        if not o.ccmonth:
            o.ccmonth = 1

        o.ccyear = line.pop ('ccyear')

        if not o.ccyear:
            o.ccyear = 2001

        o.email = line.pop ('email').split() [0].strip (' ,')
        o.shipmethod = (line.pop ('shipmethod').split() or ['']) [0]
        o.paymeth = line.pop ('paymeth').replace ('credit card','byccard')

        shipzip = line.pop ('shipzip')
        shipregn = line.pop ('shipregn')
        if shipzip == 'NETHERLANDS ANTILLES' and not shipregn:
            o.shipregn = shipzip
            o.shipzip = ''
        else:
            o.shipzip = shipzip
            o.shipregn = shipregn

        shipstate = line.pop ('shipstate')
        if shipstate == 'VA  20196':         #order 16654 - or len(shipstate) >2 and ' ' in shipstate
            o.shipstate = 'VA'
            o.shipzip = '20196'
        else:
            o.shipstate = shipstate

        o.shipdate          = line.pop ('shipdate')
        o.cc_charged_date   = line.pop ('cc_charged_date')
        o.approved_date     = line.pop ('approved_date')
        o.orderdate         = line.pop ('orderdate')

        def massage_date (dt):
            if dt:
                if dt == 'Jun 20 2003':  # 22005
                    dt = '2003-06-20 12:00:00'
                elif dt == '8-4-03':  # 23814?
                    dt = '2003-08-04 12:00:00'
                elif dt == '12/30/03 - 1/7/04':  # 25887
                    dt = '2004-01-07 12:00:00'
                elif dt == '1-6-04':  # 26101
                    dt = '2004-01-06 12:00:00'
                elif dt == '1-10-04':  # 26101
                    dt = '2004-01-10 12:00:00'
                elif dt == '1-14-04':  # 2610x
                    dt = '2004-01-14 12:00:00'
                elif dt == '1-15-04':  # 2610x
                    dt = '2004-01-15 12:00:00'
                elif dt == '1-16-04':  # 2610x
                    dt = '2004-01-16 12:00:00'
                elif dt == '1-17-04':  # 2610x
                    dt = '2004-01-17 12:00:00'
                elif dt == '1-19-04':  # 2610x
                    dt = '2004-01-19 12:00:00'
                elif dt == '1-20-04':  # 2610x
                    dt = '2004-01-20 12:00:00'
                elif dt == '1-21-04':  # 2610x
                    dt = '2004-01-21 12:00:00'
                elif dt == '1-23-04':  # 2610x
                    dt = '2004-01-23 12:00:00'
                elif dt == '1-30-04':  # 26xxx
                    dt = '2004-01-30 12:00:00'
                elif dt == '2-5-04':  # 26xxx
                    dt = '2004-02-05 12:00:00'
                elif dt in ['2-6-04', '2-06-04']:  # 26xxx
                    dt = '2004-02-06 12:00:00'
                elif dt == '2-9-04':  # 26xxx
                    dt = '2004-02-09 12:00:00'
                elif dt == '2-10-04':  # 26xxx
                    dt = '2004-02-10 12:00:00'
                elif dt == '2-11-04':  # 26xxx
                    dt = '2004-02-11 12:00:00'
                elif dt == '06-04-04':  # 27xxx
                    dt = '2004-06-04 12:00:00'
                elif dt == '06-25-04':  # 27xxx
                    dt = '2004-06-25 12:00:00'
                elif dt == '6.14-21.04':  # 27xxx
                    dt = '2004-06-21 12:00:00'
                elif dt == '07-01-04':  # 27xxx
                    dt = '2004-07-01 12:00:00'
                elif dt == 'June 10 2004':  # 27xxx
                    dt = '2004-06-10 12:00:00'
                elif dt == '09 10 04':  # 27xxx
                    dt = '2004-09-10 12:00:00'
                elif dt == 'Jan 25 2005':  # 28xxx
                    dt = '2005-01-25 12:00:00'
                elif dt == '12-09/05':  # 31xxx
                    dt = '2005-12-09 12:00:00'
                elif dt == '04-21-06':  # 319xx
                    dt = '2006-04-21 12:00:00'
                elif dt == '09-05-06':  # 324xx
                    dt = '2006-09-05 12:00:00'
                elif len (dt) < 12:
                    #print dt
                    dt = datetime.datetime.fromtimestamp (time.mktime (p.parseDate (dt))).isoformat()
                else:
                    dt = '-'.join(dt.split ('/',2))
                    dt = str(dt.replace (' US/Pacific','-08:00').strip())
                    dt = str(dt.replace (' GMT-7','-07:00').strip())
                    if dt == '5-28-03':  # 21752 Don witt.   grrr.
                        dt = '2003-05-28 12:00:00'
                    elif dt == '03/0/05':
                        dt = '2003-03-08 12:00'
            else:
                dt = None
            return dt

        o.shipdate          = massage_date (o.shipdate)
        o.cc_charged_date   = massage_date (o.cc_charged_date)
        o.approved_date     = massage_date (o.approved_date)
        o.orderdate         = massage_date (o.orderdate)

        #if int (d) == 22152: # ESR - paymeth lengthened to 12
        #    print o.shipstate, o.shipzip, o.shipregn, o.shipmethod, o.paymeth, o.shiprate, o.shipacct, o.email, o.title

        if int (d) == 24837:
            o.internalnotes = unicode (line.pop ('internalnotes'), errors='ignore') #.replace ('0x94', "'").replace ('�',"'")
            o.adjustments = unicode (line.pop ('adjustments'), errors='ignore') #.replace ('\\0x94', "'").replace ('�',"'")
            #print o.internalnotes
            #print o.adjustments

        if int (d) in [26103, 26106, 27474]:
            o.shipaddr1 = unicode (line.pop ('shipaddr1'), errors='ignore')

        if int (d) == 27065:
            o.shipacct = line.pop ('shipacct') [:20]

        if int (d) == 27295:
            #print o.shipstate, o.shipregn, o.shipmethod, o.paymeth, o.shiprate
            o.shipzip = o.shipzip.split() [0]

        if int (d) == 27476:
            o.saleinitials = line.pop ('saleinitials').split() [0]

        if int (d) == 28494:
            o.shipinitials = line.pop ('shipinitials').replace (' ','')

        if int (d) == 28812:
            line.pop ('payterms')
            o.payterms = 'Net 30'

        if int (d) == 31476:
            print o.shipstate, o.shipzip, o.shipregn, o.shipmethod, o.paymeth, o.shiprate, o.shipacct
            o.shipacct = line.pop ('shipacct')
            o.instr = line.pop ('instr') + '||from shipacct:|' + o.shipacct
            o.shipacct = ''

        if int (d) == 31502:
            #print o.shipstate, o.shipzip, o.shipregn, o.shipmethod, o.paymeth, o.shiprate, o.shipacct, o.email, o.title
            o.title = line.pop ('title')
            o.internalnotes = line.pop ('internalnotes') + '||extra email: ' + o.title.split() [1]
            o.title = o.title.split () [0].strip (', ')
            #print o.title, o.email

        if int (d) == 31705:
            line.pop ('saleinitials')

        if int (d) == 33763:
            o.shipphone = line.pop ('shipphone').replace (' ','')

        if int (d) == 38501:
            o.billsame = line.pop ('billsame').replace ('False', 'off')

        if int (d) == 38502:
            o.billsame = line.pop ('billsame').replace ('True', 'on')

        if int (d) == 38738:
            o.shipphone = line.pop ('shipphone') [:20]  # it's a fraud order anyway

        if int (d) in [38738, 39307]:
            o.shipper = line.pop ('shipper') [:15]  # it's an invalid or fraud order anyway

        if int (d) == 41362:
            o.billcity = 'Munchen'
            line.pop ('billcity')

        if int (d) == 42543:
            #print o.shipstate, o.shipzip, o.shipregn, o.shipmethod, o.paymeth, o.shiprate, o.shipacct, o.email, o.title
            o.shipmethod = 'ground'

        if int (d) == 43821:
            o.shipname = unicode (line.pop ('shipname'), errors='ignore')
            o.billname = unicode (line.pop ('billname'), errors='ignore')

        if int (d) in [47082, 47083]:
            #print o.shipstate, o.shipzip, o.shipregn, o.shipmethod, o.paymeth, o.shiprate, o.shipacct, o.email, o.title
            o.shipregn = 'Quebec'

        if int (d) == 47600:
            o.shipaddr1 = unicode (line.pop ('shipaddr1'), errors='ignore')

        #o.update (line)
        #o.save()
        #continue

        for k,v in line.iteritems():
            #print 'setting:', k, 'to', v
            setattr (o, k, v)
            #o.save()

        #setfields (o, line)
        try:
            o.save()
        except Exception, e:
            print e
            from pprint import pprint
            pprint (line)
            raise

#print reader.fieldnames

