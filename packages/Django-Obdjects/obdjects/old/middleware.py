from django.conf import settings
#from django.contrib.sites.models import Site
from eracks.obdjects.models import Site

trace = 0

class RequestMiddleware:
  def process_request (self, req):
    #setreq (request)    #print req.META
    host = req.get_host()
    if trace: print 'MIDDLEWARE', host

    try:
      site = Site.objects.get(domain=host)
      settings.SITE_ID = site.id
      req.urlconf = site.urlconf
      req.site = site
      req.site_id = site.id # these all work, but don't show in list
      print host, site, settings.SITE_ID, req.urlconf, req.site, req.site_id
    except Exception, e:
      if trace: print 'EXCEPTION:', `e`
      #site = Site.objects.get_current()

    return

    # old try:
    if site.id > 3:
      settings.SITE_ID = site.id
      req.urlconf = 'eracks.multisites.urls'  # works!
      req.site = site
      req.site_id = site.id # these all work, but don't show in list
      print host, site, settings.SITE_ID, req.urlconf, req.site, req.site_id

      # be sure to put:
      # assert settings.SITE_ID == req.site_id
      # wherever you use this, until we've tested it EVERYWHERE - 
      # incl fcgi, wsgi, nginx, apache threadmodel, etc - apache processmodel should work OK


  def no_process_response (self, request, response):
    ses = getattr (request, 'session', None)
    if not ses: return response

    xtras = ses.get ('header_extras', None)
    if not xtras: return response

    # KLUGE ALERT:
    jslist = []
    csslist = []
    head = ''
    for k,v in xtras.items():
      if v == 'js':
        jslist += [k]
      elif v == 'css':
        csslist += [k]
      else:
        head += k
    head += jstags (jslist)
    head += csstags (csslist)
    response.content = response.content.replace ('</head>', '%s\n</head>' % head)
    del ses ['header_extras']
    return response
