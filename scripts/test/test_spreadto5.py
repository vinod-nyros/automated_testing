import sys, os
from pprint import pprint

sys.path.insert (0, '/home/joe/eracks10/apps')
os.environ ['DJANGO_SETTINGS'] = '/home/joe/eracks10/settings.py'

#from utils import eval_duple, spreadto5


def spreadto5 (p1, p2, multiplier):
    print p1, p2, multiplier
    print p1 - p2
    print p1 - p2 + 2.5
    print (p1 - p2 + 2.5) / 5
    print ((p1 - p2 + 2.5) / 5) * 5
    print 1.35 * ((p1 - p2 + 2.5) / 5) * 5
    print int ((p1 - p2 + 2.5) / 5) * 5
    
    if p1 < p2:
        return int (1.0*((p1 - p2) - 2.5) / 5) * 5
    elif p1 > p2:
        return int ((multiplier or 1.35)*((p1 - p2) + 2.5) / 5) * 5

    return 0 # WHEN $1 = $2 THEN 0


print spreadto5 (75.0 * 2, 0.0, 0)

print 

