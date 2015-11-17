import csv

#reader = csv.DictReader (open ('CPUs-test.csv', 'rb'))
reader = csv.DictReader (open ('CPUs.csv', 'rb'))

print reader.fieldnames
#writer.fielddnames = reader.fieldnames

#writer = csv.DictWriter (open ('CPUs-test-out.csv', 'wb'), reader.fieldnames)
writer = csv.DictWriter (open ('CPUs-out.csv', 'wb'), reader.fieldnames)  

writer.writeheader()

sortorder = 1300

for line in reader:
    print line ['name']

    line ['comment'] = 'CPU Passmark score ' + line ['comment'] 

    line ['blurb'] = "%s - %s" % (line ['name'], line ['comment']) 
    line ['published'] = True
    
    scost = line ['cost']
    
    try:
        cost = float (scost)
    except:
        if scost.endswith ('*'):
            line ['cost'] = float (scost.replace('*','').replace('$','').replace(',',''))
            line ['comment'] += ' - Price is last known price' 
            
        if scost == 'NA':
            line ['cost'] = 0.0
            line ['published'] = False
    
    line ['sortorder'] = sortorder
    sortorder -= 1
    
    line ['choicecategory'] = 'CPUs'
    
    writer.writerow (line)

