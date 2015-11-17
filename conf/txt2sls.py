import sys 
#, yaml
from pprint import pprint
#from collections import OrderedDict

trace = 0

lines = [l.strip() for l in open ('requirements.txt')]
lines = [l for l in lines if l and not l.startswith ('#')]

if trace: pprint (lines)

print '# DO NOT EDIT - generated from txt2sls.py - to generate, run:'
print '# python txt2sls.py > requirements.txt.sls'

#dct = OrderedDict()

for l in lines:
  print
  print l.strip ('-e ') + ':'
  if l.startswith ('-e'):
    print '', 'pip installed:'
    print '  ', 'editable: ', l.strip ('-e ')
    print '  ', 'exists-action: w'
    #dct [l] = { 'pip.istalled': [ {'editable': l.strip ('-e ') }, { 'exists-action': 'w'} ] }
  else:
    print '  pip.installed'
    #dct [l] = 'pip.installed'


#pprint (dct)
#print yaml.dump (dct)
#print yaml.dump ({'1': 2})



