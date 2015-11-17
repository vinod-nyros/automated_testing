from pyjade.parser import Parser
#from pyjade.ext.html import Compiler  # straight HtmlCompiler
from pyjade.ext.django import Compiler  # django-templates-based

trace = 0

def jade2django (s, **kw):
  if s.startswith ('\n'):
    s = s [1:]
  p = Parser (s)
  if trace: print p
  block = p.parse()
  if trace: print block
  c = Compiler (block, **kw)  # pretty=True)  # **kw
  rslt = c.compile()  #.strip()
  if trace: print rslt
  return rslt

