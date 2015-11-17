# -*- coding: utf-8 -*-
sqls = '''
Choices insert

INSERT INTO  choices (name, current, id, cost, sortorder, comment)
    VALUES ('Intel Core 2 Duo Mobile T8100 2.1GHz 3MB CPU', 'T', DEFAULT, 194, 1765, 'for GAMER laptop');


---

Show DESQ Processor options

Select products.id, products.name, options.id, options.name, 
choices.id, choices.name, choices.cost, choices.price, choices.sortorder
where products.id = prodopts.productid AND prodopts.optionid = options.id
AND choices.id = prodoptchoices.choiceid AND 
prodoptchoices.productoptionid = prodopts.id AND products.id = 12819 AND
options.id = 6564 ORDER BY choices.cost;

---
show all options/choices for a product

Select products.id, products.name, options.id as optionsid, options.name, 
prodoptchoices.productoptionid, prodopts.defaultchoiceid,
choices.id, choices.name, choices.cost, choices.price, choices.sortorder
where products.id = prodopts.productid AND prodopts.optionid = options.id
AND choices.id = prodoptchoices.choiceid AND 
prodoptchoices.productoptionid = prodopts.id AND 
products.name LIKE '%/OPTDESKTOP' 
ORDER BY options.id, choices.cost;

---

Delete from prodoptchoices old processors, etc. 

DELETE FROM prodoptchoices 
WHERE prodoptchoices.choiceid = 31466 AND (old choice id) prodoptchoices.productoptionid = 12988  (for only one product)
RETURNING *;

---

Show everything that uses a certain choiceid

SELECT  products.sku, prodopts.id, products.baseprice, options.name as option, choices.name as choice, choices.cost, prodoptchoices.pricedelta  
from products, options, prodopts, choices, prodoptchoices 
WHERE 
 (prodopts.productid = products.id) AND
 (prodopts.optionid = options.id)  AND  

 (prodoptchoices.productoptionid = prodopts.id)  AND
 (prodoptchoices.choiceid = choices.id) AND 

 (prodoptchoices.choiceid = '31466') 
ORDER BY products.sku, options.name, prodopts.optionid, choices.name;

---

Show me every product that uses Adaptec% as a defaultchoice somewhere

SELECT  products.sku, prodopts.id, products.baseprice, options.name as option, choices.name as choice, choices.cost, prodoptchoices.pricedelta  
from products, options, prodopts, choices, prodoptchoices 
WHERE 
 (prodopts.productid = products.id) AND
 (prodopts.optionid = options.id)  AND  

 (prodoptchoices.productoptionid = prodopts.id)  AND
 (prodoptchoices.choiceid = choices.id) AND 
 (choices.id = prodopts.defaultchoiceid) AND

 (choices.name LIKE 'Adaptec%') 
ORDER BY products.sku, options.name, prodopts.optionid, choices.name;

---

Show me everything that has an LSI card somewhere

SELECT  products.sku, prodopts.id, products.baseprice, 
options.name as option, choices.id, choices.name as choice, choices.cost, 
prodoptchoices.pricedelta, prodopts.defaultchoiceid  
from products, options, prodopts, choices, prodoptchoices 
WHERE 
 (prodopts.productid = products.id) AND
 (prodopts.optionid = options.id)  AND  
 (prodoptchoices.productoptionid = prodopts.id)  AND
 (prodoptchoices.choiceid = choices.id) AND 
 (choices.name like 'LSI%') 
ORDER BY products.sku, options.name, prodopts.optionid, choices.name;

---

Update ProdOptChoices

UPDATE prodoptchoices 
  SET choiceid = 35408
  WHERE prodoptchoices.choiceid = 37254;
replaces old processor for a new one across models.

---

Replace 80GB SATA for SATA 2 in all bays of PREMIUM2

Update prodoptchoices set choiceid = 32407
where products.id = prodopts.productid AND prodopts.optionid = options.id
AND choices.id = prodoptchoices.choiceid AND 
prodoptchoices.productoptionid = prodopts.id AND 
products.sku = 'PREMIUM2' AND
options.name like 'Removable HD%' AND 
choices.id = 27251;


---

Show default choices for each option for QUADPREM

Select products.id, products.name, options.id, options.name, 
prodoptchoices.productoptionid,
choices.id, choices.name, choices.cost, choices.price, choices.sortorder
where products.id = prodopts.productid AND prodopts.optionid = options.id
AND choices.id = prodoptchoices.choiceid AND 
prodoptchoices.productoptionid = prodopts.id AND 
choices.id = prodopts.defaultchoiceid AND
products.name LIKE '%/QUADPREM' 
 ORDER BY choices.name;


---

Print out baseprices, and total default costs for each sku, sort by category, then ascending total cost.


Select  categories.name, products.sku, products.baseprice, sum(choices.cost) as total 
where categories.id = products.categoryid AND
products.id = prodopts.productid AND 
products.current = 'T' AND
prodopts.optionid = options.id
AND choices.id = prodoptchoices.choiceid AND 
prodoptchoices.productoptionid = prodopts.id AND 
choices.id = prodopts.defaultchoiceid 
group by categories.name, products.sku, products.baseprice
order by categories.name, total;


---

Adding a comment field to a table! 

Alter table optionchoices 
add column comment varchar(80);

---

Show all choices for PCI-e across products

Select products.id, products.name, options.id, options.name, 
prodoptchoices.productoptionid,
choices.id, choices.name, choices.cost, choices.price, choices.sortorder
where products.id = prodopts.productid AND prodopts.optionid = options.id
AND choices.id = prodoptchoices.choiceid AND 
prodoptchoices.productoptionid = prodopts.id AND 
options.id = 36525 ORDER BY choices.name;

---

Get the set of general SATA2 HD choices

Select options.id, optionchoices.comment, options.name, choices.id, choices.name, choices.cost
FROM options, choices, optionchoices 
where optionchoices.optionid = options.id 
AND optionchoices.choiceid = choices.id
AND optionchoices.optionid = 32416
ORDER BY choices.cost;

---

These are the prodopts that I went through to make sure all SATA2 defaultchoices ids are OK and all choices are complete.
SATA -> SATA 2


SELECT  prodopts.id, products.sku, prodopts.id, products.baseprice, options.name as option, choices.name as choice, choices.cost, prodoptchoices.pricedelta  
from products, options, prodopts, choices, prodoptchoices 
WHERE 
 (prodopts.productid = products.id) AND
 (prodopts.optionid = options.id)  AND 
 (prodoptchoices.productoptionid = prodopts.id)  AND
 (prodoptchoices.choiceid = choices.id) AND 
 (products.current = 'T') AND
 (prodoptchoices.choiceid = '27251') 
ORDER BY products.sku, options.name, prodopts.optionid, choices.name;

---

Who is using 80GB as a defaultchoice? 

SELECT  prodopts.id, products.sku, prodopts.id, products.baseprice, options.name as option, choices.name as choice, choices.cost, prodoptchoices.pricedelta  
from products, options, prodopts, choices, prodoptchoices 
WHERE 
 (prodopts.productid = products.id) AND
 (prodopts.optionid = options.id)  AND 
 (prodoptchoices.productoptionid = prodopts.id)  AND
 (prodoptchoices.choiceid = choices.id) AND 
 (products.current = 'T') AND
 (prodopts.defaultchoiceid = choices.id) AND
 (prodoptchoices.choiceid = '27251') 
ORDER BY products.sku, options.name, prodopts.optionid, choices.name;


---

Test for nested query. (then add 1.5TB drives to everybody who has a 1TB drive in selection).

-- my test (inserts into two old skus)

INSERT into prodoptchoices ( pricedelta, productoptionid, choiceid, current)
Select   0, productoptionid, 39338, 'T' 
from prodoptchoices
where (prodoptchoices.productoptionid = 4310 or 
prodoptchoices.productoptionid = 30895) and 
prodoptchoices.choiceid = 36230;

---

Add 1.5TB to every prodoptchoice set that has 1TB in it

-- OK, assumes the nested query test works -

INSERT into prodoptchoices ( pricedelta, productoptionid, choiceid, current)
Select   0, prodoptchoices.productoptionid, 39338, 'T' 
from prodoptchoices,products, prodopts,options, choices 
where (
 prodopts.productid = products.id AND
 prodopts.optionid = options.id  AND 
 prodoptchoices.productoptionid = prodopts.id  AND
 prodoptchoices.choiceid = choices.id AND 
 products.current = 'T' AND
 prodoptchoices.choiceid = 36230)
 ORDER by prodoptchoices.productoptionid;


---

Copy all choices from productoptionid 40953 to a new productoptionid 40954 (that I already entered into prodopt table)

INSERT into prodoptchoices ( pricedelta, productoptionid, choiceid, current)

Select 0,40954, choiceid,'T' 
from prodoptchoices
where prodoptchoices.productoptionid = 40953;

---

Show me each Sku's Ubuntu* choices to make sure all 4 are included

SELECT  products.sku, prodopts.id as prodoptid, choices.id as choiceid, prodopts.defaultchoiceid as default, products.baseprice, options.name as option, choices.name as choice, choices.cost, prodoptchoices.pricedelta  
from products, options, prodopts, choices, prodoptchoices 
WHERE 
 (prodopts.productid = products.id) AND
 (prodopts.optionid = options.id)  AND  
 (products.current = 'T') AND

 (prodoptchoices.productoptionid = prodopts.id)  AND
 (prodoptchoices.choiceid = choices.id) AND 
  (choices.name like 'Ubuntu Linux 8%') 
ORDER BY products.sku, choices.name ;


---

Print out all the 5.25in Bay choices (except tape drives)

SELECT  products.sku, prodopts.id, products.baseprice, 
options.name as option, prodopts.id as prodoptid, choices.name as choice, choices.cost, prodoptchoices.pricedelta  
from products, options, prodopts, choices, prodoptchoices 
WHERE 
 (prodopts.productid = products.id) AND
 products.current = 'T' AND
 (prodopts.optionid = options.id)  AND  
 (prodoptchoices.productoptionid = prodopts.id)  AND
 (prodoptchoices.choiceid = choices.id) AND 
 (options.name like '5.25%') AND 
 (choices.name NOT like 'Tape Drive%')
ORDER BY products.sku, options.name, prodopts.optionid, choices.cost;
'''

from pprint import pformat

lst = sqls.split ('\n---')

#print pformat (lst)
#print 'sqls:'
#y = 'sqls:\n'
y = ''
inx = 1

for entry in lst:
  y += '\n- model: sqls.sql\n'
  y += '\n  pk: %d\n' % inx
  inx += 1
  y += '\n  fields:\n'

  try:
    nam,sql = entry.strip('\n ').split ('\n\n',1)
    sql = '      ' + sql.replace ('\n\n','\n').replace ('\n','\n      ')
    nam = '      ' + nam.replace ('\n\n','\n').replace ('\n','\n      ')

    #print '  nam: >\n' + nam
    y += '\n    description: >\n' + nam + '\n'

    #print '  sql: |\n' + sql
    y += '\n    sql: |\n' + sql + '\n'
  except Exception, e:
    #print e, entry
    y+= '\nWhoa, error: ' + `e` + entry

print y

import yaml
d = yaml.load (y)

#print pformat (d)

