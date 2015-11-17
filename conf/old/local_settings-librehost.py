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
        ENGINE = 'django.db.backends.postgresql_psycopg2',		#, 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        NAME = 'eracksdb',             # Or path to database file if using sqlite3.
        USER = 'eracks',             # Not used with sqlite3.
        PASSWORD = 'Wav3lets9',         # Not used with sqlite3.
        # HOST = 'eracks.com',             # Set to empty string for localhost. Not used with sqlite3.
        # PORT = '5432',             # Set to empty string for default. Not used with sqlite3.
        HOST = '127.0.0.1',             # Set to empty string for localhost. Not used with sqlite3.
        PORT = '65432',             # Set to empty string for default. Not used with sqlite3.
    )
)

ROOT_URLCONF = 'django_eracks.urls'

# add dbtemplates loader 3/26/12 JJW
#TEMPLATE_LOADERS = (
#    'django.template.loaders.filesystem.Loader',  # load_template_source',
#    'django.template.loaders.app_directories.Loader',  # load_template_source',
##   'django.template.loaders.eggs.load_template_source',
#    'dbtemplates.loader.Loader',
#)

INSTALLED_APPS = (
    #'grapelli',
    #'filebrowser',
    'django.contrib.admindocs',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    #'django.contrib.staticfiles',
    'south',
    'debug_toolbar',
    'django_eracks.apps.legacy',
    'django_eracks.apps.sqls',
    'django_eracks.apps.quotes',
    'django_eracks.apps.customers',
    'django_eracks.apps.utils',
    'djide',
    #'dbtemplates',
    'aloha',
)


#### for DB Templates
#DBTEMPLATES_USE_CODEMIRROR = True
#DBTEMPLATES_MEDIA_PREFIX = '/static/dbtemplates/'


#### For Django Debug Toolbar
INTERNAL_IPS = ('127.0.0.1',)
