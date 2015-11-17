# -*- coding: utf-8 -*-
# Django local_settings for eracks9 aka django_eracks project.

import os 

if 'APACHE_PID_FILE' in os.environ:  # Apache => production
    DEBUG = False
else:
    DEBUG = True

TEMPLATE_DEBUG = DEBUG

DATABASES = dict (
    default = dict (
        ENGINE = 'django.db.backends.postgresql_psycopg2', #, 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        NAME = 'eracksdb',             # Or path to database file if using sqlite3.
        USER = 'eracks',             # Not used with sqlite3.
        PASSWORD = 'Wav3lets9',         # Not used with sqlite3.
        # HOST = 'eracks.com',             # Set to empty string for localhost. Not used with sqlite3.
        PORT = '5432',             # Set to empty string for default. Not used with sqlite3.
        HOST = '127.0.0.1',             # Set to empty string for localhost. Not used with sqlite3.
        #PORT = '65432',             # Set to empty string for default. Not used with sqlite3.
    )
)

ROOT_URLCONF = 'django_eracks.urls'

INSTALLED_APPS = (
    'django.contrib.admindocs',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    #'south',
    'django_eracks.apps.legacy',
    'django_eracks.apps.sqls',
    'django_eracks.apps.quotes',
)
