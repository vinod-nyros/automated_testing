from string import find, join, split
from time import time, ctime

### util functions & classes

def iff (b,t,f):
  if b: return t
  else: return f

class Dict:
  def __init__(self, dict):
    self.__dict__ = dict

  def __getattr__ (self, a):
    if self.__dict__.has_key (a): return self.__dict__ [a]
    return ''

  def __getitem__ (self, i):
    return self.__getattr (i)


def hq (v, name='(Unknown name)', md={},       # html_quote
               character_entities=(
                       (('&'),    '&amp;'),
                       (('<'),    '&lt;' ),
                       (('>'),    '&gt;' ),
                       (('\213'), '&lt;' ),
                       (('\233'), '&gt;' ),
                       (('"'),    '&quot;'))): #"
        text=str(v)
        for re,name in character_entities:
            if find(text, re) >= 0: text=join(split(text,re),name)
        return text

def now():
  return ctime (time())
