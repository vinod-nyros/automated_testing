import os, sys

# nonportable, not recommended, but effective - writes appear in Apache err log - JJW.
sys.stdout = sys.stderr

# JJW 7/11/11 - goes in wsgi.py and manage.py
parent =  os.path.abspath(os.path.dirname(__file__))
def ensure_path (s): 
    if not s in sys.path: sys.path.append (s)
ensure_path (os.path.dirname (parent))
ensure_path (parent)
ensure_path (os.path.join (parent, 'apps'))
# sys.path.append ('/home/joe') do we need the home dir in the path?! lame, but yes - so django_proj.settings and django_proj.urls are unambiguous
#sys.path.append ('/home/joe/eracks/apps')

os.environ['DJANGO_SETTINGS_MODULE'] = 'django_eracks.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
