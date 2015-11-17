import re
#import os
import inspect

#from inspect import isfunction, getmembers, ismethod, isclass #, getclasstree
#from copy import deepcopy
#from pprint import pformat
#from operator import isMappingType

#from django.http import HttpResponse
from django.shortcuts import render
from django.template import Template, RequestContext  # Context,
from django.template.loader import render_to_string, get_template, select_template
from django.template.defaultfilters import slugify
#from django.utils import simplejson as json
import json

#from eracks.obdjects.models import Snippet # , Site, Page


__doc__='''
- subclass generic template class(es)
- call returns as_view
- as_json returns json
- urls gens urls for both, to use with 'register' and include


ObdjectPage (
    as json
    as view
    def urls (self)
    urlpattern = r'^myurl/(some parm)/$'

...

    #also push v pull??  optional 'context' arg to override namespace, in case you want to pass in 'template'. eg
    # js (unsepcified), css, meta, head_top, head_bottom, base, js_bottom, js_top, define w/pyquery arg?

    #prepare() done on evry req for debug

    #template_engine?  template_name?

'''


#### globals

trace = 0



#### classes


class BaseObdject (object):
    def __init__ (self, *args, **kw):
        self._prepared = False
        self._name = ''

        self.args = args
        self.kw = kw


class CssObdject (BaseObdject):
    pass

class SassObdject (CssObdject):
    pass

class LessObdject (CssObdject):
    pass

class CompassObdject (CssObdject):
    pass

class StylusObdject (CssObdject):
    pass



class Obdject (object):
    def __init__ (self, template=None, context=None, urlregex=None, **kw):
        self.template = template
        self._prepared = False
        self._name = ''
        self.context = context if context else kw
        self.urlregex = urlregex

    def __call__ (self, request=None, *args, **kw):
        if request:
            if request.is_ajax():
                return json.encode (self.context)
            else:
                self.context ['request'] = request  # shouldn't need this
                return render (request, self.template, self.context, *args, **kw)
        else:  # wants string
            render_to_string (self.template, self.context, RequestContext (request))

    @property
    def my_name (self):
        if self._name: return self._name

        stack = inspect.stack()

        for framerec in stack [1:]:  # 1: skips the 'self' ref
            frame = framerec [0]
            if trace: print frame.f_code, frame.f_locals # frame.f_code.co_names   # frame.f_locals  # globals

            for k,v in frame.f_locals.iteritems():
                if id(v) == id (self) and k != 'self': # still might be more internal calls
                    if trace: print 'Found!', k
                    self._name = k
                    return k

        # old:
        #for k,v in globals().iteritems():  # need to get caller here with inspect
        #    if id (v) == id (self):
        #        self._name = k
        #        return k

        self._name = slugify (self.__class__.__name__)
        return self._name

    __name__ = my_name  # make DjDT happy


    def prepare (self):
        for member in dir (self):
            prep = getattr (member, 'prepare', None)
            if prep and callable (prep):
                prep()

    @property
    def urlpattern (self):
        return (self.urlregex or (r'^%s/$' % self.my_name), self)

