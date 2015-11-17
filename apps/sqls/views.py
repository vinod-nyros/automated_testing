import re

from django.db import connection, transaction, IntegrityError, DatabaseError, ProgrammingError #backend
# django bug: no ProgrammingError per dbapi spec / pep 249
#from django.db.utils import DatabaseError, DatabaseErrorWrapper, ProgrammingError
from django.contrib.auth.decorators import login_required, user_passes_test
#from django.utils.encoding import smart_str, smart_unicode
from django.http import HttpResponse

from minitags import table, tr, td, th, h2, h3, pre #, p as para

trace = 0


@user_passes_test(lambda u: u.is_superuser)
@login_required  # arbitrary sql!
def do_sql (req) : #, sql):
  sql = req.REQUEST.get('sql')
  parms = req.REQUEST.getlist('parms[]')  # add [] - new 1/4/15 JJW on django17
  updates = req.REQUEST.get('updates') == 'true'
  cursor = connection.cursor()
  cursor.name = 'MyName'
  content = h3('Updating DB', style='color:red') if updates else h3('Not updating DB', style='color:green')

  if trace: print 'UPDATES:', updates, 'parms:', parms, 'req:', req

  if not parms and '%' in sql:
    sql = sql.replace ('%','%%')
  elif parms and '%' in sql:
    sql = re.sub (r'%([^s\(])', r'%%\1', sql)  #  escape all %'s except %s and %(..

  if '%(' in sql:
    parms = dict ([('parm' + `x+1`, p) for x,p in enumerate(parms)])
  else:
    parms = [p for p in parms if p]  # lose the '' entries
    #parms = [[int(i) for i in p.split(',')] for p in req.REQUEST.getlist('parms') if p]  # lose the '' entries
    #parms = [p.split(',') for p in req.REQUEST.getlist('parms') if p]  # lose the '' entries

  if trace: print '\nparms:', parms, '\nsql:', sql, '\n'

  # TEST: todo: smartly handle % and %s with parms, use %(.. to set parms to dict..
  # INVERT: todo: 'updates' bool, 'many' bool for lists of ids in parms, or smartly set on presence of ','
  # todo: split on ';' and use executescript if >1

  #if len ([s for s in sql.split (';') if s.strip()]) > 1:
  #  cursor.executescript(sql, parms)
  #else:

  try:
    ex = cursor.execute(sql, parms)
  except ProgrammingError, e:
    content += h2 ('SQL Programming Error: %s', e)

  rowcount = cursor.rowcount
  lastid = cursor.lastrowid
  desc = cursor.description
  #rows = cursor.fetchone() if rowcount == 1 else cursor.fetchall()  nope

  try:
    rows = cursor.fetchall()

    columns = [d [0] for d in cursor.description] # name,type_code,display_size,internal_size,precision,scale,null_ok
    column_range = range (len (columns))

    header = th (['row'] + columns)
    tbody = []

    for rowx, row in enumerate (rows):
      tbody += [td ([rowx] + [row [colx] for colx in column_range])]

    content += h2 ('%s result row%s returned' % (len(rows), '' if len(rows)==1 else 's'))  # could use cursor.rowcount
    content += table (tr ([header]) + tr (tbody))

  except DatabaseError, e:
    content += h2 ('(No results returned)')
  #Trying to catch except database related errors here
  except:
    content += h2 ('(No results returned)')

  if hasattr (cursor, 'query'):
    content += h3 ('SQL Performed:') + pre (cursor.query)  #_executed)

  if hasattr (cursor, 'rowcount') and cursor.rowcount:
    content += h3 ('Cursor row count:' + `cursor.rowcount`)

  if hasattr (cursor, 'messages'):
    for message in cursor.messages:
      content += h3 ('Cursor message: ' + message)

  if hasattr (connection, 'messages'):
    for message in connection.messages:
      content += h3 ('Connection message: ' + message)

  if hasattr (cursor, 'lastrowid'):
    content += h3 ('Last row ID: ' + `cursor.lastrowid`)

  if updates:
    cursor.connection.commit()
  else:
    cursor.connection.rollback()

  return  HttpResponse (content)
  #return  HttpResponse (`len (rows)`)

