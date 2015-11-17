# -*- coding: utf-8 -*-

from time import sleep

from django.http import HttpResponse, Http404
#from django.template import Template, Context, RequestContext
from django.contrib.auth.decorators import user_passes_test
from django.core.cache import cache
from django.shortcuts import render
from django.utils.safestring import mark_safe

from eracks.urls import urlpatterns

import django
from django.core.management import call_command


#### globals

trace = 0


#### Clear the cache

def clearcache (request):
    cache.clear()

    return render (request, 'base.html', dict (
        content = mark_safe ('<h1>Cache cleared</h1>'),
        request=request,
    ))

### collect static

def collect_static(request):
    call_command('collectstatic', verbosity=1, interactive=False, link=True)
    return render(request, 'base.html', dict(
        content = mark_safe('<h1>Collected all static files</h1>'),
        request=request,
        ))


#### Url View utility

@user_passes_test(lambda u: u.is_staff)  #@login_required
def urls (request):
    def show_url_patterns (urlpatterns, indent):  # , result):
        if trace:
            print
            print 'indent', indent
            print 'urlpatterns:', urlpatterns

        result = ''

        for u in urlpatterns:
            if hasattr (u, 'url_patterns'):
                # u.urlconf_name
                # 'accessories.urls'
                # u.urlconf_module
                # <module 'accessories.urls' from '/home/joe/eracksaccessories/accessories/urls.pyc'>
                #print 'nested url_patterns:', u.url_patterns, 'indent', indent
                result += '%s%s\n' % (' '*indent, u.regex.pattern)  # ' ' + u._callback_str +
                result += show_url_patterns (u.url_patterns, indent+2)  #, result)
            elif hasattr (u, '_callback_str'):
                result += '%s%s %s\n' % (' '*indent, u.regex.pattern, u._callback_str)
            elif hasattr (u, '_get_callback'):
                f = u._get_callback()
                if hasattr (f, '__module__') and hasattr (f, 'func_name'):
                    result += '%s%s %s %s\n' % (' '*indent, u.regex.pattern, f.__module__, f.func_name)
                else:
                    result += '%s%s Unknown callback: %s\n' % (' '*indent, u.regex.pattern, `f`)
                #except Exception, e:
                #    result += '%s%s Exception:%s %s\n' % (' '*indent, u.regex.pattern, e, f)  # ' ' + u._callback_str +
            else:
                result += '%s%s Unknown pattern: %s\n' % (' '*indent, u.regex.pattern, `u`)

                #print result
        return result

    patterns = sorted (urlpatterns, key=lambda x:x.regex.pattern)
    result = 'URLs:\n\n' + show_url_patterns (patterns, 0)
    return HttpResponse (result, content_type="text/plain")



#### refresh utility - hangs for a long time to facilitate auto-browser-refresh

def refresh (request):
    if not request.is_ajax():
        raise Http404

    #from time import sleep
    sleep (84000)  # a day or so
    return HttpResponse ('refreshing..')
