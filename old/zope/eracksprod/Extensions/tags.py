#__debug__ = 1  # for asserts - CAN'T DO ON 2.X PYTHON!

def tagimp (tg, args, kw={}):
  s = attrs = ''

  #return type (kw)

  for (k,v) in kw.items():
    attrs = attrs + ' %s="%s"' % (str(k), str(v))

  #if len (args) == 1 and len (args [0]) > 1:  # allow direct passing of lists & tuples
  #  args = args [0]
  
  #assert len (args) >= 1, 'len (args) >= 1'   # causing problems in checkout
  
  if type (args) == type ('string'):
    s = s + '<%s%s>%s</%s>\n' % (tg, attrs, args, tg)
  else:
    for arg in args:
      s = s + '<%s%s>%s</%s>\n' % (tg, attrs, arg, tg)

  return s

def tag1imp (tg, args, kw={}):  # args is not used right now, so there is no auto-iterate for this tag
  s = attrs = ''

  for (k,v) in kw.items():
    attrs = attrs + ' %s="%s"' % (str(k), str(v))
  
  #if args:
  #  assert len (args) == 1  # actually, could auto-iterate here
  #  args = args [0]
  #
  #return '<%s %s%s>\n' % (tg, args, attrs)

  if args:
    for arg in args:
      s = s + '<%s %s%s>\n' % (tg, arg, attrs)
  else:
    s = '<%s%s>\n' % (tg, attrs)

  return s


def tag (tg, *args, **kw):
  return tagimp (tg, args, kw)

def html (*args, **kw):
  return tagimp ('html', args, kw)  

def head (*args, **kw):
  return tagimp ('head', args, kw)  

def body (*args, **kw):
  return tagimp ('body', args, kw)  

def tr (*args, **kw):
  if not kw:
    kw={'valign':'left', 'halign':'left'}
  return tagimp ('tr', args, kw)  

def td (*args, **kw):
  return tagimp ('td', args, kw)  

def th (*args, **kw):
  return tagimp ('th', args, kw)  

def table (*args, **kw):
  return tagimp ('table', args, kw)

def button (*args, **kw):
  return tagimp ('button', args, kw)

def input (*args, **kw):
  if not kw:
    kw = {'type':'text'}
  return tag1imp ('input', args, kw)

def inputimg (*args, **kw):
  kw ['type'] = 'image'

  if args:
    s = ''
    for arg in args:
      if hasattr (arg, 'id'): 
        kw ['name'] = arg.id()
        kw ['src']  = arg.absolute_url()
      if hasattr (arg, 'height'): kw ['height'] = arg.height
      if hasattr (arg, 'width') : kw ['width']  = arg.width
      if hasattr (arg, 'title') : kw ['alt']  = arg.title
      if hasattr (arg, 'border'): kw ['border'] = arg.border
      #return `arg`
      s = s + tag1imp ('input', (), kw)
    return s
  else:
    return tag1imp ('input', (), kw)

def bold (s):
  return tagimp ('b', s)

def link (lnk, txt, **kw):
  if not kw.has_key ('href'):
    kw ['href'] = lnk
  return tagimp ('a', txt, kw)

def mailto (mto, **kw):
  if not kw.has_key ('href'):
    kw ['href'] = 'mailto:' + mto
  return tagimp ('a', mto, kw)

def font (*args, **kw):
  return tagimp ('font', args, kw)

def para (*args, **kw):
  return tagimp ('p', args, kw)

def option (*args, **kw):  # this tag expects a list of duples, ie: (value, desc) - name is in the select
  s = ''
  selected = ''
  
  if kw.has_key ('selected'):
    selected = str (kw ['selected'])
    del kw ['selected']
    
  for arg in args:
    for (val, desc) in arg:
      kw ['value'] = val
      
      if selected and str (val) == selected:
        tag = 'option selected'
      else:
        tag = 'option'

      s = s + tagimp (tag, [desc], kw)
  
  return s

def select (*args, **kw):
  return tagimp ('select', args, kw)
  
def textarea (*args, **kw):
  return tagimp ('textarea', args, kw)

def treo (*args, **kw):         # treo - tr even/odd rows in different color
  return tagimp ('treo', args, kw)

def sqlvar (*args, **kw):         
  if not kw:
    kw = {'type':'string'}
  return tag1imp ('dtml-sqlvar', args, kw)

def trtd (*args, **kw):
  s = ''
  for arg in args:
    s = s + apply (tr, [apply (td, [arg], kw)], kw)
  return s

  
if __name__ == "__main__":
  #print `option ( ( (1, 'one'), (2, 'two'), (3, 'three') ), selected=1)`
  print trtd (1,2,3, style=123)
  pass
