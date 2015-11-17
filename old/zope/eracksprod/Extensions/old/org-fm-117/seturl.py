import string, sys

seturlrev = 1

hostmap = \
{ 'eracks': 'eRacks',
  'eracs' : 'eRacks.dev',
  'eraqs' : 'eRacks',
  'raqster' : 'eRacks',
  'emba15' : 'emba15'
}
  

def handleVia (self, req, via): 
  # parse via, which is <http ver> <domain:port>, ie:  "1.1 eraqs.org:8080"  

  err = result = ''

  lst = string.split (via, ' ')

  #req ['handleVia'] = str (locals())
  
  #if len (lst) == 2:
  #  (vers, host) = lst
  #else:
  #  raise Exception ('Improperly formed HTTP_VIA: ' + via)
  #
  # the above commented out 1/2/02 JJW due to LPA CFO unable 
  # to access, due to munged VIA header!

  host = string.lower (lst [-1])  # so try this instead


  #req ['handleVia2'] = str (locals())

  lst = string.split (host, ':')

  if len (lst) == 2:
    host, port = lst
  elif len (lst) == 1:
    host = lst [0]
    if string.find (host, 'securepages') >= 0:  # new for apache 1326 - no http(s) or :port
      port = '443'
    else:
      port = None
  else:
    raise Exception ('Invalid VIA_HTTP header from Apache')

  if port and port [-3:] == '443':
    prot = 'https'
  else:
    prot = 'http'
    port = '80'

  parts = string.split (host, '.') 

  if parts [0] == 'www':  
    site = parts [1]
  else:
    site = parts [0]

  #req ['handleVia3'] = 'host %s, site %s, hostmap %s' % (host, site, hostmap)

  # at this point we should have the site for the top level directory, ie eracks, eraqs, etc

  tldir = 'eRacks'

  if hostmap.has_key (site):
    tldir = hostmap [site]
  else:
    req ['err3'] = 'Unknown hostname: ' + host
    #raise Exception ('Unknown hostname: ' + host)

  req ['oldsteps'] = `req.steps`

  if len (req.steps) > 0 and tldir == req.steps [0]:
    del req.steps [0]

  req ['newsteps'] = `req.steps`
  req ['seturlrev'] = seturlrev
  #req ['oldreq'] = `req`

  #if tldir != req.steps [0]:
    #raise Exception ('mismatched top level dir: %s (%s)' % (tldir, req.steps [0]))
    #err = 'Mismatched top level dir: %s (%s)' % (tldir, req.steps [0])

  result = req.setServerURL (prot, host, port)  # also resets URLs with steps
  
  #req.steps.insert (0, tldir);
  #req ['handleVia4'] = str (locals())
  req ['setServerURLResult'] = result

  return 'steps: %s\nURL: %s\nVia: %s\nerr: %s\nresult: %s' % (`req.steps`, req.URL, via, err, result)


def handleSiteroot (self, req):
  #port = string.split (req.SERVER_URL, ':')
  #
  #if len (port) > 1 and port [-1] [-3:] == '080':
  #  return 'SiteRoot ignored in mgt mode!'

  lst = string.split (self.SiteRoot.base, ':')

  result = 'SiteRoot: ' + `lst`

  if len (lst) == 3:
    prot, host, port = lst
  elif len (lst) == 2:
    (prot, host) = lst
    port = None
  elif len (lst) == 1:
    prot = 'http'
    host = lst [0]
    port = None
  else:
    raise Exception ('Invalid SiteRoot base: ' + `lst`)
    
  if host [0:2] == '//': host = host [2:]  
    
  print req.setServerURL (prot, host, port)
  print req.setVirtualRoot (self.SiteRoot.path)
  print req.URL
  return result + '\n' + req.URL 


def seturl (self):
  req = self.REQUEST


  ### check for HTTP_VIA header and change URL accordingly..

  via = req.get_header ('HTTP_VIA')
  
  if via:
    return handleVia (self, req, via)
 

  ### check for SiteRoot, mimic siteroot behaviour if found, since AccessRules seem to override SiteRoots.

  #if hasattr (self, 'SiteRoot'):  
  #  return handleSiteroot (self, req)


  return 'no HTTP_VIA or SiteRoot'

