# -*- coding: utf-8 -*-

import re
import inspect
import os
import shlex
import subprocess

from distutils.dep_util import newer

from django.template.base import Template, RequestContext  # Library, Node
from django.conf import settings


try:
    from shpaml.shpaml import convert_text
except:
    from shpaml import convert_text


#from django_stylus.templatetags.stylus import compileit

#from BeautifulSoup import BeautifulSoup


#### Globals

trace = 0
trace_save = 0

me = os.path.abspath (__file__ [:-1] if __file__.endswith ('c') else __file__)

if trace: print 'TEMPLATES MODULE', me


#### Utility functions

def remove_leading_spaces (s):
    def indent (line):
        return s.find (s.strip ())

    assert not '\t' in s, "String must not contain tabs"

    lines = s.splitlines()

    indent = max (indent (l) for l in lines)
    new_lines = []

    for l in lines:  # should use tokenize, here - see tabnanny source
        new_lines.append (l [indent:])

    return '\n'.join (new_lines)


def get_source_fname(source):
    if os.path.isfile (source):
        return source

    stack = inspect.stack()
    foundit = False

    for frame in stack:
        f = frame [0]
        m = inspect.getmodule (f)
        c = f.f_code
        if trace: print f.f_code, m, m.__name__, c.co_argcount, c.co_varnames, c.co_filename

        if foundit and os.path.abspath (c.co_filename) != me:  # 1st one after us
            if trace: print 'Returning the (next) one:', os.path.abspath (c.co_filename), c.co_argcount, c.co_varnames, me
            return os.path.abspath (c.co_filename)

        if c.co_argcount > 0 and  'source' in c.co_varnames:
            if trace: print 'found - next one after me:', c.co_filename, c.co_argcount, c.co_varnames
            foundit = True

    raise 'No source'


def get_app_dir():
    apps = settings.INSTALLED_APPS [:]
    apps = [app.split ('.') [-1] for app in apps if not app.startswith (('django.', 'obdjects'))]

    stack = inspect.stack()

    for frame in stack:
        f = frame [0]
        m = inspect.getmodule (f)
        if trace: print m, m.__name__

        modname = m.__name__

        if '.' in modname:
            modname = modname.split ('.') [0]

        if modname in apps:
            if trace: print 'Found it:', modname, os.path.dirname (m.__file__)
            return os.path.dirname (m.__file__)

    return '.'  # fall back to current dir if not found


# now using distutils.dep_util.newer
#def is_newer (f1, f2):
#    print os.stat (__file__).st_mtime
#    print os.path.getmtime (__file__)
#    print datetime.fromtimestamp (os.stat (__file__).st_mtime)


def compile_coffee (source):
    args = shlex.split("%s " % getattr (settings, 'COFFEESCRIPT_EXECUTABLE', 'coffee -sc'))

    p = subprocess.Popen (args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, errors = p.communicate(source.encode("utf-8"))

    if trace:
        print out, errors

    out = out.strip()

    if out:
        return out.decode("utf-8")
    elif errors:
        return errors.decode("utf-8")  # maybe raise an exception here?

    return u"Unknown error"




#### New classes / experiment: template w/Destination, to create fs template file, and trigger reload

class AbcTemplate (object):  # should inherit fm minimal ABC with Prepare()
    def __init__ (self, source, destination=None, compile_if_newer=None):
        self.source = remove_leading_spaces (source)
        self.source_fname = compile_if_newer or get_source_fname (source)
        self.destination = destination
        self.compile()
        if destination:
            self.save()

    def compile (self):
        raise 'Abstract Base Class - must use descendant class!'

    def prepare (self):
        raise 'Abstract Base Class - must use descendant class!'

    def save (self):
        if self.destination:
            dest = self.destination

            if not dest.startswith ('/'):  # if it's relative, put it in this app's templates
                app_dir = get_app_dir()

                try:
                    os.makedirs (os.path.join (app_dir, self.subdirs))
                except os.error, e:
                    if trace: print e

                dest = os.path.join (app_dir, self.subdirs, dest)

            if newer (self.source_fname, dest):
                if trace: print self.source_fname, 'newer than', dest
                if trace_save: print 'Saving to:', dest
                f = open (dest, 'w')
                f.write (self.template_text)
                f.close()
        else:
            raise "No destination set"

    #def render


class MinamlTemplate (AbcTemplate):  # should inherit fm minimal ABC with Prepare()
    subdirs = 'templates'

    def compile (self):
        try:
            if trace_save: print 'compiling', self.source_fname, 'to', self.destination
            self.template_text = convert_text (self.source)
            #print self.template_text
        except Exception, e:
            print e
            raise e

    def prepare (self):
        self.template = Template (self.template_text)
        return self.template


#class StylusTemplate (AbcTemplate):
#    subdirs = 'static/css'
#
#    def compile (self):
#        self.template_text = compileit (self.source)
#
#    def prepare (self):
#        return self.template_text


class CoffeescriptTemplate (AbcTemplate):
    subdirs = 'static/js'

    def compile (self):
        self.template_text = compile_coffee (self.source)

    def prepare (self):
        return self.template_text


removed_041815_JJW='''
#### Earlier template class(es):

# Name Inspired by the Stone IPA @ Sauce, Gough st, SF CA 11/28/08 - PumpkinSoup?!
class StoneSoupTemplate (BeautifulSoup):  # MlTemplate?
  def __init__ (self, src=None, path=None):
    if path: src = file (path).read()
    src = src.replace('%','%%')
    BeautifulSoup.__init__ (self, src)

  def ids (self, id_or_regex=re.compile(".*")):
    lst = self.findAll (id=id_or_regex)
    return lst

  def id (self, id_to_find):
    lst = self.ids (id_to_find)
    assert len (lst) in (1,0)
    if lst: return lst [0]

  def replaceIds (self, **kw): #def replaceInnerHtml (**kw):
    #if trace: print 'REPLACE IDS', kw.items()
    for k,v in kw.items():
      for id in self.ids (k):
        if trace: print 'REPLACING:', k, v #len (v)
        id.contents = []
        id.append (v)
    return self

  render = replaceIds  # cosmetic, for now

  def prepare (self, ids):  # change to 'compile'!
    if trace: print 'PREPARE SOUP', ids
    if not self.head:
      self.html.insert (0, Tag (self, 'head'))

    if 'base' in ids: # set up base tag - get from request, at render/call-time
      ids.remove ('base')
      if self.base:
        self.base ['href'] = '%(base)s'
      else:
        self.head.insert (0, '<base href="%(base)s" />')

    if 'title' in ids:
      ids.remove ('title')
      if self.title:
        self.title.contents = '%(title)s'
      else:
        self.head.insert (1, '<title>%(title)s</title>')

    # if 'meta' in ids:  # need to enh to deal with meta kw, meta desc, etc

    if 'header_extras' in ids:
      ids.remove ('header_extras')
      self.head.append ('%(header_extras)s')
      # bsoup 3.04 requires this:
      # self.head.insert (99,'%(header_extras)s')
      #print self.head

    if 'footer_extras' in ids:
      ids.remove ('footer_extras')
      self.body.append ('%(footer_extras)s')

    kw = dict ([(id, '%(' + id + ')s') for id in ids])

    # could do it this way:
    #for k in 'doctype base title meta header_extras footer_extras'.split():
    #  if k in kw:
    #    v = kw.pop (k)

    self.replaceIds (**kw)
'''


#### main - for in-place testing

from datetime import datetime

if __name__ == '__main__':
    #print os.stat (__file__).st_mtime
    print datetime.fromtimestamp (os.stat ('./templates.py').st_mtime)

    my_cs_tester = CoffeescriptTemplate ('''\
        console.log "calling refresh"

        $.ajax '/utils/refresh',
            type: 'GET'
            timeout: 60000000
            dataType: 'html'
            error: (jqXHR, textStatus, errorThrown) ->
                console.log "AJAX Error!: #{textStatus}"
                console.log setTimeout("console.log('reloading...');location.reload(true)", 2000)
                console.log "After setTimeout!"
            success: (data, textStatus, jqXHR) ->
                console.log "Successful AJAX call: #{data}"
        ''',
        destination = 'mytest.js'
    )

