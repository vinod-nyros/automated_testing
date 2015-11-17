# session4.py, goes w/session.txt & session2.txt

import datetime
import sys, os

from pprint import pprint
from collections import OrderedDict

#print sys.path

#sys.path.insert ('/home/joe/eracks10/apps')
os.environ ['DJANGO_SETTINGS'] = '/home/joe/eracks10/settings.py'

#from home.helpers import SessionHelper

f = open ('session2.txt')

#print f.readline()
ses = '{' + f.read().replace ('Session:','"Session":') + '}'

ses = ses.replace ("': <", "': '<").replace ('\\n','').replace ('\\r','').replace (">,", ">',").replace (">}",">'}")

#print ses
# ...
 
ses = dict (eval (ses) ['Session'])

print len(ses)

#pprint (ses)

print ses.keys()

prod = ses ['prod']

print prod ['sku'], prod.keys()

class Prod (): # dict):
    def __init__ (self, ses):
        self.__dict__.update (ses ['prod'])
        #self.update (ses ['prod'])
        
        self.option_list = [Opt (k,v) for k,v in self.opts.items()]
        self.options_by_id = dict ([(o.id, o) for o in self.option_list])


    #def choices (self):
    def options (self):
        for k,v in self.opts.items():
            #print k
            pprint (v) #o.name
            print v ['name']
            selectedchoiceid = v ['selectedchoiceid']
            print '%s: %s' % (v ['name'], v ['choices'] [selectedchoiceid])

    def all_choices_works (self):
        for k,v in self.opts.items():
            #o = Opt (k.split ('_') [0], v)
            o = Opt (k, v)
            print o.name
            selectedchoiceid = o.selectedchoiceid
            selectedchoice = o.choices_by_id [o.selectedchoiceid]
            #print '%s %s: %s' % (o.qty, o.name, o.choices [selectedchoiceid]) # ['name'])
            print '%s %s: %s' % (o.choiceqty, o.name, selectedchoice.name)

    def all_choices (self):
        for o in self.option_list:
            selectedchoice = o.choices_by_id [o.selectedchoiceid]
            if o.choiceqty > 1:
                print '%s: %sx %s' % (o.name, o.choiceqty, selectedchoice.name), o.price
            else:
                print '%s: %s' % (o.name, selectedchoice.name), o.price


class Id_dict():
    def __init__ (self, id, dct):
        self.__dict__.update (dct)
        assert self.id == int(id), (self.id, id)

class Opt (Id_dict):
    def __init__ (self, theid, dct):
        theid = theid.split ('_') [0]
        #super(Opt, self).__init__ (theid, dct)
        Id_dict.__init__ (self, theid, dct)
        
        #print self.choices
        self.choice_list = [Choice (k,v) for k,v in self.choices.items()]
        self.choices_by_id = dict ([(c.id, c) for c in self.choice_list])


#    def choice_list (self):
#        for k,v in self.choices:
            

class Choice (Id_dict):
    pass

p = Prod (ses)

print p.__dict__.keys()

#print p.options()
pprint (p.opts)

print p.all_choices()

        
'''
OO breakdown:

- cart
- order
  - shipping
  - line items
    - prod
      - options
        - default vs chosen
    - qty
    - num
    - sumry / desc
    - notes
   
methods:
to_db
from_db
 
work_order - - full manifest
invoice
packing list
receipt


'''
    
