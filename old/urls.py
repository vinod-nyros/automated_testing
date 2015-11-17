# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns, include
from django.conf import settings
from django.http import HttpResponse

from filebrowser.sites import site

from django.contrib import admin
admin.autodiscover()

#import haystack
#haystack.autodiscover()

# http://django-jquery-grid-admin.readthedocs.org/en/latest/overview.html
from djgrid.resources import GridResource
class Resource(GridResource):
    class Meta:
        register = [
            ['auth','user'],
            ['orders','importedorder'],
        ]
resource = Resource()


urlpatterns = patterns('',
    (r'^admin/filebrowser/', include(site.urls)),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$', 'userena.views.signin', name='userena_signin'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        { 'next_page': '/', 'template_name': 'userena/signout.html'}, name='userena_signout'),

    (r'^accounts/', include('userena.urls')),
    (r'', include('social_auth.urls')),
    #url(r'^social/', include('socialregistration.urls', namespace = 'socialregistration')),

    # why doesn't this usurp all the urls?
    #(r'', include('django_eracks.apps.sqls.urls')),

    # for djgrid
    (r'^', include(resource.urls)),

    # for fluent_dashbaord and django-admin-tools
    (r'^admin_tools/', include('admin_tools.urls')),

    (r'^quotes/', include('quotes.urls')),
    (r'^customers/', include('customers.urls')),

    (r'^djide/', include('djide.urls')),
    (r'^aloha/', include('aloha.urls')),
    (r'^utils/', include('utils.urls')),
    #(r'^',       include('home.urls')),
    (r'^',       include('orders.urls')),
    (r'^products/', include('products.urls')),

    #(r'^files/', include('django_bfm.urls')),
    #(r'^', include('filer.server.urls')),
    (r'^browserid/', include('django_browserid.urls')),
    (r'^search/', include('haystack.urls')),

    (r'^$', include('home.views')),
)

if settings.DEBUG:
    media_dict = {'document_root': settings.MEDIA_ROOT, 'show_indexes': True }
    static_dict = {'document_root': settings.STATIC_ROOT, 'show_indexes': True }

    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', media_dict),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', static_dict),
        # This next one is necessary because the StaticFilesHandler (in the lower wsgi layer) overrides the show_indexes setting for STATIC_URLs - JJW
        (r'^static2/(?P<path>.*)$', 'django.views.static.serve', static_dict),
        (r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT + '/js' }),
        (r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT + '/css' }),
        (r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT + '/images', 'show_indexes': True }),
        (r'^stylesheets/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT + '/stylesheets' }),
        (r'^javascripts/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT + '/javascripts' }),
        (r'^favicon.ico/*$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT + '/images', 'path': 'favicon.ico' }),
        (r'^packages/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.PROJECT_ROOT + '/packages', 'show_indexes': True }),
    )

    #from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    #urlpatterns += staticfiles_urlpatterns()


out = ''' move to apache conf, along with humans.txt JJW 1/29/13
    # no robots for now 4/20/11 JJW
    # JJW upd 1/29/13 separate debug/prod robots
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
    #(r'^robots\.txt$', direct_to_template,  {'template': 'robots.txt', 'mimetype': 'text/plain'}),
else:
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nAllow: /", mimetype="text/plain")),
'''

### Dynamic DB-based QuickPages: in general, this section should be last, since it will match any pattern..

urlpatterns += patterns ('quickpages.views',
    (r'^(?P<slug>.*)/$', 'quickpage'),
)
