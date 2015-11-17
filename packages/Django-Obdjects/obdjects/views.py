import sys
#from time import ctime
from pprint import pformat

#from django.template import Context, Template
from django.http import HttpResponse
#from django.template.defaultfilters import slugify

from eracks.obdjects.minitags import pre #tr,td,a as link,p as para,ul,li,h1,h2,form,treo,table,tr,td,th,img,div,submit,hidden
#from eracks.obdjects.classes import WebPage, WebSnippet, js_tags
#from eracks.obdjects.jquery import JQueryMenu

trace = 1

def test (req):
  #s = pformat (sys.modules)
  #s = `dir (sys.modules.values()[2])`
  #m = sys.modules.values()[2]
  #for attr in ['Command', 'CommandError', 'LabelCommand', 'ProjectCommand', '__builtins__', '__doc__', '__file__', '__name__', 'copy_helper', 'os']:
  #  s += attr + ': ' + `getattr (m, attr)` + '\n'

  # GOAL:  to ensure unique modules, and that modifying settings.SITE_ID will always work!

  s = ''
  l = []
  mods = sys.modules.values()
  for m in mods:
    if m and hasattr (m, '__file__'):
      s += m.__name__ + ': ' +  m.__file__ + '\n'   # __doc__ - match that, too!
      l += [m.__name__]

  l.sort()
  s = pformat (l)
  return HttpResponse (s + '\n\n\n' + pformat (req), content_type='text/plain')
  #return HttpResponse (pre (pformat (req)))
