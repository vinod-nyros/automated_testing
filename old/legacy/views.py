# -*- coding: utf-8 -*-

from django.template import Template, Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from models import Product  #, Categories, Prodopt, Prodoptchoice, Option, Choice, ChoiceCategory #, Optchoices

from django_eracks.apps.utils.minitags2 import TagStream
from django_eracks.apps.utils import eval_duple, iff, spreadto5

try:
    import json
except ImportError:
    import simplejson as json


#### globals

trace = 0


#### session management - fill, update

#def fill_session (session, sku):  # getpool - new arch version of getpoc
#    product             = Product.objects.filter(sku=sku)       # query results - with 'values', etc
#    prod                = product.values() [0]                  # plain dict
#    product_options     = product [0].product_options()         # query results

def fill_session (session, product):  # getpool - new arch version of getpoc
    prod                = product.__dict__                      # plain dict
    product_options     = product.product_options()             # query results

    opts                = {}  #product [0].product_options().values()

    for po in product_options:
        for inx in range (po.qty):
            lineid = '%s_%s' % (po.id, inx+1)
            opts [lineid] = po.__dict__
            # may need to break this out & install pricedelta:
            opts [lineid] ['choices'] = dict ([(c['id'],c) for c in po.option_choices().values()])

    prod ['opts'] = opts
    #prod ['sku'] = sku
    prod ['qty'] = 1
    prod ['totprice'] = prod ['baseprice']
    prod ['notes'] = ''

    session ['prod'] = prod


def update_session (request):
    session     = request.session

    # need to massage for zope here
    choiceids   = request.POST.getlist ('choiceid')
    choiceqtys  = request.POST.getlist ('choiceqty')
    notes       = request.POST.get ('notes', '')

    prod        = session ['prod']
    opts        = prod ['opts']
    totprice    = prod ['baseprice']
    summary     = ''

    def calc_optprice (choice, default):
        return spreadto5 (choice ['cost'], default ['cost'], choice ['multiplier'])

    optchoices = []  # passed via ajax back to client

    for tpl in choiceids:     # update user selections, total price, summary
        optid, userchoiceid = eval_duple (tpl)
        opt = opts [optid]
        opt ['selectedchoiceid'] = userchoiceid
        defaultchoiceid = opt ['defaultchoice_id']
        opt ['defaultchoiceid'] = defaultchoiceid  # workaround django values() bug - ignores dbcolumn setting
        choices = opt ['choices']
        # userchoiceid = int (userchoiceid) now done in eval_duple
        choice = choices [userchoiceid]
        default = choices [defaultchoiceid]
        optprice = calc_optprice (choice, default)
        totprice += optprice
        opt ['price'] = optprice
        #totprice = totprice + spreadto5 (choice ['price'], default ['price'], choice ['multiplier'])
        #totprice = totprice + choice ['pricedelta']  # may need to put this in the dict at fill time
        #totprice = totprice + Choice.objects.get (id=userchoiceid).calc_pricedelta (??! need it fm the po..)


        # what we really want here is 'if item has changed'. grrr. need to re-write 'Add' when default re-selected.
        # And add a 'reset to defaults' btn, too.
        if defaultchoiceid != userchoiceid:
            #desc = choice ['Choices']
            desc = choice ['name']
            summary = summary + iff (summary, ', ' + desc, desc)
            #optchoices.append ((opt, choice))  # nope - dates aren't json serializable
            optchoices.append (dict (
                optid=optid,
                #choiceid=choice['id'],
                choiceblurb=choice['blurb'],
                choicename=choice['name'],
                optprice=opt['price'],
                )
            )

    for tpl in choiceqtys:     # update quantities, total price (summary?)
        optid, choiceqty = eval_duple (tpl)
        opt = opts [optid]
        opt ['choiceqty'] = choiceqty
        choices = opt ['choices']
        userchoiceid = opt.get ('selectedchoiceid', opt ['defaultchoice_id'])
        defaultchoiceid = opt ['defaultchoice_id']
        choice = choices [userchoiceid]
        default = choices [defaultchoiceid]
        optprice = calc_optprice (choice, default)
        totprice += choiceqty * optprice
        opt ['price'] = choiceqty * optprice
        optchoices.append (dict (
            optid=optid,
            optprice=opt['price'],
            )
        )


    if not summary:
      summary = 'Default Configuration'

    if notes:
      summary = summary + ', Notes:' + notes

    prod ['totprice'] = totprice   # save back to the session
    prod ['summary']  = summary
    prod ['notes']    = notes

    return dict (price=totprice, summary=summary, prodid=prod['id'], optchoices=optchoices)


#### configgrid view with js

config_grid_js='''
function update_config (e) {
    console.log ($('.configform').serialize());
    if (e) {
        console.log ('ITEM CHANGED:');
        console.log (e.currentTarget);
        console.log ($(e.target).find ('option:selected'));
    }

    $.post ("/update_product/", $('.configform').serialize(), function(json) {
        console.log (json);
        $('.configform .price b').html ('$' + json.price);
        $('.configform .summary').html ('Configuration Summary: ' + json.summary);

        $.each(json.optchoices, function(key, val) {  // it's an array, so keys are 0
            console.log (key, val);
            console.log ('#' + val.optid + ' .info');
            if (val.choicename)
                $('#' + val.optid + ' .info').html (val.choicename)
            if (val.choiceblurb)
                $('#' + val.optid + ' .info').attr ('title', val.choiceblurb)
            if (val.optprice)
                $('#' + val.optid + ' .optprice').html ('$' + val.optprice)
        });
    });
}

$(document).ready(function() {
    update_config();

    $('.configgrid select[name="choiceid"]').change (update_config);
    $('.configgrid select[name="choiceqty"]').change (update_config);
});
'''

def configgrid2 (request, sku):
    product = get_object_or_404 (Product, sku=sku)

    fill_session (request.session, product)

    return HttpResponse (TagStream()
        .html
            .body
                .script ('', src="/js/jquery.js", type="text/javascript")
                .script (config_grid_js, type="text/javascript")
                .form (product.as_content, cls='configform')
        .render()
    )


#@is_ajax or ajax_required...
def update_product (request):
    results = update_session (request)
    return HttpResponse (json.dumps (results), mimetype='application/json')






#### Old:

from django_eracks.apps.utils import HamlTemplate

configgrid_template = HamlTemplate ('''
.configurator
    %h1= product.name
    %p Desc:{{ product.description|default:'(No Desc)' }}
    %p Specs:{{ product.specs|default:'(No Specs)' }}
    %p <a href='/images/product/{{ product.sku }}'>More Photos</a>
    %p Base Price: ${{ product.baseprice|stringformat:".2f" }}

    %table.configgrid
        %tr
            %th Option
            %th Choices
            %th More Info
        - for po in product.product_options
            %tr{'class':"{% cycle 'odd' 'even' %}"}
                %td= po.calc_name
                %td= po.as_combo|safe
                %td{'id':'choicedesc_{{ po.defaultchoice.id }}' }= po.defaultchoice.name
''')

#### Views


def configgrid (request, sku):
    product = get_object_or_404 (Product, sku=sku)

    session_items = request.session.items()

    force_fault_to_show_session = 1 / 0

    return HttpResponse ('<html><form>%s</form></html>' % configgrid_template.render (Context (dict(product=product))))

