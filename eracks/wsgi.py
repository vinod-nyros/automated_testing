"""
WSGI config for eracks project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os

# JJW upd 10/19/14, org 7/11/11 - goes in wsgi.py and manage.py
import sys
pparent =  os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
def ensure_path (s):
    if not s in sys.path: sys.path.append (s)
#ensure_path (os.path.dirname (parent))
#ensure_path (parent)
ensure_path (os.path.join (pparent, 'apps'))
#print sys.path


# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "eracks.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eracks.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
