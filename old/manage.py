#!/usr/bin/env python
from django.core.management import execute_manager

# JJW 7/11/11 - goes in wsgi.py and manage.py
import os, sys
parent =  os.path.abspath(os.path.dirname(__file__))
def ensure_path (s): 
    if not s in sys.path: sys.path.append (s)
ensure_path (os.path.dirname (parent))
#ensure_path (parent)
ensure_path (os.path.join (parent, 'apps'))

# JJW 7/6/11
#import os, sys
if os.path.exists ('/var/lib/zope2.10/instance/eracksprod/lib/python'):
    ensure_path ('/var/lib/zope2.10/instance/eracksprod/lib/python')

try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings)
