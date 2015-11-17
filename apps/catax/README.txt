12/26/14:

Latest rates in csv format are here:

http://www.boe.ca.gov/sutax/files/city_rates.csv

and linked here:

http://www.boe.ca.gov/sutax/pam71.htm

and are from Oct 1st, 2014.

See views.py for code to extract, that we can split out into a script file.

JJW



4/11/12 JJW

- Rates by zipcode are from:

    http://www.taxrates.com/resources/tax-rate-tables/California-sales-tax-rate-table/

    (Avalara) and include other fields too - there are about ~2600 records.

    filename as of Apr 2012 is:

    TAXRATES_ZIP5_CA201204.csv


- Rates by city are directly from the State of CA, and are from:

    http://www.boe.ca.gov/sutax/pam71.htm

    about ~1700 records.


    filename as of Apr 2012 is city_rates.csv

    rates are new as of Apr 1.