# -*- coding: utf-8 -*-
# Django local_settings for eracks9 aka django_eracks project.

import os

if 'APACHE_PID_FILE' in os.environ:  # Apache => production
    DEBUG = False
else:
    DEBUG = True

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = dict (
    default = dict (
        ENGINE = 'django.db.backends.postgresql_psycopg2',        #, 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        NAME = 'eracksdb',              # Or path to database file if using sqlite3.
        USER = 'eracks',                # Not used with sqlite3.
        PASSWORD = 'Wav3lets9',         # Not used with sqlite3.
        # HOST = 'eracks.com',          # Set to empty string for localhost. Not used with sqlite3.
        # PORT = '5432',                # Set to empty string for default. Not used with sqlite3.
        HOST = '127.0.0.1',             # Set to empty string for localhost. Not used with sqlite3.
        PORT = '65432',                 # Set to empty string for default. Not used with sqlite3.
        OPTIONS = dict (
            autocommit=True,
        )
    )
)

ROOT_URLCONF = 'django_eracks.urls'

# add dbtemplates loader 3/26/12 JJW
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',  # load_template_source',
    'django.template.loaders.app_directories.Loader',  # load_template_source',
    #'django.template.loaders.eggs.load_template_source',
    #'dbtemplates.loader.Loader',
)

INSTALLED_APPS = (

    #### Admin & related admin apps which need to be before Django Admin apps
    #'grapelli',
    'filebrowser',  # must be before admin (note this is a non-grapelli fork)
    # Fluent dashboard & admin-tools
    'fluent_dashboard',
    'admin_tools',     # for staticfiles in Django 1.3
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',

    #### Django admin & related apps which should be before other projec apps
    'django.contrib.admindocs',
    'django.contrib.admin',
    'django.contrib.auth',
    #'django.contrib.formtools',  # for preview
    'django_browserid',  # Load after auth to monkey-patch it.
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',  # yuk
    'haystack',  # docs say it needs to be above your apps - see http://django-haystack.readthedocs.org/en/v1.2.7/tutorial.html

    #### internal apps:
    'home',
    'customers',
    'orders',
    #'legacy',
    'products',
    'bloglets',
    'utils',
    'catax',
    'sqls',
    'quotes',

    #### projects dir
    'django_stylus', # jjw
    'djgrid',
    'obdjects', # jjw
    'quickpages', # jjw

    #### 3rd party:
    'codemirror2',
    'south',
    'debug_toolbar',
    'djide',
    #'dbtemplates',  # retired 6/10/12 JJW
    'aloha',
    'coffeescript',
    'django_wysiwyg',
    #'django_bfm',
    'userena',
    'guardian', # required by userena
    #'apps',  # reposition Admin for snippets into quickpages
    #'filer',
    'easy_thumbnails',  # reqd by filer, userena
    'taggit',
    'taggit_templatetags',
    'social_auth',
    #'socialregistration',
    #'socialregistration.contrib.linkedin',
    'email_extras',
    #### Shop:
    #'plata',
    #'plata.contact', # Not strictly required (contact model can be exchanged)
    #'plata.discount',
    #'plata.payment',
    #'plata.shop',
)


#### for DB Templates
#DBTEMPLATES_USE_CODEMIRROR = True
#DBTEMPLATES_MEDIA_PREFIX = '/static/dbtemplates/'


#### For Django Debug Toolbar
INTERNAL_IPS = ('127.0.0.1',
    #'216.103.147.100',  # torrance hospital 6/15/12 :)  7/17/12 :-(
    '96.249.201.237',  # sheldon 6/16/12
    #'68.65.169.163',    # stanford 7/26/12
    #'68.65.169.138',    # stanford 7/26/12 - why is this different?
    )

#def custom_show_toolbar(request):
#    print 'AHA', request.get_host(), request.META ['REMOTE_ADDR']
#    return True # Always show toolbar, for example purposes only.

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    #'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
    #'EXTRA_SIGNALS': ['myproject.signals.MySignal'],
    #'HIDE_DJANGO_SQL': False,  # default: True
    #'TAG': 'div',  # default: body
    #'ENABLE_STACKTRACES' : True,
}

#### for django-wysiwyg - TODO: install CKEditor!
DJANGO_WYSIWYG_FLAVOR = 'ckeditor'
# The following editors are supported out of the box:
#
#    yui - The YAHOO editor.
#    yui_advanced - The YAHOO editor with more toolbar buttons.
#    ckeditor - The CKEditor, formerly known as FCKEditor
#
# It's also possible to add new editors, see extending django-wysiwyg


#### for django-filer - removed
#from filer.utils.loader import storage_factory
#FILER_IS_PUBLIC_DEFAULT = True
#FILER_STATICMEDIA_PREFIX = '/static/filer/'
#FILER_SUBJECT_LOCATION_IMAGE_DEBUG = True


#### for django-filebrowser (Bouke's fork, no grappelli!)
FILEBROWSER_DIRECTORY = ''


#### True => enable my js AUTORELOAD functionality, in base template
AUTORELOAD = False  # DEBUG


#### True => load the Aloha css/js in the base template - you stilll have to load the aloha tags in your template though
ALOHA = False  # DEBUG


#### For django.contrib.auth UserProfile & Userena
AUTH_PROFILE_MODULE = 'customers.UserenaProfile'

#### Userena, guardian, BrowserID, social_auth
USERENA_DEFAULT_PRIVACY = 'closed'  # 'registered' allows registered users to see each other, 'open' allows all to see all
USERENA_ACTIVATION_REQUIRED = False
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # move to end if using social_auth
    'django_browserid.auth.BrowserIDBackend',       # for django-browserid
    # Userena:
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    #socialregistration:
    #'socialregistration.contrib.linkedin.auth.LinkedInAuth',
    # social_auth:
    'social_auth.backends.contrib.linkedin.LinkedinBackend',  # no email!
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    #'social_auth.backends.google.GoogleOAuthBackend',
    #'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.google.GoogleBackend',
    #'social_auth.backends.yahoo.YahooBackend',
    'social_auth.backends.contrib.github.GithubBackend',
    'social_auth.backends.contrib.dropbox.DropboxBackend',
    #'django.contrib.auth.backends.ModelBackend',
)

if 0 and DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'mail.eracks.com'
    #EMAIL_PORT = 25
    EMAIL_HOST_USER = 'relay'
    EMAIL_HOST_PASSWORD = 'allow'
    EMAIL_USE_TLS = True

# for django-guardian
ANONYMOUS_USER_ID = -1

# for social_auth:
SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
SOCIAL_AUTH_ASSOCIATE_BY_MAIL = True
#Old:
#LINKEDIN_CONSUMER_KEY          = '20qhsfqxi4t3'
#LINKEDIN_CONSUMER_SECRET       = 'pYLru1MTqxAnQvmi'
LINKEDIN_CONSUMER_KEY           = 'zy6tydz4ot9r'
LINKEDIN_CONSUMER_SECRET        = 'NkNycVC9phkoG8ST'
LINKEDIN_EXTRA_DATA             = [('main-address','main-address'),('phone-numbers','phone-numbers'),('bound-account-types','bound-account-types')]  # [('email', 'email')]
LINKEDIN_EXTRA_FIELD_SELECTORS  = ['main-address','phone-numbers','bound-account-types']  # ['email']
FACEBOOK_APP_ID                 = '151775531612916'
FACEBOOK_API_SECRET             = 'b3e8d3c5d8ca159a63b06eb5a1bbf691'
FACEBOOK_EXTENDED_PERMISSIONS   = ['email']
FACEBOOK_EXTRA_DATA             = [('email', 'email')]
TWITTER_CONSUMER_KEY            =  'O7uvpmrWFm6ks54D7Kow'
TWITTER_CONSUMER_SECRET         = 'Bjh8KTrtYNdiDmdF1s2TwMYXK8sdk0isLHxf4rRbrY'
TWITTER_EXTENDED_PERMISSIONS    = ['email']
TWITTER_EXTRA_DATA              = [('email', 'email')]
GITHUB_APP_ID                   = '9e21e195c19e04c51e75'
GITHUB_API_SECRET               = '50b02ed8b3b0aaecd4b0801259eea5793cb77e17'
GITHUB_EXTENDED_PERMISSIONS     = ['email']
GITHUB_EXTRA_DATA               = [('email', 'email')]
DROPBOX_APP_ID                  = 'feokr5j5kctsmvw'
DROPBOX_API_SECRET              = '4lzeucdbluzqxs2'
#GOOGLE_SREG_EXTRA_DATA          = [('email', 'email')]
#GOOGLE_AX_EXTRA_DATA            = [('email', 'email')]
GOOGLE_OAUTH2_CLIENT_ID         = '137682524779.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET     = 'g0rihndQFstz7oHIDUieBYub'
#GOOGLE_OAUTH_EXTRA_SCOPE        = ['email']

# for socialregistration:
#LINKEDIN_CONSUMER_KEY        = 'zy6tydz4ot9r'
#LINKEDIN_CONSUMER_SECRET_KEY = 'NkNycVC9phkoG8ST'



#### for django-browserID - also inserted auth-backend, see above in the Userena settings
#SITE_URL = 'http://127.0.0.1:8000'

BROWSERID_CREATE_USER = True

def username(email):
    print 'In BrowserID callback:', email
    #return email # nope - can't use raw email, because userena can't deal with the @ on the reverse url
    from django.contrib.auth.models import User
    uname = email.split('@', 1)[0]
    existing = User.objects.filter (username__istartswith=uname).values_list ('username', flat=True)
    add_integer = 1

    # still a timing hole here...
    while uname in existing:
        uname = '%s%s' % (email.rsplit('@', 1)[0], add_integer)
        add_integer += 1

    return uname
    #nope: won't fit into 30 chars: joseph_dot_wolff_at_gmail_dot_com
    #return email.replace ('@', '_at_').replace ('www.','').replace('.','_dot_')
    # could use dot-com as the default, & remove:
    #return email.replace ('@', '_at_').replace ('www.','').replace ('.com','').replace('.','_dot_')  # .rsplit('@', 1)[0]
    # could also add a number, incrementally count up to an available one, or use a db seq/id

BROWSERID_USERNAME_ALGO = username
LOGIN_REDIRECT_URL = '/'


#### Haystack settings

# 1.2.x settings:
#HAYSTACK_SITECONF = 'django_eracks.conf.haystack'
#HAYSTACK_SEARCH_ENGINE = 'simple'
# 2.0.0 beta settings:
#HAYSTACK_CONNECTIONS = {
#    'default': {
#        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
#    },
#}
import os
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}


#### for plata - not used 7/12 JJW
#
#PLATA_SHOP_PRODUCT = 'products.Product'
#
#import logging, os
#import logging.handlers
#
#PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
#LOG_FILENAME = os.path.join(PROJECT_ROOT, 'log', 'plata.log')
#
#plata_logger = logging.getLogger('plata')
#plata_logger.setLevel(logging.DEBUG)
#plata_logging_handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=10*1024*1024, backupCount=15)
#plata_logging_formatter = logging.Formatter('%(asctime)s %(levelname)s:%(name)s:%(message)s')
#plata_logging_handler.setFormatter(plata_logging_formatter)
#plata_logger.addHandler(plata_logging_handler)


#### for testing 7/26/12 JJW
#DISABLE_TRANSACTION_MANAGEMENT  = True


#### Fluent Dashboard and django-admin-tools
ADMIN_TOOLS_INDEX_DASHBOARD = 'fluent_dashboard.dashboard.FluentIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'fluent_dashboard.dashboard.FluentAppIndexDashboard'
ADMIN_TOOLS_MENU = 'fluent_dashboard.menu.FluentMenu'

FLUENT_DASHBOARD_ICON_THEME = 'oxygen'

FLUENT_DASHBOARD_APP_ICONS = {
    'cms/page': 'internet-web-browser.png',
    'auth/user':  'system-users.png',
    'auth/group': 'resource-group.png',
    'sites/site': 'applications-internet.png',
    'google_analytics/analytics': 'view-statistics.png',
    'registration/registrationprofile': 'list-add-user.png',
    'customers/userenaprofile': 'list-add-user.png',
    # ...
}

FLUENT_DASHBOARD_DEFAULT_ICON = 'unknown.png'

from django.utils.translation import ugettext_lazy as _

FLUENT_DASHBOARD_APP_GROUPS = (
    #(_('CMS'), {
    #    'models': (
    #        '*cms*.*',
    #        'fiber.*',
    #    ),
    #    'module': 'CmsAppIconList',
    #    'collapsible': False,
    #}),
    #(_('Interactivity'), {
    #    'models': (
    #        'django.contrib.comments.*',
    #        'form_designer.*'
    #        'threadedcomments.*',
    #        'zinnia.*',
    #    ),
    #}),
    (_('Administration'), {
        'models': (
            'django.contrib.auth.*',
            'django.contrib.sites.*',
            '*Userena*',
            'google_analytics.*',
            'registration.*',
        ),
        #'module': 'AppIconList', # the default, apparently
        'collapsible': True,
    }),
    (_('Categories and Products'), {
        'models': (
            'product*',
        ),
        'module': 'AppList',
        'collapsible': True,
    }),
    (_('Orders and Customers'), {
        'models': (
            #'customers.*',
            'orders.*',
        ),
        'module': 'AppList',
        'collapsible': True,
    }),
    (_('Home Page'), {
        'models': (
            'home.*',
            'bloglets.*',
            'quickpages.*',
        ),
        'module': 'AppList',
        'collapsible': True,
    }),
    (_('Other Applications'), {
        'models': ('*',),
        'module': 'AppList',
        'collapsible': True,
    }),
)

#FLUENT_DASHBOARD_CMS_PAGE_MODEL = ('cms', 'page')
#FLUENT_DASHBOARD_CMS_APP_NAMES = (
#    '*cms*',  # wildcard match; DjangoCMS, FeinCMS
#    'fiber',  # Django-Fiber
#)
#FLUENT_DASHBOARD_CMS_MODEL_ORDER = {
#    'page': 1,
#    'object': 2,
#    'layout': 3,
#    'content': 4,
#    'file': 5,
#    'site': 99
#}


#### django-email_extras - gnupg-encrypted emails
# Boolean that controls whether the PGP encryption features are used. Defaults to True if EMAIL_EXTRAS_GNUPG_HOME is specified
#EMAIL_EXTRAS_USE_GNUPG
# String representing a custom location for the GNUPG keyring.
EMAIL_EXTRAS_GNUPG_HOME = '/home/sysadmin/.gnupg'
#EMAIL_EXTRAS_GNUPG_HOME = '/var/gnupg'
# Skip key validation and assume that used keys are always fully trusted.
EMAIL_EXTRAS_ALWAYS_TRUST_KEYS = True

