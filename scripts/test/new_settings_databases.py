#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding: utf-8

import re

settings = file ("../settings.py")
lines = settings.readlines()
file ("../settings.py~", 'w').writelines (lines)
dbregex = re.compile (r"(#*\W*)(DATABASE_)")
databases_section = []  # list of tuples w/line number

#print len (lines)

for n,l in enumerate (lines):
    #print n,l
    if dbregex.match (l):
        #print dbregex.match (l).expand (r'\1aha')
        print dbregex.sub (r'        \1', l)
        databases_section += [(n ,dbregex.sub (r'    \1', l))]
        #print l
        #if l.startswith ('#'):
        #    print 'aha', l

print databases_section

def contiguous (lst):  # assumes list of tuples with integer first entry
    test = [tupl [0] for tupl in lst]
    print test
    return len (test) == test [-1] +1 - test [0]

if not contiguous (databases_section):
    raise Exception ("DATABASE settings not contiguous or more than one section - must do by hand")


print contiguous ([(n,'') for n in [1,2,3,4,5]])
print contiguous ([(n,'') for n in [2,3,4,5,6,7,8]])
print contiguous ([(n,'') for n in [1,2,3,4,5,8,9,]])
print contiguous ([(n,'') for n in [3,4,5,123]])
print contiguous ([(n,'') for n in [1,2,2,3,4,5]])


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
        newsettings += [l for n,l in databases_section]
        newsettings += ['    )']
        newsettings += [')']
    elif n > dbstart and n < dbend:
        continue
    elif n == dbend:
        done = True
    else:
        newsettings += [l]

for l in newsettings: print l
