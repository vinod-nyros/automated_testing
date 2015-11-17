from django.core.management.base import BaseCommand
import urllib2, re
from pprint import pprint,pformat
from catax.models import Catax
from utils import create_or_update

trace = 1
teeth = 1  # write the new catax.py file
dbteeth = 0  # upd the db :-)


class Command(BaseCommand):
    manual_help = "python manage.py update_ca_tax "
    def handle(self, *args, **options):
        self.update_ca_tax()

    def update_ca_tax (self):  # loads the normalized-by-county-rate table, ~110 entries
        url="http://www.boe.ca.gov/sutax/files/city_rates.csv"
        data = urllib2.urlopen(url)
        while True:
            each_line = data.readline()
            if "City" in each_line:
                break# skip over column headings
        #### First build unique dict tree by county & tax rate, listing cities:
        catax = {}
        count = 0
        while True:
            each_line = data.readline()
            words = each_line.split(",")
            if len(words)!=3:
                break
            city = words[0]
            rate = words[1]
            county = words[2]
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
            pprint(catax)
        catax2 = []
        for county, ratesdict in catax.items():
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
            f = open ("./test.py",'w')
            f.write ('calist=' + pformat (calist))
            f.close()
