# id is always first
columns = '''line order_id title sku product summary qty baseprice totprice notes weight shipper shipdate shipprice tracknum
serial serials details'''.split()

#nope, not in Zope:
#from types import ListType, TupleType

def qt (s):
    #if isinstance (s, (list, tuple)):
    #if isinstance (s, (ListType, TupleType)):
    #if same_type (s, (list, tuple)):
    #if isinstance (s, (type ([]), type (()))):
    if same_type (s, []) or same_type (s, ()):
        s = '|'.join (s)
    s = str(s)
    s = s.replace ('"', '\\"')
    s = s.replace (',','\,')
    return s

def checkfolder (fold, parent_id=None):
  id = fold.id

  if str (id).isdigit():
    if int(id) < 999:  # it's a lineitem
        line = id

        #print parent_id  # fold.PARENTS [0] nope fold.parent nope
        #for k,v in fold.propertyItems():
        #    print k, qt(v)

        props = dict ([(k,v) for k,v in fold.propertyItems()])
        print '%s, %s,' % (line, parent_id), ', '.join (['"%s"' % qt (props.get (k, '')) for k in columns [2:-1]]) + ', ',

        # now check we got all of them:
        for k in columns [2:-1] + ['index']:
            props.pop (k, '')

        if props:
            raise `props` + parent_id

        # now add details
        print '"%s"' % qt (str (dict ([(d.id(), d.title) for d in fold.objectValues ('DTML Document')]))),

        '''
        we don't need pricedelta, etc:
        id = d.id
        if callable (id):  id = id()

        pairs = ['additem (id=' + id]

        for k,v in d.propertyItems():
            pairs += ['%s="%s"' % (k,qt(v))]

        print ','.join (pairs), ')'
        '''

  # Recurse - (postorder traversal!)
  for f in fold.objectValues ('Folder'):
      result = checkfolder (f, id)
      if result:
          print result

  if printed:
      return printed


print '<pre>'
print ', '.join (columns)
print checkfolder (context.orders)  #  ['30487']),
return printed
