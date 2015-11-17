7/31/12 JJW

Run two scripts from this dir, to import all Zope orders and lineitems:

../runscript.sh import_orders.py
../runscript.sh import_order_lineitems.py

in that order - That's it!


Notes 9/8/12:

The extract_order*csv.py files are cut/pasted into the Zope folders & run (called by the above) from there.


..Now working on importing mailing lists & users..