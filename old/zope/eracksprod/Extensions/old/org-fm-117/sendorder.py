#__debug__ = 1

import smtplib, os, sys, time  #, urllib

if __name__ != "__main__" and sys.modules.has_key ('ZServer'):  # we're in zope, only now import mymodules
  import mymodules
  log    = os.path.join (mymodules.varpath, 'sendorder.log')
  me     = os.path.join (mymodules.zopeextpath, 'sendorder.py')

python = sys.executable         #os.path.join (sys.exec_prefix, 'python')

template='''\
to: %s
from: %s
bcc: emails@eracks.net
subject: %s

%s'''

codetemplate='''
import sys, time, smtplib
sys.stderr = sys.stdout = open (%s, 'a', 1)
print '- - - - - sending order %%s - - - - -' %% time.ctime (time.time())      
server = smtplib.SMTP ('mail.swisa.org')
server.set_debuglevel(1)
server.sendmail (%s, %s, \'\'\'%s\'\'\')
server.quit()
sys.stderr.close()
'''


### unix sendorder - spawns self under unix

def uso (mto, mfrom, subj, msg):
  t = time.ctime (time.time())
  f = open (log + '.' + t, 'a', 1)
  f.write ('\n\n\n%s: in uso' % t)

  cmd = '%s "%s" "%s" "%s" "%s" "%s" "%s"&' % (python, me, mto, mfrom, subj, msg, log)
  f.write ('\n\n%s command: %s' % (t, cmd))
  r = os.system (cmd)
  f.write ('\n\n%s result: %s' % (t, r))
  f.close()


### old/test uso - not used

def uso2 (mto, mfrom, subj, msg):
  f = open (log, 'a', 1)
  f.write ('in uso2 at %s' % time.ctime (time.time()))

  mesg = template % (mto, mfrom, subj, msg)

  code = codetemplate % (log, mfrom, mto, mesg)
  cmd = '%s -c "%s" >>%s &' % (python, code, log)
  f.write (`cmd`)
  r = os.system (cmd)
  f.write (`r`)
  f.close()


### windoze sendorder - spawns self under wdoz

def wso (mto, mfrom, subj, msg):
  def q (s):
    return '"%s"' % s

  l = (python, q(me), q(mto), q(mfrom), q(subj), q(msg), q(log))
  return `l` + `os.spawnv (4, l[0], l)`  # `os.execv (l[0], l)`   # perhaps >> to the logfile, here?

# consts for spawnv:
#define P_WAIT    0 /* child runs separately, parent waits until exit */
#define P_NOWAIT  1 /* both concurrent -- not implemented */
#define P_OVERLAY 2 /* child replaces parent, parent no longer exists */
#define P_NOWAITO 3 /* ASYNCH,       toss RC    */
#define P_DETACH  4 /* DETACHED,     toss RC    */



### standalone sendorder, called from main in spawned task

def sendorder (mto, mfrom, subj, msg, log):
  mesg = template % (mto, mfrom, subj, msg)

  sys.stderr = sys.stdout = open (log, 'a', 1)
  print '\n\n- - - - - sending order %s - - - - -' % time.ctime (time.time())
       
  server = smtplib.SMTP ('mail.swisa.org')
    
  #if not inzope:
  server.set_debuglevel(1)
    
  #print mesg
  server.sendmail (mfrom, mto, mesg)
  server.quit()
  sys.stderr.close()


### async sendorder, called from zope, spawns copy of itself on appropriate platform

def asyncsendorder (mto, mfrom, subj, msg):
  if sys.platform == 'win32':
    return wso (mto, mfrom, subj, msg)
  else:
    return uso (mto, mfrom, subj, msg)


if __name__ == "__main__":
  args = sys.argv
  #uso2 ('to@eracks.com', 'from@eracks.com', 'subject', 'themessage')
  sendorder (args [1], args [2], args [3], args [4], args [5])

