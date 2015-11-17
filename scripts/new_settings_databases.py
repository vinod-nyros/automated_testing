#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

settings = file ("../settings.py")
lines = settings.readlines()
file ("../settings.py~", 'w').writelines (lines)
#dbregex = re.compile (r"(#*.*)(DATABASE_)([^#]*\s*?)(\s*#*.*)")
dbregex = re.compile (r"(#*.*)(DATABASE_)([^#]*?)(?=\s*#)(\s*#*.*)")
databases_section = []  # list of tuples w/line number

for n,l in enumerate (lines):
    if dbregex.match (l):
        databases_section += [(n ,dbregex.sub (r'\1\3,\4', l))]

def contiguous (lst):  # assumes list of tuples with integer first entry
    test = [tupl [0] for tupl in lst]
    return len (test) == test [-1] +1 - test [0]

if not contiguous (databases_section):
    raise Exception ("DATABASE settings not contiguous or more than one section - must do by hand")

newsettings = []
done = False
dbstart = databases_section [0][0]  # first line
dbend = databases_section [-1][0]    # last line

for n,l in enumerate (lines):
    if done:
        newsettings += [l]
        continue

    if n == dbstart:
        newsettings += ['DATABASES = dict (\n']
        newsettings += ['    default = dict (\n']
        newsettings += ['        ' + l for n,l in databases_section]
        newsettings += ['    )\n']
        newsettings += [')\n']
    elif n > dbstart and n < dbend:
        continue
    elif n == dbend:
        done = True
    else:
        newsettings += [l]

file ("../settings.py", 'w').writelines (newsettings)
#print ''.join ([l for n,l in databases_section])
