import csv

trace = 0

#def u(s):
#    try: return unicode (s)
#    except: pass
#    return unicode ('')

f = open ("WD Hard Drives Feb 2015 - Sheet1.csv")

reader = csv.reader (f)
lines = [l for l in reader]

if trace:
    print lines [0]

lines = lines [1:]

red = [l[1] for l in lines]
green = [l[3] for l in lines]
black = [l[5] for l in lines]
blue = [l[7] for l in lines]
purple = [l[9] for l in lines]
se = [l[11] for l in lines]
redpro = [l[13] for l in lines]
re = [l[15] for l in lines]
xe = [l[17] for l in lines]

if trace:
    print len (red)
    print len (redpro)
    print len (green)
    print len (black)
    print len (blue)
    print len (purple)
    print len (se)
    print len (re)
    print len (xe)
'''
for i in range (20):
    #print i
    s = red [i]
    s = s.replace ('*','').replace ('"','')
    #print s #red [i]
    comment = s
    toks = s.split()
    cost = [t for t in toks if '$' in t][0].strip ('$')
    cost = float(cost.replace (',',''))
    pack = 'Pack' in s or 'pack' in s  # parse for numeric predecessor
    frm = [t for t in toks if 'from' in t or '+' in t]

    #for t in toks:
    #    if t.strip ('+').isdigit():
    #        print t, 'YES'

    #print frm

    #t.strip ('+').isdigit()

    #print cost
    model = [t for t in toks if 'EFRX' in t]  #also strip ','
    model = model [0] if model else None
    if model and frm and cost <1000:
        print i, model, cost
        #print 'Pack' in s
        #print s
'''

def parse (a, matchname, sortorder):
    for i in range (20):
        s = a [i]
        s = s.replace ('*','').replace ('"','')
        comment = s
        s = s.replace ('Western Digital', 'WD').replace ('Tb','TB').replace ('terabytes','TB')\
            .replace ('WD 3 TB WD Red','WD Red 3 TB').replace ('WD WD30EFRX','WD Red 3 TB')
        toks = s.split()
        try:
            cost = [t for t in toks if '$' in t][0].strip ('$')
        except:
            if trace: print toks
            continue
        cost = float(cost.replace (',',''))
        pack = 'Pack' in s or 'pack' in s  # parse for numeric predecessor
        frm = [t for t in toks if 'from' in t or '+' in t]

        # skip ones without "from nn stores..", or packs (costing >1000), older / slower, SAS for now
        if not frm or cost >1000 or \
                [t for t in toks if t in ['ATA-100','ATA-300','1.5Gb/s','3Gb/s','SAS','SCSI']]:
            continue

        tb = [t for t in toks if 'TB' in t or 'GB' in t or t=='1.5' or t.isdigit() and int(t)<4000]
        tb = ''.join (tb [:2])
        #model = [t for t in toks if suffix in t]  #also strip ','
        model = [t.strip(',') for t in toks if len(t.strip(','))<=10 and len(t.strip(','))>2 and t.startswith('WD')]
        model = model [0] if model else ''
        rpm = [t for t in toks if t.isdigit() and int(t)>4000]
        rpm = rpm[0]+'rpm' if rpm else ''
        name = ' '.join (toks [4:7]) if toks [6] == 'Pro' else' '.join (toks [4:6])
        if name.lower() != matchname.lower():
            if trace:
                print name, matchname, 'NOMATCH'
                print toks
            continue

        inches = [t for t in toks if t in ['3.5','2.5']]
        inches = inches[0] + '"' if inches else ''
        #if model and frm and cost <1000:
        choicecategory = '%s %s\" HDs' % (name, inches)
        blurb = [t for t in toks if t in ['SATA','Serial'] or 'Gb/' in t or 'ATA-' in t]
        blurb = ' '.join (blurb [0:2]) if blurb else ''

        name = '%s %s %s\" %s internal hard drive' % (name, tb, inches, rpm)

        #print i, cost, name, tb, rpm, inches, 'drive', model, blurb, comment #'|'.join (toks[4:25])
        #print s
        print ','.join ('"%s"' % t for t in (cost, name, choicecategory, blurb, comment, '', '', '', True, sortorder))


print "cost,name,choicecategory,blurb,comment,supplier,price,multiplier,published,sortorder"
parse (red, 'WD Red', 5000) #'EFRX')
parse (redpro, 'WD Red Pro', 5010) #'EFRX')
parse (green, 'WD Green', 5020) #'EZRX')
parse (black, 'WD Black', 5030) #'FZEX',
parse (blue, 'WD Blue', 5040)
parse (purple, 'WD Purple', 5050)

#parse (se, 'WD Se') NFG

# TBD, later, SAS:
#parse (re, 'WD Re')
#parse (xe, 'WD Xe')


