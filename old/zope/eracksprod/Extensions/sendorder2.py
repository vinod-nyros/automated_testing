# This version 7/23/01 JJW differs fm sendorder (1) in that the headers 
# are assumed to be in the message itself, and are not passed in the parms
# there is therefore no need for the template, either.
#
# notes:
# 1) the top few lines of the msg itself contain the rest of the headers, whatever you want
# 2) sendorder2 prepends the first 3 lines, to, from, and cc, to the msg
# 3) the from address is always cced
#
# jjw 8/17/3 Add date to headers
# jjw 8/17/3 reduce config dependence, use myconfig.py for var
# jjw 7/24/10 use myconfig for mailhost, furhter debugging

#__debug__ = 1

import smtplib, os, sys, time, string
from myconfig import mailhost

### main (sendorder2) - spawned by uso/wso, calls sendorder

if __name__ == "__main__":
  args = sys.argv

  ### standalone sendorder, called from main in spawned task

  def sendorder (mto, mfrom, msg, log):
    #t = time.ctime (time.time())
    #t = time.strftime ('%Y-%m%d-%H.%M.%S')
    sys.stderr = sys.stdout = f = open (log, 'a', 1)  # % (t, mto, 'sndo'), 'a', 1)
    print '\n\n- - - - - sending mail to %s - - - - -' % mto

    server = smtplib.SMTP (mailhost)  # JJW 7/24/10 chged fm 'mail' # .swisa.org')  
    server.starttls()                 # SMTP_SSL not supported in py 2.4.x
    server.login ('relay','allow')

    #msg = 'To: %s\nFrom: %s\nCC: %s\nDate: %s\n%s' % (mto, mfrom, mfrom, t, msg)
    msg = 'To: %s\nFrom: %s\nCC: %s\n%s' % (mto, mfrom, mfrom, msg)
    mto = (mto, mfrom)

    server.set_debuglevel(1)
    sys.stderr = sys.stdout = f 
    server.sendmail (mfrom, mto, msg)
    server.quit()
    sys.stderr.flush()
    sys.stderr.close()
    sys.stdout.flush()
    sys.stdout.close()

  sendorder (args [1], args [2], args [3], args [4])

elif sys.modules.has_key ('ZServer'):   # we're in zope, set up envo for spawn
  varpath = 'var/maillog/'
  log    = os.path.join (varpath, 'sendorder_%s_%s.log')
  me     = 'Extensions/sendorder2.py' # __self__.__file__ doesn't work 5/22/05 JJW: __file__ # os.path.join (mymodules.zopeextpath, 'sendorder2.py')

python = sys.executable         #os.path.join (sys.exec_prefix, 'python')


### unix sendorder - spawns self under unix

def uso (mto, mfrom, msg):
  t = time.strftime ('%Y-%m%d-%H.%M.%S')
  l = log % (t, mto)
  f = open (l, 'a', 1)
  f.write ('\n\n- - - - - %s: in uso - - - - -' % t)

  msg = string.replace (msg, '\\"', '"')
  msg = string.replace (msg, '"', '\\"')

  cmd = '%s "%s" "%s" "%s" "%s" "%s"&' % (python, me, mto, mfrom, msg, l)
  f.write ('\n\n%s command: %s' % (t, cmd))
  r = os.system (cmd)
  f.write ('\n\n%s result: %s' % (t, r))
  f.flush()
  f.close()
  return 'Queued for sending'


### windoze sendorder - spawns self under wdoz

def wso (mto, mfrom, msg):
  def q (s):
    return '"%s"' % s

  l = (python, q(me), q(mto), q(mfrom), q(msg), q(log))
  return `l` + `os.spawnv (4, l[0], l)`  # `os.execv (l[0], l)`   # perhaps >> to the logfile, here?

# consts for spawnv:
#define P_WAIT    0 /* child runs separately, parent waits until exit */
#define P_NOWAIT  1 /* both concurrent -- not implemented */
#define P_OVERLAY 2 /* child replaces parent, parent no longer exists */
#define P_NOWAITO 3 /* ASYNCH,       toss RC    */
#define P_DETACH  4 /* DETACHED,     toss RC    */


### async sendorder, called from zope, spawns copy of itself on appropriate platform

def asyncsendorder (mto, mfrom, msg):
  if sys.platform == 'win32':
    return wso (mto, mfrom, msg)
  else:
    return uso (mto, mfrom, msg)
