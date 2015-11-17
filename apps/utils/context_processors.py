"""
Joe's request processors that return dictionaries to be merged into a
template context. Each function takes the request object as its only parameter
and returns a dictionary to add to the context.

These are referenced from the setting TEMPLATE_CONTEXT_PROCESSORS and used by
RequestContext.
"""

from django.conf import settings as django_settings
from django.db.models import get_models, Manager
from django.utils.safestring import mark_safe

#from django.utils.functional import lazy

from quickpages.models import QuickSnippet


#### module globals

trace = 0


#### utility functions

def get_managers (model):
    '''
    Helper function to return the list of managers for a given model.

    Could be moved to top-level utils app
    '''
    managers = []

    for mgr in dir(model):
        try:
            if not mgr.startswith ('_') and isinstance (getattr (model, mgr), Manager):
                if trace: print model, mgr
                managers.append (mgr)
        except Exception, e:
            if trace: print model.__name__, e, mgr

    return managers


#### Context Processors

def settings (request):
    """
    Context processor that provides the full settings object.

    Other cp's only provide one little piece here or there, this gives you the whole thing.

    Since we can't check the context to ensure it's not there already before injecting, don't set
    for /files or /admin, to avoid stepping on conflicting 'settings' var set by django_bfm.
    """
    #print hasattr (request, 'settings'), request.REQUEST.get ('settings', None), request.META.get ('settings', None),
    #    return {}
    #nope: print request

    if request.path.startswith (('/files', '/admin')):  # collides with admin, django_bfm
        return {}

    return dict (settings = django_settings)


def models (request):
    '''
    Context processor that provides the database models for the apps in the project.

    Because the template mechanism calls the model class (since it's callable), the class itself can't be used directly in the tempalte,
    so this returns the primary Manager for the model, using the convention:

    <model name>_<manager name>

    eg, Customer_objects or Product_published_objects

    Note that managers which begin with an underscore, such as _default_manager and _base_manager are not included.
    '''

    if request.path.startswith (('/files', '/admin')):  # collides with admin, django_bfm
        return {}

    result = {}
    all_models = get_models()

    for model in all_models:
        if trace: print model

        managers = get_managers (model)

        for mgr in managers:
            result [model.__name__ + '_' + mgr] = getattr (model, mgr)

    return result


moved_to_quickpages='''
#### for Obdjects

class StringObject (unicode):
    pass

def _get_snippets():
    result = {}

    for obj in QuickSnippet.objects.published():
        s = StringObject (obj.body)
        s = mark_safe (s)
        s.object = obj
        result [obj.name] = s

    return result

#snippets = dict ([(name, mark_safe (body)) for name, body in Snippet.pub_objects.values_list ('name','body')])
#snippets = dict ([(obj.name, obj) for obj in Snippet.objects.published()])

snippets = _get_snippets()

def obdjects (request):
    if request.path.startswith (('/files', '/admin')):  # collides with admin, django_bfm
        return {}

    # jjw 1/1/13 commented out - confusing python interpreter into not using the global above when DEBUG is False!
    #if django_settings.DEBUG:
    #    #snippets = dict ([(obj.name, obj) for obj in Snippet.objects.published()])
    #    snippets = _get_snippets()

    return snippets
'''


#### Dynamic injection

later='''
# _registered = {}  # this doesn't work, different threads...

I could use the Process module, with a Manager

http://docs.python.org/library/multiprocessing.html

from django.core.cache import cache
from sys import maxint

def register (k,v):
    #global _registered
    print 'registering:', k
    # _registered = {}  # this doesn't work, different threads...
    cache.set(k, v, maxint)
    #_registered [k] = v
    #print _registered
    print cache.get(k)
    ..nope - need to marshal / serialze it.,

def registered (request):
    global _registered
    print _registered
    return _registered
'''

#### main, for testing

if __name__ == '__main__':
    models (None)
