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
#from djgrid.resources import GridResource
#class Resource(GridResource):
#    class Meta:
#        register = [
#            ['auth','user'],
#            ['orders','importedorder'],
#        ]
#resource = Resource()


urlpatterns = patterns('',
    (r'^admin/filebrowser/', include(site.urls)),
    (r'^grappelli/', include('grappelli.urls')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$', 'userena.views.signin', name='userena_signin'),

    #Email signup box
    url(r'^accounts/signup/$', 'home.views.user_signup', name='user_signup'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        { 'next_page': '/', 'template_name': 'userena/signout.html'}, name='userena_signout'),

    (r'^accounts/', include('userena.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    # (r'', include('social_auth.urls')), #commenting this to use python-social-auth
    #url(r'^social/', include('socialregistration.urls', namespace = 'socialregistration')),

    # out temporarily, migrate to https://github.com/ntucker/django-aloha-edit - JJW ~Oct 2014
    #(r'^aloha/', include('aloha.urls')),

    # for djgrid
    #(r'^', include(resource.urls)),

    # 3rd-party
    #url(r'^select2/', include('django_select2.urls')),
    (r'^admin/webshell/', include('webshell.urls')),
    # JJW 10/21/14 new 0.11 browserID must have blank regex per docs
    #(r'^browserid/', include('django_browserid.urls')),
    (r'', include('django_browserid.urls')),

    # for changeable themes, used by my new theme eng 4/15 JJW
    #url(r'^themes/', include('themes.urls')),

    # eRacks apps
    (r'^quotes/',    include('quotes.urls')),
    (r'^customers/', include('customers.urls')),
    (r'^djide/',     include('djide.urls')),
    (r'^utils/',     include('apps.utils.urls')),
    (r'^',           include('home.urls')),
    (r'^',           include('orders.urls')),
    (r'^products/',  include('products.urls')),
    (r'',            include('sqls.urls')),
    (r'^search/',    include('haystack.urls')),

    #(r'^$', include('home.views')),
    #url(r'^products_sitemap\.xml$', sitemap,{'sitemaps': sitemaps},
    #    name='django.contrib.sitemaps.views.sitemap'),
    #url(r'^all_sitemap\.xml$', sitemap, {'sitemaps': sitemaps1},
    #    name='django.contrib.sitemaps.views.sitemap'),
)


if settings.DEBUG:
    media_dict = {'document_root': settings.MEDIA_ROOT, 'show_indexes': True }
    static_dict = {'document_root': settings.STATIC_ROOT, 'show_indexes': True }

    urlpatterns += patterns('',
        (r'', include ('stheme.urls')),  # theme prefix for static files
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', media_dict),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', static_dict),
        # This next one is necessary because the StaticFilesHandler (in the lower wsgi layer) overrides the show_indexes setting for STATIC_URLs - JJW
        (r'^static2/(?P<path>.*)$', 'django.views.static.serve', static_dict),
        (r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT + '/js' }),
        (r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT + '/css' }),
        (r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT + '/images', 'show_indexes': True }),
        (r'^assets/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT + '/assets', 'show_indexes': True }),
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
