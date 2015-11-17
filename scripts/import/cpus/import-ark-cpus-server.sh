import_ark_cpus() {
    python tablescrape.py http://ark.intel.com/products/family/$arknum/$arkurl $tableinx \
    | python parse_cpus.py "$choicecat" \
    > $arkurl.csv

    ../../../manage.py importcsv --model=products.choice $arkurl.csv
}

#### Intel Server CPUs - from 
# python tablescrape.py http://ark.intel.com/ 3

tableinx=1

arknum=78584
arkurl=Intel-Xeon-Processor-E7-v2-Family
choicecat="Xeon E7 v2 CPUs" 

import_ark_cpus


akrnum=59139
arkurl=Intel-Xeon-Processor-E7-Family
choicecat="Xeon E7 CPUs" 

import_ark_cpus


tableinx=2


arknum=78583
arkurl=Intel-Xeon-Processor-E5-v3-Family
choicecat="Xeon E5 v3 CPUs" 

import_ark_cpus


arknum=78582
arkurl=Intel-Xeon-Processor-E5-v2-Family
choicecat="Xeon E5 v2 CPUs" 

import_ark_cpus


arknum=59138
arkurl=Intel-Xeon-Processor-E5-Family
choicecat="Xeon E5 CPUs" 

import_ark_cpus


# http://ark.intel.com/products/family/78581/Intel-Xeon-Processor-E3-v3-Family
arknum=78581
arkurl=Intel-Xeon-Processor-E3-v3-Family
choicecat="Xeon E3 v3 CPUs" 

import_ark_cpus


# http://ark.intel.com/products/family/78580/Intel-Xeon-Processor-E3-v2-Family
arknum=78580
arkurl=Intel-Xeon-Processor-E3-v2-Family
choicecat="Xeon E3 v2 CPUs" 

import_ark_cpus


#http://ark.intel.com/products/family/59137/Intel-Xeon-Processor-E3-Family
arknum=59137
arkurl=Intel-Xeon-Processor-E3-Family
choicecat="Xeon E3 CPUs" 

import_ark_cpus



