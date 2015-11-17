# This version 7/23/01 JJW differs fm sendorder (1) in that the headers 
# are assumed to be in the message itself, and are not passed in the parms
# there is therefore no need for the template, either.
#
# notes:
# 1) the top few lines of the msg itself contain the rest of the headers, whatever you want
# 2) sendorder2 prepends the first 3 lines, to, from, and cc, to the msg
# 3) the from address is always cced

#__debug__ = 1

import smtplib, os, sys, time, string


### main (sendorder2) - spawned by uso/wso, calls sendorder

if __name__ == "__main__":
  args = sys.argv


  ### standalone sendorder, called from main in spawned task

  def sendorder (mto, mfrom, msg, log):
    t = time.ctime (time.time())
    sys.stderr = sys.stdout = open (log % ('send', t), 'a', 1)
    print '\n\n- - - - - sending order %s - - - - -' % t
       
    server = smtplib.SMTP ('mail.swisa.org')    
  
    msg = 'To: %s\nFrom: %s\nCC: %s\n%s' % (mto, mfrom, mfrom, msg)
    mto = (mto, mfrom)

    server.set_debuglevel(1)
    server.sendmail (mfrom, mto, msg)
    server.quit()
    sys.stderr.flush()
    sys.stderr.close()

  sendorder (args [1], args [2], args [3], args [4])

elif sys.modules.has_key ('ZServer'):   # we're in zope, only now import mymodules
  import mymodules
  log    = os.path.join (mymodules.varpath, 'sendorder2.%s.%s.log')
  me     = os.path.join (mymodules.zopeextpath, 'sendorder2.py')

python = sys.executable         #os.path.join (sys.exec_prefix, 'python')


### unix sendorder - spawns self under unix

def uso (mto, mfrom, msg):
  t = time.ctime (time.time())
  f = open (log % ('uso', t), 'a', 1)
  f.write ('\n\n\n%s: in uso' % t)

  msg = string.replace (msg, '\\"', '"')
  msg = string.replace (msg, '"', '\\"')

  cmd = '%s "%s" "%s" "%s" "%s" "%s"&' % (python, me, mto, mfrom, msg, log)
  f.write ('\n\n%s command: %s' % (t, cmd))
  r = os.system (cmd)
  f.write ('\n\n%s result: %s' % (t, r))
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

