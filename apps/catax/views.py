# -*- coding: utf-8 -*-

import re
from csv import reader
from pprint import pprint, pformat

from utils import create_or_update

#from customers import models
#from legacy import models
#from legacy.models import Product
#from catax import models
from catax.models import Catax   # ,CataxByCity
#from apps.catax.models import Catax   # ,CataxByCity


#### Globals

trace = 0
teeth = 0  # write the new catax.py file
dbteeth = 1  # upd the db :-)


#### Load / Cmdline Functions

def load (csvfile):  # for a by-city table with ~2600 entries
    rows = reader (csvfile)
    rows.next()  # skip over column headings

    for city, tax, county in rows:
        unique_city = city.replace ('*','')

        try:
            instance, created = create_or_update (CataxByCity, dict (city=unique_city), dict (tax=tax, county=county))
        except DuplicateException, e:
            unique_city = '%s %(%s County)' % (city, row.county)
            instance, created = create_or_update (CataxByCity, dict(city=unique_city), dict (tax=tax, county=county))

        if created:
            print 'Created:', unique_city, tax
        else:
            print 'Updated:', unique_city, tax


def load2 (csvfile):  # loads the normalized-by-county-rate table, ~110 entries
    rows = reader (csvfile)
    rows.next()  # skip over column headings


    #### First build unique dict tree by county & tax rate, listing cities:

    catax = {}
    count = 0

    for city, rate, county in rows:
        count += 1
        city = re.sub('(\(.*\))', '', city)
        city = city.strip().replace ('*', '')
        county = county.strip().replace ('*', '')
        rate = '%4g' % float (rate.strip('% '))

        if county in catax:
            if rate in catax [county]:
                catax [county][rate] += ', ' + city
            else:
                catax [county][rate] = city
        else:
            catax [county] = { rate:city }

    if trace:
        pprint (catax)


    #### Now count cities and build minimized list - county default is highest city count, then exceptions listed with cities

    catax2 = []

    for county, ratesdict in catax.items():
        #print len (ratesdict)
        rates = [[rate, len (cities.split(',')), cities] for (rate, cities) in ratesdict.items()]
        rates.sort(key=lambda r: r[1], reverse=1)
        #print rates
        catax2 += [(county, '', rates [0][0], rates [0][1])]
        rates [0].append (county)  # append name

        for r in rates [1:]:
            catax2 += [(county, r [2], r [0], r [1])]
            r.append ('%s (%s)' % (county, r [2]))

        if dbteeth:
            for rate, count, cities, name in rates:
                #for (rate, cities) in ratesdict.items()

                instance, created = create_or_update (Catax, dict(name=name), dict (tax=rate, county=county, cities=cities, count=count))

                if created:
                    print 'Created:', name, rate
                else:
                    print 'Updated:', name, rate


    catax2.sort()
    if trace:
        pprint (catax2)
        #print "Org len (total CA cities):", len (catax.items()), "Normalized:", len (catax2)
        print "Org len (total CA cities):", count, "Counties:", len (catax), "Unique rates:", len (catax2)


    #### Now create legacy catax.calist for Zope, as needed

    if teeth:
        calist = [ ('', 'Select CA County') ]

        for (county, city, tax, count) in catax2:
            tax = float (tax) #+ 1.25

            if city:
                val = county + ' (%s)' % city
            else:
                val = county

            val = val + ' %.4g%%' % (tax)

            if city:
                county = '%s.%s' % (county, city.replace(' ','').replace(',','_'))

            nam = "(%s,'%s')" % (tax, county)
            calist.append ( (nam, val) )

        f = open ('catax.py','w')
        f.write ('calist=' + pformat (calist))
        f.close()


#### main for loading and testing

if __name__ == '__main__':
    load2 (open ('./city_rates.csv'))
