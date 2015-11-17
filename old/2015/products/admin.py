# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ModelForm, Select, ModelMultipleChoiceField, ModelChoiceField #, Form
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.html import escape

from sqls.minitags import a as link
from models import Image, Categories, Prodopt, Product, Prodoptchoice, Option, Choice, ChoiceCategory, get_misc_choice_category #, Optchoices

from utils import modified, created, updated, publish, unpublish

from filebrowser.settings import ADMIN_THUMBNAIL
from filebrowser.widgets import ClearableFileInput
from filebrowser.fields import FileBrowseField


#### globals

trace = 0


#### Admin helpers - Django 1.7 check framework (override m2m check for through)
# https://docs.djangoproject.com/en/1.7/topics/checks/

from django.core.checks import register

@register('admin')
def m2m_check(app_configs, **kwargs):
    errors = []
    # ... your check logic here
    return errors

# JJW from https://github.com/etiennekruger/meddb/blob/master/meddb/registrations/admin.py, among others - should move to utils / helpers
class FilteredSelectSingle (Select):
    """
    A Select with a JavaScript filter interface.
    """
    class Media:
        js = ("admin/js/fkfilter.js",)
        css = { 'all': ("admin/css/filteredselect.css",) }

    def __init__(self, verbose_name, attrs=None, choices=()):
        self.verbose_name = verbose_name
        super(FilteredSelectSingle, self).__init__(attrs, choices)

    def render(self, name, value, attrs={}, choices=()):
        attrs['class'] = 'selectfilter'
        output = [super(FilteredSelectSingle, self).render(name, value, attrs, choices)]
        output.append((
                '<script type="text/javascript">'
                'django.jQuery(document).ready(function(){'
                'django.jQuery("#id_%s").fk_filter("%s")'
                '});'
                '</script>'
            ) % (name, self.verbose_name.replace('"', '\\"'),));
        return mark_safe(u''.join(output))


#### Admin classes - Image

def image_thumbnail(obj):
    if obj.image and obj.image.filetype == "Image":
        return '<img src="%s" />' % obj.image.version_generate(ADMIN_THUMBNAIL).url
    else:
        return ""
image_thumbnail.allow_tags = True
image_thumbnail.short_description = "Thumbnail"


# out 10/14/13 JJW? nope, m2m
class ImageAdmin (admin.ModelAdmin):
    date_hierarchy = 'updated'
    list_display = (image_thumbnail, 'image', 'title', 'caption', updated, created,'published')
    list_filter = ('updated', 'created','published')
    actions = [publish, unpublish]

    #formfield_overrides = {
    #    models.ImageField: {'widget': ClearableFileInput},
    #    FileBrowseField: {'widget': ClearableFileInput},
    #}


#class ImageInline(admin.TabularInline):
#    model = Image


class CategoryAdmin (admin.ModelAdmin):
    #change_form_template = 'admin_category_wysiwyg_change_form.html'
    change_form_template = 'admin_wysiwyg_change_form.html'

    date_hierarchy = 'updated'
    list_display = ('id', 'name', 'title', 'blurb','sortorder', updated, created,'published')
    list_filter = ('updated','created','published')
    #list_editable = ('title','blurb','sortorder',)  # 'name', doesn't work - can't be both clickable and editable
    list_editable = ('title','sortorder',)  # 'name', doesn't work - can't be both clickable and editable
    list_display_links = ('id','name')
    list_per_page = 50
    save_as = True
    prepopulated_fields = {"slug": ("name","title",)}
    actions = [publish, unpublish]
    filter_horizontal = ('images',)

    formfield_overrides = {
        models.ImageField: {'widget': ClearableFileInput},
    }


#### Product Option admin - combined PO-OL and legacy PO-POC models

def require (modeladmin, request, queryset):
    queryset.update (required=True)
require.short_description = "Require selected items"

def unrequire (modeladmin, request, queryset):
    queryset.update (required=False)
unrequire.short_description = "Unrequire selected items"

def single (modeladmin, request, queryset):
    queryset.update (single=True)
single.short_description = "Set single for selected items"

def unsingle (modeladmin, request, queryset):
    queryset.update (single=False)
unsingle.short_description = "Unset single for selected items"


def option_link (instance):
    if instance:
        option = instance.option # Prodopt.objects.get (option=instance.option)
        return link (option.name,
            href='/admin/products/option/%s' % option.id,
            title='Go to the option for this ProdOpt: %s' % option)
    return 'None'

option_link.short_description = 'Option'
option_link.description = 'Option referenced by this ProdOpt'
option_link.allow_tags = True


def product_link (instance):
    if instance:
        product = instance.product # Prodopt.objects.get (product=instance.product)
        return link (product.sku,
            href='/admin/products/product/%s' % product.id,
            title='Go to the product for this ProdOpt: %s' % product)
    return 'None'

product_link.short_description = 'Product'
product_link.description = 'Product referenced by this ProdOpt'
product_link.allow_tags = True


def poc_link (instance):
    if instance:
        pocs = Prodoptchoice.objects.filter (productoption=instance)
        c = pocs.count()

        if c:
            if c==1:
                poc = pocs[0]
                return link (poc.choice.name,
                    href='/admin/products/choice/%s' % poc.choice.id,  # could double-check this matches defaultchocie, here
                    title="Go to the choice referenced by this prodopt's legacy POCs: %s" % instance)
            else:
                return link ("%s choices / POCs" % c,
                    href='/admin/products/choice/?prodoptchoice__productoption=%s' % instance.id,
                    title='Go to the list of choices which are referenced by the prodoptchoices for this prodopt: %s :\n%s' % (instance, '\n'.join (pocs.values_list ('choice__name', flat=True))))
        return 'None'

poc_link.short_description = 'POCs'
poc_link.description = 'Choices referenced by the (legacy) prodoptchoices for this ProdOpt'
poc_link.allow_tags = True


def choices_link (instance):
    if instance:
        choices = instance.option.choices.all()
        c = choices.count()

        if c:
            if c==1:
                choice = choices[0]
                return link (choice.name,
                    href='/admin/products/choice/%s' % choice.id,  # could double-check this matches defaultchocie, here
                    title='Go to the choice referenced by this prodopt: %s' % instance)
            else:
                return link ("%s choices" % c,
                    href='/admin/products/choice/?options__id__exact=%s' % instance.option.id,
                    title="Go to the list of choices which are referenced by this prodopt's option: %s :\n%s" % (instance, '\n'.join (choices.values_list ('name', flat=True))))
        return 'None'

choices_link.short_description = 'Choices'
choices_link.description = "Choices referenced by this ProdOpt's Option"
choices_link.allow_tags = True


def product_published (instance):
    if instance:
        #return instance.product.published
        if instance.product.published:
            return '<span style="color:green">Yes</span>'
    return '<span style="color:red">No</span>'

product_published.short_description = 'Pub' # 'Product published'
product_published.description = 'Product referenced by this ProdOpt is published'
product_published.allow_tags = True
#product_published.type = bool  # nope


class ProdoptForm (ModelForm):
    def __init__ (self, *args, **kw):
        ModelForm.__init__ (self, *args, **kw)
        if self.instance and isinstance (self.instance, Prodopt):
          inst=self.instance
          dc=self.fields.get('defaultchoice')
          if trace: print inst.all_choices # option_id # dir (inst)
          if inst.pk and inst.all_choices().count():
            dc.queryset = inst.all_choices()  #Choice.objects.filter (id__in = inst.choices.values_list('id', flat=True))

    class Meta:
        model = Prodopt


from django.utils.functional import curry
from django.forms.models import modelform_factory

class ProdoptAdmin (admin.ModelAdmin):
    class Media:
        css = { "all": ("/css/wide_lookup_horizontal.css",) }
        #js = ("my_code.js",)

    @classmethod
    def check(cls, model, **kw):  # Django 1.7 system check framework - gets called wtih ModelBase class
        return []

    def lookup_allowed(self, key, value):
        #if key in ('team__season__season_start_date__year', 'team__sport'):
        return True
        return super(ProdoptAdmin, self).lookup_allowed(key, value)

    def save_model(self, request, obj, form, change):
        obj.save()

        if 'choices' in form.cleaned_data:  # otherwise it's the summary screen just changing the default choice
            # We can't just do .clear(), it wipes out the 'through' data, so do careful_update..
            curr_choices = frozenset (obj.choices.all())
            new_choices = frozenset (form.cleaned_data ['choices'])
            to_add = new_choices - curr_choices
            to_delete = curr_choices - new_choices

            for choice in to_delete:
                #choice.delete()  # NOOOOOOOOO!  Don't delete the underlying object! Just the m2m entry!!
                obj.prodoptchoice_set.get(choice=choice).delete()

            for choice in to_add:
                Prodoptchoice.objects.create (productoption=obj,choice=choice)

        form.save_m2m = lambda : None # self.dummy # lambda x: x  # Kluge alert! Monkey patching!

    fieldsets = (
        (None, { 'fields': (    ('name', 'published'),
                                ('product', 'option','created', 'updated',),
                            )   }),
        ('Option-related fields', { 'fields': ('qty','single','required'), 'classes': ('wide', ), }),
        ('Choice-related fields', { 'fields': ('allowed_quantities', 'choices_orderby', 'defaultchoice'), 'classes': ('wide'), }),
        ('Legacy Choices (POCs)', { 'fields': ('choices', ), 'classes': ('wide', 'collapse'), }),
    )

    list_filter = ('updated', 'created', 'published', 'choices_orderby', 'product__published', 'product', 'option')  # no: gives all, not just the ones that are df's: 'defaultchoice')
    #list_display = ('__unicode__', 'defaultchoice', product_link, option_link, 'name', 'qty', 'single','required', 'choices_orderby', updated, created, 'product__published', product_published)
    list_display = ('__unicode__', 'defaultchoice', product_link, option_link, choices_link, poc_link, 'name', 'qty', 'allowed_quantities', 'single','required', created, updated, product_published)
    list_editable = ('defaultchoice', 'allowed_quantities', 'single', 'required')  # CAN'T restrict to existing choices :(
    filter_horizontal = ('choices', )
    readonly_fields = ('option', 'product', 'created', 'updated')
    form = ProdoptForm
    list_per_page = 20
    #change_form_template = 'admin_prodopt_change_form.html'
    save_on_top = True
    save_as = True
    actions = [publish, unpublish, require, unrequire, single, unsingle]

    def get_changelist_form (self, req, **kw):
        defaults = {
            "formfield_callback": curry(self.formfield_for_dbfield, request=req),
        }
        defaults.update(kw)
        return modelform_factory (Prodopt, form=ProdoptForm, **defaults)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
      if db_field.name in (list(self.filter_vertical) + list(self.filter_horizontal)):
        kwargs['widget'] = FilteredSelectMultiple(db_field.verbose_name, (db_field.name in self.filter_vertical))
      return db_field.formfield(**kwargs)


# NLN JJW 10/13
class ProdoptchoiceAdmin(admin.ModelAdmin):
    def lookup_allowed(self, key, value):
        return True

    date_hierarchy = 'updated'
    fields = ('productoption', 'choice', 'pricedelta', 'current')
    search_fields = ('productoption__product__sku','productoption__option__name')
    # nope: 'productoption____unicode__'
    list_filter = ('updated','created', 'current')  # too many:'productoption''pricedelta''choice')  # 'productoption__product' doesn't work
    # nope: list_filter = ('dt', 'productoption.product', 'productoption.option', 'choice','pricedelta')
    list_display = ('productoption', 'choice','pricedelta','current', updated, created, )
    list_editable = ('pricedelta',)
    list_per_page = 50

    list_display_links = []
    readonly_fields = ('productoption', 'choice')
    save_as = True


#### Product admin

class ProductAdmin (admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        # We can't just do .clear(), it wipes out the 'through' data, so do careful_update..
        curr_opts = frozenset (obj.options.all())

        if form.cleaned_data.has_key ('options'):  # if not, you're updating from the list page, so leave options alone
            new_opts = frozenset (form.cleaned_data ['options'])
            to_add = new_opts - curr_opts
            to_delete = curr_opts - new_opts

            for option in to_delete:
                # option.delete()  # NOOOOOOO!  Don't delete the whole Option!!!!!
                # obj.prodopt_set.remove (option) # nope. not there.
                obj.prodopt_set.get (option=option).delete()

            for option in to_add:
                po = Prodopt (product=obj, option=option)
                po.defaultchoice_id = 30
                po.save()
                #Prodopt.objects.create (product=obj, option=option)

        form.save_m2m=lambda : None  # Kluge alert! Monkey patching!

    @classmethod
    def check(cls, model, **kw):  # Django 1.7 system check framework - gets called with ModelBase class
        return []

    fieldsets = (
        (None, { 'fields': (('sku', 'name',),
                            ('cost', 'baseprice'),
                            ('title', 'published',),
                            #('new_grid'),
                            ('sortorder', 'multiplier', 'weight',),
                            ('baseoptions',),
                            ('link', 'image',),
                            #('options',)
                            )   }),
        ('Blurb',       { 'fields': ('blurb',),       'classes': ('collapse', ), }),
        ('Description', { 'fields': ('description',), 'classes': ('collapse', 'edit'), }),
        #('Specs',       { 'fields': ('specs',),       'classes': ('collapse', 'xinha_editor'), }),
        ('Features',    { 'fields': ('features',),    'classes': ('collapse', ), }),
        ('Comments',    { 'fields': ('comments',),     'classes': ('collapse', ), }),
        ('Meta',        { 'fields': ('meta_title','meta_description','meta_keywords'), 'classes': ('collapse', ), }),
        #('Algorithm',   { 'fields': ('algorithm',),   'classes': ('collapse', ), }),
        ('Category',    { 'fields': ('category',),    'classes': ('wide', 'collapse'), }),
        ('Options',     { 'fields': ('options',),     'classes': ('wide', 'collapse'), }),
        ('Images',      { 'fields': ('images',),      'classes': ('wide', 'collapse'), }),
    )

    date_hierarchy = 'updated'
    list_filter = ('updated', 'created', 'published', 'category', 'baseoptions')
    list_display = ('sku', 'category', 'sortorder', 'baseprice', updated, created, 'published')
    list_editable = ('sortorder',)
    search_fields = ('name', 'description', 'blurb', 'features') # 'title', - only adds 'eracks' over the sku
    #filter_horizontal = ('category',) #  can't find fm m2m, have 2 define
    filter_horizontal = ('options','images')
    list_per_page = 50
    change_form_template = 'admin_product_change_form.html'
    change_form_template = 'admin_wysiwyg_change_form.html'
    save_as = True
    actions = [publish, unpublish]
    #inlines = [ImageInline] nope, its m2m

    # this is necessary otherwise it doesn't show up (likely because it's a "through" model)
    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name in (list(self.filter_vertical) + list(self.filter_horizontal)):
            kwargs['widget'] = FilteredSelectMultiple(db_field.verbose_name, (db_field.name in self.filter_vertical))

        return db_field.formfield(**kwargs)

    # nope, image is a charfield
    #formfield_overrides = {
    #    models.ImageField: {'widget': ClearableFileInput},
    #}


#### Option admin

def option_prodopt_refs (instance):
    if instance:
        pos = Prodopt.objects.filter (option=instance, product__published=True)
        c = pos.count()

        if c:
            if c==1:
                po = pos[0]
                return link (po.calc_name,
                    href='/admin/products/prodopt/%s' % po.id,
                    title='Go to the prodopt which references this option: %s' % po)
            else:
                return link ("%s prodopts" % c,
                    href='/admin/products/prodopt/?option__id__exact=%s' % instance.id,
                    title='Go to the list of prodopts which reference this option' )
        return 'None'

option_prodopt_refs.short_description = 'ProdOpts'
option_prodopt_refs.description = 'Prodopts which reference this option'
option_prodopt_refs.allow_tags = True

class OptionAdmin (admin.ModelAdmin):
    def choices_link (self, instance):
        if instance:
            choices = instance.choices.all()
            c = choices.count()

            if c:
                if c==1:
                    choice = choices[0]
                    return link (choice.name,
                        href='/admin/products/choice/%s' % choice.id,  # could double-check this matches defaultchoice, here
                        title='Go to the choice referenced by this prodopt: %s' % instance)
                else:
                    return link ("%s choices" % c,
                        href='/admin/products/choice/?options__id__exact=%s' % instance.id,
                        title="Go to the list of choices which are referenced by this option: %s :\n%s" % (instance, '\n'.join (choices.values_list ('name', flat=True))))
            return 'None'

    choices_link.short_description = 'Choices'
    choices_link.description = "Choices referenced by this Option"
    choices_link.allow_tags = True

    def lookup_allowed(self, key, value):
        #if key in ('prodopt__product__sku', 'choices__id__exact', ):
        # add updated__year 11/7/13 jjw
        # also updated__lt, sortorder
        return True

    date_hierarchy = 'updated'
    list_display = ('name', 'usage_notes', option_prodopt_refs, 'choices_link', 'published', 'sortorder', updated, created)
    list_filter = ('updated', 'created', 'sortorder','published')
    list_editable = ('sortorder', 'published')
    list_per_page = 50
    change_form_template = 'admin_option_change_form.html'
    filter_horizontal = ('choices',)
    search_fields = ('name','usage_notes')
    readonly_fields = ('created','updated')
    save_as = True

    fieldsets = (
        (None, { 'fields': (('name', 'usage_notes', 'sortorder'),
                            ('created', 'updated'),
                            )   }),
        ('Blurb',       { 'fields': ('blurb',),       'classes': ('collapse', ), }),
        ('Description', { 'fields': ('description',), 'classes': ('collapse', 'edit'), }),
        ('Comments',    { 'fields': ('comments',),    'classes': ('collapse', ), }),
        ('Choices',     { 'fields': ('choices',),     'classes': ('wide', ), }),
    )


#### Choice admin

def default_refs (instance):
    if instance:
        pos = Prodopt.objects.filter (defaultchoice=instance, product__published=True)
        c = pos.count()

        if c:
            if c==1:
                po = pos[0]
                return link (po.calc_name,
                    href='/admin/products/prodopt/%s' % po.id,
                    title='Go to the prodopt for this choice: %s' % po)
            else:
                return link ('%s defaults' % c,
                    href='/admin/products/prodopt/?defaultchoice__id__exact=%s' % instance.id,
                    title='Go to prodopts that have this default choice')
        return 'None'

default_refs.short_description = 'Defaults'
default_refs.description = 'Published prodopts where I am a default choice'
#is_default_count.admin_order_field = 'modified'
default_refs.allow_tags = True


# deprecated - use ProdOpt_refs instead..
def poc_count (instance):
    if instance:
        pocs = Prodoptchoice.objects.filter (choice=instance, productoption__product__published=True)
        c = pocs.count()

        if c:
            if c==1:
                poc = pocs[0]
                return link (poc,
                    href='/admin/products/prodoptchoice/%s' % poc.id,
                    title='Used to go to the prodoptchoice - deprecated')
            else:
                return link ("%s poc's" % c,
                    href='/admin/products/prodoptchoice/?choice__id__exact=%s' % instance.id,
                    title='Used to go to the list of these prodoptchoices - deprecated')
        return 'None'

poc_count.short_description = 'PocCnt'
poc_count.description = 'Count of prodoptchoices of published products where I am a choice'
poc_count.allow_tags = True


def prodopt_refs (instance):
    if instance:
        pos = Prodopt.objects.filter (choices=instance, product__published=True)
        c = pos.count()

        if c:
            if c==1:
                po = pos[0]
                return link (po.calc_name,
                    href='/admin/products/prodopt/%s' % po.id,
                    title='Go to the prodopt which references this choice: %s' % po)
            else:
                return link ("%s prodopts" % c,
                    href='/admin/products/prodopt/?choices__id__exact=%s' % instance.id,
                    title='Go to the list of prodopts which reference this choice' )
        return 'None'

prodopt_refs.short_description = 'ProdOpts'
prodopt_refs.description = 'Prodopts of published products where I am a choice'
prodopt_refs.allow_tags = True


def option_refs (instance):
    if instance:
        options = Option.objects.filter (choices=instance) # , productoption__product__published=True)
        c = options.count()

        if c:
            if c==1:
                option = options [0]
                return link (option.name,
                    href='/admin/products/option/%s' % option.id,
                    title='Go to the option which references this choice: %s' % option)
            else:
                return link ("%s option%s" % (c, '' if c==1 else 's'),
                    href='/admin/products/option/?choices__id__exact=%s' % instance.id,
                    title='Go to the list of these options')
        return 'None'

option_refs.short_description = 'Options'
option_refs.description = 'Option(s) that reference this choice'
option_refs.allow_tags = True


class ChoiceForm (ModelForm):
    def __init__ (self, *args, **kw):
        super (ChoiceForm, self).__init__ (*args, **kw)
        #self.fields['choicecategory'].widget.widget = FilteredSelectSingle (verbose_name='ChoiceCategory')
        self.fields['choicecategory'].widget = FilteredSelectSingle # (verbose_name='ChoiceCategory')

class ChoiceAdmin (admin.ModelAdmin):
    #def lookup_allowed(self, key, value):
    #    return True

    date_hierarchy = 'updated'
    search_fields = ('name', 'comment', 'sortorder') # 'choicecategory__name')
    #list_display = ('id', 'name', 'sortorder', default_refs, option_refs, prodopt_refs, poc_count, 'comment','cost',updated, 'published')
    list_display = ('id', 'name', 'choicecategory','sortorder', default_refs, option_refs, prodopt_refs, 'blurb', 'comment','cost', created, updated, 'published')
    list_filter = ('updated', 'created', 'published', 'multiplier', 'options', 'supplier', 'choicecategory', 'price', 'cost', 'sortorder', 'prodoptchoice__productoption')
    list_editable = ('name', 'choicecategory', 'cost', 'sortorder', 'published', 'blurb', 'comment')
    list_per_page = 50
    save_as = True
    actions = [publish, unpublish]
    filter_horizontal = ('options',)
    view_on_site = True  # doesn't show under Grappelli, for some reason - JJW
    form = ChoiceForm

    #formfield_overrides = {
        #models.ForeignKey: {'widget': FilteredSelectSingle},
    #}

    def not_formfield_for_foreignkey (self, db_field, request=None, **kwargs):
        #if db_field.name == "car":
        #    kwargs["queryset"] = Car.objects.filter(owner=request.user)
        print 'db_field:', db_field #, dir(db_field)
    #    print 'request:', request
        print 'kwargs:', kwargs
        kwargs.update (widget=FilteredSelectSingle (verbose_name='blah',))
        #print 'widget:', db_field.widget
        #db_field.widget.widget=FilteredSelectSingle

        db = kwargs.get ('using')
        print 'db:', db

        if 'queryset' not in kwargs:
            kwargs ['queryset'] = ChoiceCategory.objects.all() # self.get_field_queryset (db, db_field, request)

        print 'kwargs:', kwargs

        return db_field.formfield (**kwargs)
        return super(ChoiceAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    #    return admin.ModelAdmin.formfield_for_foreignkey (self, db_field, request, **kwargs)



# NFG:
# in the comments: http://chase-seibert.github.io/blog/2010/05/14/reuse-djangos-filter_horizontal-admin-widget.html

#posts_field = forms.ModelMultipleChoiceField(
#    queryset=Post.objects.all(),
#    widget=FilteredSelectMultiple("Posts", is_stacked=False))


# JJW - see http://www.lasolution.be/blog/related-manytomanyfield-django-admin-site.html

class CCatForm (ModelForm):
    choices = ModelMultipleChoiceField (
            Choice.objects.all(),
            # Add this line to use the double list widget
            widget = FilteredSelectMultiple ('Choices', False),
            required = False,
        )

    def __init__ (self, *args, **kwargs):
        super (CCatForm, self).__init__ (*args, **kwargs)
        #ModelForm.__init__ (self, *args, **kwargs)
        #print 'instance:', self.instance
        #if self.instance and isinstance (self.instance, Category):
        #  inst=self.instance
        #  dc=self.fields.get('defaultchoice')
        #  if trace: print inst.all_choices # option_id # dir (inst)
        #  if inst.pk and inst.all_choices().count():
        #    dc.queryset = inst.all_choices()  #Choice.objects.filter (id__in = inst.choices.values_list('id', flat=True))
        if self.instance.pk:
            # if this is not a new object, we load related books
            self.initial['choices'] = self.instance.choice_set.values_list('pk', flat=True)
            #rel = ManyToManyRel(Choice)
            #self.fields['choice'].widget = RelatedFieldWidgetWrapper(self.fields['choice'].widget, rel, admin.site)

    def save(self, *args, **kwargs):
        instance = super (CCatForm, self).save (*args, **kwargs)

        if instance.pk:
            for choice in instance.choice_set.all():
                if choice not in self.cleaned_data['choices']:
                    # we remove choice which has been unselected
                    # m2m:
                    #instance.choice_set.remove(choice)
                    # fk:
                    choice.choicecategory = get_misc_choice_category()  # set to Misc - 43882 :)
                    choice.save()

            for choice in self.cleaned_data['choices']:
                if choice not in instance.choice_set.all():
                    # we add newly selected choice
                    # m2m:
                    #instance.choice_set.add(choice)
                    # fk:
                    choice.choicecategory = instance
                    choice.save()

        return instance

    #class Meta:
    #    model = ChoiceCategory
    #    widgets = { 'choice_set', FilteredSelectMultiple("Choices verbose name", is_stacked=False) }


def choice_refs (instance):
    if instance:
        choices = instance.choice_set
        c = choices.count()

        if c:
            if c==1:
                choice = choices.all() [0]
                return link (choice.name,
                    href='/admin/products/choice/%s' % choice.id,
                    title='Go to this choice: %s' % choice)
            else:
                return link ("%s choice%s" % (c, '' if c==1 else 's'),
                    href='/admin/products/choice/?choicecategory__id__exact=%s' % instance.id,
                    title='Go to the list of these choices: ' + '\n'.join (escape (v) for v in choices.values_list('name', flat=True)))
        return 'None'

choice_refs.short_description = 'Choices'
choice_refs.description = 'Choice(s) that this ChoiceCateogery include'
choice_refs.allow_tags = True

class ChoiceCategoryAdmin (admin.ModelAdmin):
    #def choices (self, obj):
    #    return obj.choice_set.all()
    #choices.allow_tags=True

    date_hierarchy = 'updated'
    search_fields = ('name','abbrev')
    list_display = ('id','name','abbrev','solow','sohigh', 'parent', 'published', updated, created, choice_refs)  #'choices') # 'choice_set',)
    list_filter = ('updated','created','published','parent','solow','sohigh')
    list_editable = ('name','abbrev','parent','published')  # 'solow','sohigh'
    list_display_links = ('id',)
    list_per_page = 50
    save_as = True
    view_on_site = True
    form = CCatForm


### register all relevant admins

# out 10/14/13 JJW? nope, m2m
admin.site.register (Image, ImageAdmin)
admin.site.register (Categories, CategoryAdmin)

# monkey patch! Kluge alert!

# JJW commented out - do we still need this?  JJW 10/11/14
#from django.contrib.admin import validation
#saved_validate = validation.validate
#validation.validate = lambda model, adminclass: None

admin.site.register (Product, ProductAdmin)
admin.site.register (Prodopt, ProdoptAdmin)

#validation.validate = saved_validate


# merged w/prodopt 10/14/13 JJW
#admin.site.register (ProductOption, ProductOptionAdmin)

# NLN JJW 20/13
#admin.site.register (Prodoptchoice, ProdoptchoiceAdmin)

admin.site.register (Option, OptionAdmin)
admin.site.register (Choice, ChoiceAdmin)
admin.site.register (ChoiceCategory, ChoiceCategoryAdmin)

#admin.site.register ([Optchoices])  #, Optionchoices])

