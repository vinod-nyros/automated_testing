from collections import OrderedDict

#from utils.tagstream24_5 import TagStream
from apps.utils import eval_duple, spreadto5  # , iff
from apps.utils import minitags as tags

from django.contrib import messages
#from django.forms.models import model_to_dict
from django.conf import settings
DEBUG = settings.DEBUG

from products.models import Product


#### Globals

trace = 1


#### session helpers - fill, update, cart-widget, cart-contents, etc

class SessionHelper (object):
    def __init__ (self, session):
        self.session=session

    def fill (self, product):
        session             = self.session
        prod                = product.__dict__.copy()               # plain dict - copy() added for dj1.7
        #prod                = model_to_dict (product)              # plain dict - dj 1.7 JJW
        product_options     = product.product_options()             # query results
        opts                = OrderedDict()                         # product [0].product_options().values()

        #print prod.keys()
        #prod.pop ('_state', None)
        # dj 1.7 serializer is different:

        if '_state' in prod:
          del prod ['_state']  # dj 1.7 fault - json can't serial model state

        #print 2, prod.keys()

        for po in product_options:
            for inx in range (po.qty):
                lineid = '%s_%s' % (po.id, inx+1)
                opts [lineid] = po.__dict__.copy()
                # may need to break this out & install pricedelta:
                opts [lineid] ['choices'] = dict ([(c['id'],c) for c in po.all_choices().values()])
                opts [lineid] ['name'] = po.calc_name
                #print 'OPTS NAME', opts ['name'], po.calc_name

        prod ['opts'] = opts
        #prod ['sku'] = sku
        prod ['qty'] = 1
        prod ['totprice'] = prod ['baseprice']
        #prod ['extprice'] = prod ['baseprice']  # all because Django templates suck - can't do basic expressions
        prod ['summary'] = ''
        prod ['notes'] = ''

        session ['prod'] = prod
        return prod


    def update (self, request, called_from_cart=False):
        if not request.is_ajax() and not called_from_cart:
            return dict (err='Unauthorized - code 1')

        if not request.method == 'POST':
            return dict (err='Unauthorized - code 2')

        session     = request.session
        assert self.session == session

        # need to massage for zope here
        choiceids   = request.POST.getlist ('choiceid')
        choiceqtys  = request.POST.getlist ('choiceqty')
        notes       = request.POST.get ('notes', '')

        # JJW 11/11/13 HERE:  need to save hidden form field for prod, double-check it against session -
        # issue is, people switching product pages, then going back to old one and changing the selection
        # JJW 12/15/13 DONE:
        # Solution: reload Prod from hidden sku, then use Django messaging to send user a message:
        # "Your product selections have been reset to defaults - please work on only one config at a time"

        sku = request.POST.get ('sku', '')
        prod = session.get ('prod', {})

        if not prod:
            messages.warning (request, 'No session prod found - loading %s' % sku)
            prod = self.fill (Product.objects.get(sku=sku))

        if sku != prod ['sku']:
            messages.warning (request, 'Your previous configuration for eRacks/%s has been replaced'
                ' - you are now configuring eRacks/%s' % (prod ['sku'], sku))
            prod = self.fill (Product.objects.get(sku=sku))

        try:
            prod    = session ['prod']
        except Exception, e:
            print
            print 'No prod for session:', session.keys()
            print
            print 'User:', request.user
            print 'Path:', request.path, request.path_info
            print 'Referer:', request.META.get ('HTTP_REFERER', 'no referer')
            print
            raise e

        try:
            opts        = prod ['opts']
        except Exception, e:
            print
            print 'No opts for prod:', prod.keys()
            print
            print 'User:', request.user
            print 'Path:', request.path, request.path_info
            print 'Referer:', request.META.get ('HTTP_REFERER', 'no referer')
            print
            raise e
        totprice    = prod ['baseprice']
        summary     = ''

        def calc_optprice (choice, default, choiceqty, defaultchoiceqty):
            return spreadto5 (choice ['cost'] * choiceqty, default ['cost'] * defaultchoiceqty, choice ['multiplier'])

        optchoices = []  # passed via ajax back to client

        for tpl in choiceids:     # update user selections, total price, summary
            optid, userchoiceid = eval_duple (tpl)
            #print optid, userchoiceid
            try:
                opt = opts [optid]
            except Exception, e:
                print
                print 'Exception:', `e`
                print
                print 'OPTID:', optid
                print
                print 'OPT KEYS:', opts.keys()
                print
                print 'PROD:', prod.get ('sku')
                print
                print 'PROD KEYS:', prod.keys()
                print
                raise e
            opt ['selectedchoiceid'] = userchoiceid
            defaultchoiceid = opt ['defaultchoice_id']
            opt ['defaultchoiceid'] = defaultchoiceid  # workaround django values() bug - ignores dbcolumn setting
            choices = opt ['choices']
            # userchoiceid = int (userchoiceid) now done in eval_duple
            choice = choices [userchoiceid]
            try:
               default = choices [defaultchoiceid]
            except Exception, e:
                from pprint import pformat
                print
                print 'exception:', `e`
                print
                print 'choiceids:', choiceids
                print
                print 'userchoiceid:', userchoiceid
                print
                print 'defaultchoiceid:', defaultchoiceid
                print
                print 'opt:', opt ['name'], optid # opt, too much output
                print
                #if defaultchoiceid == 30:
                print 'Possibly a misconfigured option, missing "none" choice!'
                print
                print 'choices:', pformat (choices)
                print
                raise e

            qtydict = dict ([eval_duple (d) for d in choiceqtys])
            choiceqty = qtydict.get (optid, 1)
            opt ['choiceqty'] = int (choiceqty)

            allowed_quantities = [int (s) for s in opt ['allowed_quantities'].split(',') if s]
            #print 'allowed_quantities', '"%s"' % opt ['allowed_quantities'], allowed_quantities, choiceqty, optid
            defaultchoiceqty = allowed_quantities [0] if allowed_quantities else 1  # assume 1st one for now, could add db field for it
            opt ['defaultchoiceqty'] = defaultchoiceqty

            optprice = calc_optprice (choice, default, choiceqty, defaultchoiceqty)
            totprice += optprice
            opt ['price'] = optprice

            # what we really want here is 'if item has changed'. grrr. need to re-write 'Add' when default re-selected.
            # And add a 'reset to defaults' btn, too.
            #if defaultchoiceid != userchoiceid  or (allowed_quantities and (choiceqty != allowed_quantities [0])):
            if defaultchoiceid != userchoiceid  or choiceqty != defaultchoiceqty:
                desc = choice ['name']
                if choiceqty > 1:
                    #desc = 'qty %i: %s' % (choiceqty, desc)
                    desc = '%ix %s' % (choiceqty, desc)

                summary = summary + ('|' if summary else '') + opt ['name'] + ': ' + desc
                #optchoices.append ((opt, choice))  # nope - dates aren't json serializable

                #optchoices.append (dict (
                #    optid=optid,
                #    #choiceid=choice['id'],
                #    choiceblurb=choice['blurb'],
                #    choicename=choice['name'],
                #    optprice=opt['price'],
                #    )
                #)
            #else:  # reset it to the default
            optchoices.append (dict (
                optid=optid,
                #choiceid=choice['id'],
                choiceblurb=choice['blurb'],
                choicename=choice['name'],
                optprice=opt['price'],
                #optprice='0',
                )
            )

            #try saving COW opt back to dict 3/6/14 JJW:
            # wasnt it
            #opts [optid] = opt

        if trace and DEBUG:
            print prod ['id'], prod ['sku']
            print choiceids
            print choiceqtys, totprice
            # print qtydict
            #print dict ([eval_duple (d) for d in choiceqtys])

        if summary:
            summary = tags.ul (tags.li (summary.split("|")))
        else:
            summary = 'Default Configuration'

        prod ['totprice'] = totprice   # save back to the session
        #prod ['extprice'] = totprice * prod ['qty']
        prod ['summary']  = summary
        prod ['notes']    = notes
        #prod ['opts'] = opts

        session ['prod']  = prod  # do we need this?  JJW 7/4/12

        return dict (price=totprice, summary=summary, prodid=prod['id'], optchoices=optchoices)


    def cart_totals (self):  # deprecated, move towards cart_summary, below
        session     = self.session
        grandtot    = 0
        totqty      = 0

        if session.has_key ('cart'):
            cart = session ['cart']

            for line in cart:  # .values():
                #qty = line.qty # ['qty']
                qty = line ['qty']
                totqty = totqty + qty
                #grandtot = grandtot + qty * line.totprice # ['totprice']
                grandtot = grandtot + qty * line ['totprice']

        return (totqty, grandtot)


    def cart_summary (self):  # Returns dict
        session     = self.session
        grandtot    = 0
        totqty      = 0
        totweight   = 0

        if session.has_key ('cart'):
            cart = session ['cart']

            for line in cart:
                qty = line ['qty']
                totqty += qty
                grandtot += qty * line ['totprice']
                totweight += qty * line ['weight']

        return dict (
            totqty = totqty,
            grandtot = grandtot,
            totweight = totweight,
        )

    def cart_summary_table (self):  # Returns table innards
        smry      = self.cart_summary()
        totqty    = smry ['totqty']
        grandtot  = smry ['grandtot']
        totweight = smry ['totweight']

        return tags.tbody (
          tags.tr (tags.th ('Items') + tags.td (totqty)) +
          tags.tr (tags.th ('Total') + tags.td ('$%.2f' % grandtot)) +
          tags.tr (tags.th ('Shipping Weight') + tags.td ('%s lbs' % totweight)) +
          tags.tr (tags.th ('Subtotal (pre-tax)') + tags.td ('$%.2f' % (grandtot+totweight))) +
          tags.tr (tags.th ('Tax') + tags.td ('TBD'))
        )

    def cart_details (self):
        totqty, grandtot = self.cart_totals()
        session          = self.session
        cart             = session.get ('cart', None)

        if not cart: return None

        table = tags.table (
                tags.thead (tags.tr (tags.th ('Line', 'Sku', 'Summary','Notes','Qty','New qty', 'Price', 'Ext'))) +
                #tags.thead (tags.tr (tags.th ('Line', 'Sku', 'Summary','Qty','New qty', 'Price', 'Ext'))) +
                tags.treo (
                    [tags.td (num + 1,
                            line['sku'],
                            line.get ('summary',''),
                            line.get ('notes',''),
                            line['qty'],
                            tags.input (name="updqty", size=3, width=3),
                            # + tags.input (name="ordlin", type='hidden', value=num),
                            '$%.2f' % line['totprice'],
                            '$%.2f' % (line['qty']*line['totprice']))
                        for num, line in enumerate (cart)]
                ) +
                #tags.tfoot (tags.tr (tags.th ('Total for %s items:' % totqty, colspan=7) + tags.th ('$%.2f' % grandtot))),
                tags.tfoot (tags.tr (tags.th ('Total for %s items:' % totqty, colspan=6) + tags.th ('$%.2f' % grandtot))),
            d='cart', width='100%')
        return table


#### Product / Session dict helpers - originally in quickie show_order_cart script

class Prod (): # dict):
    def __init__ (self, prod):
        self.__dict__.update (prod)
        self.option_list = [Opt (k,v) for k,v in self.opts.items()]
        self.options_by_id = dict ([(o.id, o) for o in self.option_list])

    def options (self):
        return self.opts.items()
        #for k,v in self.opts.items():
        #    selectedchoiceid = v ['selectedchoiceid']
        #    print '%s: %s' % (v ['name'], v ['choices'] [selectedchoiceid])

    def all_choices (self):
        rslt = []
        for o in self.option_list:
            selectedchoice = o.choices_by_id [o.selectedchoiceid]
            if o.choiceqty > 0:
              if o.choiceqty > 1:
                rslt += ['%s: %sx %s' % (o.name, o.choiceqty, selectedchoice.name)]
              else:
                rslt += ['%s: %s' % (o.name, selectedchoice.name)]
        return rslt
    @property
    def options_choices_as_txt (self):
      return '\n'.join (self.all_choices())

    @property
    def options_choices_as_br (self):
      return '<br>'.join (self.all_choices())

class Id_dict():
    def __init__ (self, id, dct):
        self.__dict__.update (dct)
        assert self.id == int(id), (self.id, id)

class Opt (Id_dict):
    def __init__ (self, theid, dct):
        theid = theid.split ('_') [0]
        #super(Opt, self).__init__ (theid, dct)
        Id_dict.__init__ (self, theid, dct)
        self.choiceqty = dct.get ('choiceqty', 1)
        self.selectedchoice = dct.get ('selectedchoice', 0)

        self.choice_list = [Choice (k,v) for k,v in self.choices.items()]
        self.choices_by_id = dict ([(c.id, c) for c in self.choice_list])

        self.selectedchoiceid = dct.get ('selectedchoiceid', dct.get('defaultchoice_id'))
        self.selectedchoice = self.choices_by_id [self.selectedchoiceid]

class Choice (Id_dict):
    pass

