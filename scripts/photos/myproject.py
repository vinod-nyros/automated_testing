# myproject.py - sets py & dj parms to run script by being imported

#import datetime
import sys, os

#from pprint import pprint
#from collections import OrderedDict

# nope, its in the eracks subdir...
#while not 'settings.py' in  os.listdir ('.') and os.getcwd() != '/':
#  os.chdir ('..')
#
#print os.getcwd()

# Find root based on presence of 'eracks11' - could find based on .gitignore, .svnignore, README, etc

mynodes = __file__.split ('/')
root = '/'.join (mynodes [:mynodes.index ('eracks11') +1])

sys.path.insert (0, root)
sys.path.insert (0, root + '/apps')
os.environ ['DJANGO_SETTINGS_MODULE'] = 'eracks.settings'  #root + '/eracks/settings.py'

from django.conf import settings

# for 1.7: http://stackoverflow.com/questions/25537905/django-1-7-throws-django-core-exceptions-appregistrynotready-models-arent-load
import django
django.setup()

