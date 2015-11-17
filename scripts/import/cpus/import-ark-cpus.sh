import_ark_cpus() {
    python tablescrape.py http://ark.intel.com/products/family/78582/$arkurl 2 \
    | python parse_cpus.py "$choicecat" \
    > $arkurl.csv
}

arkurl=Intel-Xeon-Processor-E5-v2-Family
choicecat="Xeon E5 v2 CPUs" 

import_ark_cpus


