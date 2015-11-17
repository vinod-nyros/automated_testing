#!/usr/bin/env python
import os
import sys

# JJW upd 10/19/14, org 7/11/11 - goes in wsgi.py and manage.py
parent =  os.path.abspath(os.path.dirname(__file__))
def ensure_path (s):
    if not s in sys.path: sys.path.append (s)
#ensure_path (os.path.dirname (parent))
#ensure_path (parent)
ensure_path (os.path.join (parent, 'apps'))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eracks.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
