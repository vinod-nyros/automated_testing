# -*- coding: utf-8 -*-

from string import capwords

from django.template import Template, Context, RequestContext

from hamlpy.hamlpy import Compiler


#### Globals

trace = 0


#### Utility Functions

def unslugify (s):
    s = s.replace ('_',' ').replace ('-',' ')
    s = capwords (s)
    return s


def eval_duple (s):
    def convert_maybe (s):
        if s.isdigit(): return int (s)
        else: return s

    return tuple (convert_maybe (i.strip()) for i in s.strip (' ()').split (','))
    #return tuple (str(i.strip("'" + '" ')) for i in s.strip (' ()').split (','))
    #return tuple (str(i.strip()) for i in s.strip (' ()').split (','))
    #return tuple (int(i.strip()) for i in s.strip (' ()').split (','))


def iff (b,t,f):
  if b: return t
  else: return f


def spreadto5 (p1, p2, multiplier):
    #print p1, p2, multiplier
    if p1 < p2:
        return int (1.0*((p1 - p2) - 2.5) / 5) * 5
    elif p1 > p2:
        return int ((multiplier or 1.35)*((p1 - p2) + 2.5) / 5) * 5

    return 0 # WHEN $1 = $2 THEN 0


def remove_leading_spaces (s):
    def indent (line):
        return s.find (s.strip ())

    assert not '\t' in s, "String must not contain tabs"

    lines = s.splitlines()

    indent = max (indent (l) for l in lines)
    new_lines = []

    for l in lines:  # should use tokenize, here - see tabnanny source
        new_lines.append (l [indent:])

    return '\n'.join (new_lines)


# Workarounds for annoying new BrowserID autologin "Feature" Sep 2013 - NOT NECESSARY NOW, used old onclick handler, modified for new form

#from django_browserid.views import Verify

#class MyVerifyClass(Verify):
#    def dispatch(self, request, *args, **kwargs):
#        print "IN MyVerifyClass DISPATCH:", request.user, request.user.is_authenticated()
#        if not request.user or not request.user.is_authenticated():
#            return False
#        else:
#            return super(Verify, self).dispatch(request, *args, **kwargs)

    #def form_valid (self, form):
    #    print "IN MyVerifyClass FORM_VALID:", self.user
    #    if not self.user:
    #        return False
    #    else:
    #        return super (MyVerify, self).form_valid (form)


# JJW example for finding caller module - used in obdjects

def app_dir():
    import inspect, os
    #from django.db.models import get_apps
    from pprint import pformat
    #print __file__
    #print pformat (get_apps())  # nope - only apps with *models*
    from django.conf import settings
    apps = settings.INSTALLED_APPS [:]
    apps = [app.split ('.') [-1] for app in apps if not app.startswith ('django.')]
    print apps
    print

    stack = inspect.stack()
    #print stack

    for frame in stack:
        f = frame [0]
        #print inspect.getmodule (f)
        m = inspect.getmodule (f)
        print m
        print dir (m)
        print m.__name__
        print

        # print inspect.getsourcelines (f)

        modname = m.__name__
        if '.' in modname:
            modname = modname.split ('.') [0]

        if modname in apps:
            print 'Found it:', modname, os.path.dirname (m.__file__)
            break


#### Utility Forms helpers and classes

from django.forms.widgets import Media
#from obdjects.templates import remove_leading_spaces # pasted here directly 11/7/15 JJW to remove dependency

class InlineMedia (Media):
    def __init__ (self, inline_js, *args, **kw):
        self.inline_js = remove_leading_spaces (inline_js)
        super (InlineMedia, self).__init__(*args, **kw)

    def render_js (self):
        return [u'<script type="text/javascript">%s</script>' % self.inline_js]


from django.utils.safestring import mark_safe
from django.forms import ModelForm  #, BaseModelForm
#from django.template.defaultfilters import truncatechars
from django.template.loader import render_to_string
from apps.utils import minitags as tags

class TemplateFormMixin (object):
    template = 'Subclasses need to indicate a template here'
    header = 'Subclasses need to fill in a header here'
    columns = 3

    @property
    def myname (self):
        return self.__class__.__name__

    def handle_required_fields (self):  # bold_the_labels, turn off required, etc
        for name, field in self.fields.items():
            if trace: print name, field.required
            if field.required:
                field.old_label = field.label
                field.label = mark_safe ('<b>%s</b>' % field.label)

    def is_empty (self):   # beware - this will NOT work if any of the fields have defaults, eg, US for country :)
        for field in self:
            if trace: print '"%s"' % field.value()
            if field.value():
                return False
        return True

    def as_table (self):
        """
        Returns this form rendered as HTML <tr>s -- excluding the <table></table>.

        - Bolds the labels of the required fields

        - adds a thead header

        - renders to a template

        Rewritten to use a template rather than django.forms.forms.Form.as_table
        JJW 7/11/12
        """
        self.handle_required_fields()

        return render_to_string (self.template, dict (form=self)) #, RequestContext (no request :-(

    @property
    def media (self):
        return InlineMedia ('''\
            $('#edit%(myname)s').click (function (e) {
                e.preventDefault();
                $('#%(myname)s tr').toggleClass ('hidden');
            });
            ''' % dict (myname=self.myname)
        )

    #def _get_media (self):
    #media = property (_get_media)


class TemplateForm (TemplateFormMixin, ModelForm):
    # pass

    def old_as_table_for_dual_form (self):
        """
        Returns this form rendered as HTML <tr>s -- excluding the <table></table>.

        - Bolds the labels of the required fields

        - Includes a display version of the data (aka preview) if an existing instance is supplied

        Copied and modified from django.forms.forms.Form
        JJW 7/11/12
        """
        self.handle_required_fields()

        thead = tags.thead (tags.tr (tags.th (self.header + '&nbsp;' + tags.button ('Toggle Edit', d='edit%s' % self.myname, cls='nice small green radius button'), colspan=self.columns))) if self.header else ''

        if self.initial:  # filled with data
            #preview_rows = [('<td>%s:</td><td>%s</td><td>%s</td>' % (field.label, field.value, field.help_text)) for name, field in self.fields.items()]
            preview_rows = [('<th>%s:</th><td>%s</td><td>%s</td>' % (field.label, getattr (self.instance, name, ''), field.help_text)) for name, field in self.fields.items()]
            preview = '<tr>%s</tr>' % '</tr><tr>'.join (preview_rows) if preview_rows else ''
            normal_row = u'<tr%(html_class_attr)s class="hidden"><th>%(label)s</th><td>%(errors)s%(field)s</td><td title="%(help_text)s">%(help_text).50s</td></tr>'
        else:
            preview = ''
            normal_row = u'<tr%(html_class_attr)s><th>%(label)s</th><td>%(errors)s%(field)s</td><td title="%(help_text)s">%(help_text).50s</td></tr>'

        rows = preview + self._html_output (
            normal_row = normal_row,  # u'<tr%(html_class_attr)s><th>%(label)s</th><td>%(errors)s%(field)s</td><td>%(help_text)s</td></tr>',
            error_row = u'<tr><td colspan="2">%s</td></tr>',
            row_ender = u'</td></tr>',
            #help_text_html = u'<br /><span class="helptext">%s</span>',
            #help_text_html = u'<span class="helptext">%s</span>',
            help_text_html = u'My Help Text: %s',
            errors_on_separate_row = False
        )

        return mark_safe (thead + tags.tbody (rows, d=self.myname))



#### Utility Classes

class CountDict (dict):
    def inc (self, key):
        count = self.get (key, 0)
        self [key] = count + 1

class Breadcrumb (object):
    def __init__ (self, name='Name', title='Rackmount Servers', url='/'):
        self.name = name
        self.title = title
        self.url = url


#### Utility Database Functions

## DBModel Helpers - there *should* be a dbmodel.update (fields)  - but nope, there isn't
def setfields (dbmodel_instance, fields):
    for k,v in fields.iteritems():
        setattr (dbmodel_instance, k, v)

# this one should also be built-in:
# idea for ensure_present: get_or_create, then update as needed - see milestone1/www/beyond/scripts/partner/modules/umg.py
def create_or_update (model, keys, fields):  # keys, fields: dicts of unique keys, default fields to create / update
    instance, created = model.objects.get_or_create (defaults = fields, **keys)

    if not created:
        setfields (instance, fields)
        instance.save()

    return instance, created


#### Admin display methods

def modified (instance):
    if instance.dt:
        return instance.dt.date()
modified.short_description = 'Modified'
modified.admin_order_field = 'modified'


def created (instance):
    if instance.created:
        return instance.created.date()
created.short_description = 'Created'
created.admin_order_field = 'created'

def updated (instance):
    if instance.updated:
        return instance.updated.date()
updated.short_description = 'Updated'
updated.admin_order_field = 'updated'


#### Admin Actions

def publish (modeladmin, request, queryset):
    queryset.update (published=True)
publish.short_description = "Publish selected items"

def unpublish (modeladmin, request, queryset):
    queryset.update (published=False)
unpublish.short_description = "Unpublish selected items"


#### Haml and Templating

# For inline text haml compiles
def hamlpy (t):
    #from hamlpy.hamlpy import Compiler
    return Compiler().process(t)

# Combined Haml and Django Template
def HamlTemplate (s):
    the_haml = hamlpy (s)
    #print the_haml
    result = Template (the_haml)
    #print result
    return result



#### main for testing

if __name__ == '__main__':
    from apps.legacy.models import Product

    p = Product.objects.filter (sku='NAS16X') [0]

    configgrid = HamlTemplate ('''
    .configurator
        %h1= product.name
        %p Desc:{{ product.description|default:'(No Desc)' }}
        %p Specs:{{ product.specs|default:'(No Specs)' }}
        %p <a href='/images/product/{{ product.sku }}'>More Photos</a>
        %p Base Price: ${{ product.baseprice|stringformat:".2f" }}

        %table.configgrid
            - for po in product.product_options
                %tr{'class':"{% cycle 'odd' 'even' %}"}
                    %td= po.calc_name
                    %td= po.as_combo|safe
                    %td{'id':'choicedesc_{{ po.defaultchoice.id }}' }= po.defaultchoice.name
    ''')

    print configgrid.render (Context (dict(product=p)))




    oldconfiggrid = HamlTemplate ('''
.configgrid
    %h1= product.name
    %p Desc:{{ product.description|default:'(No Desc)' }}
    %p Specs:{{ product.specs|default:'(No Specs)' }}
    %p <a href='/photos/{{ product.sku }}'>More Photos</a>
    %p Base Price: ${{ product.baseprice|stringformat:".2f" }}

    %table
        - for po in product.prodopt_set.all
            %tr{'class':"{% cycle 'even' 'odd' %}"}
                %td= po.option.name
''')



the_goal='''
    s = h1 (p.title)
    s += para ('Desc:' + (p.description or '(No Desc)'))
    s += para ('Specs:' + (p.specs or '(No Specs)'))
    s += para (link ('More Photos', href = '/photos/' + prod))
    s += para ('Base Price: $%.2f' % p.calc_baseprice)
    rows = []
    for po in p.productoption_set.all():
      rows += [td (po.calc_name, po.as_combo) +
               td (po.optionchoice.choice.description, d='choicedesc_%s' % po.optionchoice.choice.id)]
    tbl = table (treo (rows), d='configgrid')
    s += form (tbl + hidden (name='prod', value=p.id) +
                     submit (value='Add to Cart'),
               action='/cart/', method='post')
    #s += div ('my content2 div', d='content2')
'''
