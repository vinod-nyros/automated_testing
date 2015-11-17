# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ModelForm   #ModelMultipleChoiceField #ModelChoiceField #, Form

from sqls.minitags import a as link
from models import Image, Categories, Prodopt, Product, Prodoptchoice, Option, Choice, ChoiceCategory #, Optchoices

from utils import modified, created, updated, publish, unpublish


#### globals

trace = 0


#### Admin classes

class ImageAdmin (admin.ModelAdmin):
    date_hierarchy = 'updated'
    list_display = ('image', 'title', 'caption', updated, created,'published')
    list_filter = ('updated', 'created','published')
    actions = [publish, unpublish]


class CategoryAdmin (admin.ModelAdmin):
    change_form_template = 'admin_wysiwyg_change_form.html'

    date_hierarchy = 'updated'
    list_display = ('name', 'title', 'blurb','sortorder', updated, created,'published')
    list_filter = ('updated','created','published')
    #list_editable = ('title','blurb','sortorder',)  # 'name', doesn't work - can't be both clickable and editable
    list_editable = ('title','sortorder',)  # 'name', doesn't work - can't be both clickable and editable
    list_display_links = ('id','name')
    list_per_page = 50
    save_as = True
    prepopulated_fields = {"slug": ("name","title",)}
    actions = [publish, unpublish]
    list_horizontal = ('images',)


#### Product Option admin - new PO-OL model

class ProductOption (Prodopt):
    class Meta:
        proxy = True
        verbose_name = 'New Product Option (PO-OL model)'
        verbose_name_plural = 'New Product Options (PO-OL model)'

class ProductOptionAdmin (admin.ModelAdmin):
    list_display = ('__unicode__', 'defaultchoice', 'name', 'qty', 'single','required', 'choices_orderby', updated, created, 'published')
    readonly_fields = ('option', 'product','created','updated')
    save_on_top = True
    save_as = True
    list_filter = ('updated', 'created', 'published', 'choices_orderby', 'allowed_quantities', 'product', 'option')  # no: gives all, not just the ones that are df's: 'defaultchoice')
    actions = [publish, unpublish]

    fieldsets = (
        (None, { 'fields': (    ('name', 'published'),
                                ('product', 'option','created', 'updated',),
                            )   }),
        ('Option-related fields', { 'fields': ('qty','single','required'), 'classes': ('wide', ), }),
        ('Choice-related fields', { 'fields': ('allowed_quantities', 'choices_orderby', 'defaultchoice'), 'classes': ('wide'), }),
    )

    #TODO: restrict defaultchoice to new POOL / OC choices


#### Product Option admin - legacy PO-POC model

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

    # 'ProdoptAdmin.fieldsets[0][1]['fields']' can't include the ManyToManyField field 'choices'
    # because 'choices' manually specifies a 'through' model.
    # FIXED Mar 010 - via monkeypatch around validate - see bottom
    #fieldsets = (
    #    (None, { 'fields': (('product', 'option', ),
    #                        ('defaultchoice',),
    #                        ('choices',),
    #                        )   }),
    #)

    # ditto - but FIXED Mar 010 - via monkeypatch around validate - see bottom
    fields = ('product', 'option', 'name', 'qty', 'single', 'required','choices_orderby', 'defaultchoice', 'choices',)

    list_filter = ('updated', 'created', 'published', 'choices_orderby', 'product__published', 'product', 'option')  # no: gives all, not just the ones that are df's: 'defaultchoice')
    list_display = ('__unicode__', 'defaultchoice', 'name', 'qty', 'single','required', 'choices_orderby', updated, created, 'published')
    list_editable = ('defaultchoice',)  # CAN'T restrict to existing choices :(
    filter_horizontal = ('choices', )
    readonly_fields = ('option', 'product',)
    form = ProdoptForm
    list_per_page = 20
    change_form_template = 'admin_prodopt_change_form.html'
    save_on_top = True
    save_as = True
    actions = [publish, unpublish]

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


class ProductAdmin (admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        # We can't just do .clear(), it wipes out the 'through' data, so do careful_update..
        curr_opts = frozenset (obj.options.all())
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

    fieldsets = (
        (None, { 'fields': (('sku', 'name',),
                            ('cost', 'baseprice'),
                            ('title', 'published',),
                            ('new_grid'),
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
        #('Algorithm',   { 'fields': ('algorithm',),   'classes': ('collapse', ), }),
        ('Category',    { 'fields': ('category',),    'classes': ('wide', ), }),
        ('Options',     { 'fields': ('options',),     'classes': ('wide', ), }),
    )

    date_hierarchy = 'updated'
    list_filter = ('updated', 'created', 'published', 'category', 'baseoptions')
    list_display = ('sku', 'category', 'sortorder', 'baseprice', updated, created, 'published')
    list_editable = ('sortorder',)
    search_fields = ('name', 'description', 'blurb', 'features') # 'title', - only adds 'eracks' over the sku
    #filter_horizontal = ('category',) #  can't find fm m2m, have 2 define
    filter_horizontal = ('options',)
    list_per_page = 20
    change_form_template = 'admin_product_change_form.html'
    change_form_template = 'admin_wysiwyg_change_form.html'
    save_as = True
    actions = [publish, unpublish]

    # this is necessary otherwise it doesn't show up (likely because it's a "through" model)
    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name in (list(self.filter_vertical) + list(self.filter_horizontal)):
            kwargs['widget'] = FilteredSelectMultiple(db_field.verbose_name, (db_field.name in self.filter_vertical))

        return db_field.formfield(**kwargs)


class OptionAdmin (admin.ModelAdmin):
    date_hierarchy = 'updated'
    list_display = ('name', 'usage_notes', 'sortorder', updated, created,)
    list_filter = ('updated','created','sortorder')
    list_editable = ('sortorder',)
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

def is_default_count (instance):
    if instance:
        pos = Prodopt.objects.filter (defaultchoice=instance, product__published=True)
        c = pos.count()

        if c:
            return link ('%s defaults' % c,
                href='/admin/legacy/prodopt/?defaultchoice__id__exact=%s' % instance.id,
                title='Go to prodopts for these default choices')
        return 'None'

is_default_count.short_description = 'DefCnt'
is_default_count.description = 'Count of published prodopts where I am a default choice'
#is_default_count.admin_order_field = 'modified'
is_default_count.allow_tags = True

def poc_count (instance):
    if instance:
        pocs = Prodoptchoice.objects.filter (choice=instance, productoption__product__published=True)
        c = pocs.count()

        if c:
            return link ("%s poc's" % c,
                href='/admin/legacy/prodoptchoice/?choice__id__exact=%s' % instance.id,
                title='Go to the list of these prodoptchoices')
        return 'None'

poc_count.short_description = 'UseCnt'
poc_count.description = 'Count of prodoptchoices of published products where I am a choice'
poc_count.allow_tags = True

class ChoiceAdmin (admin.ModelAdmin):
    date_hierarchy = 'updated'
    search_fields = ('name','comment') # 'choicecategory__name')
    list_display = ('id', 'name', 'sortorder', is_default_count, poc_count, 'comment','cost',updated, 'published')
    list_filter = ('updated','created','published','multiplier','supplier','choicecategory','price','cost','sortorder')
    list_editable = ('name', 'cost','sortorder','published','comment')
    list_per_page = 20 # 50
    save_as = True
    actions = [publish, unpublish]


class ChoiceCategoryAdmin (admin.ModelAdmin):
    date_hierarchy = 'updated'
    list_display = ('id','name', 'solow','sohigh', updated, created,)
    list_filter = ('updated','created','solow','sohigh')
    list_editable = ('name','solow','sohigh')
    list_display_links = ('id',)
    list_per_page = 50
    save_as = True


### register all relevant admins

# monkey patch! Kluge alert!

from django.contrib.admin import validation
saved_validate = validation.validate
validation.validate = lambda model, adminclass: None

admin.site.register (Image, ImageAdmin)
admin.site.register (Categories, CategoryAdmin)
admin.site.register (Product, ProductAdmin)
admin.site.register (Prodopt, ProdoptAdmin)

validation.validate = saved_validate

admin.site.register (ProductOption, ProductOptionAdmin)

admin.site.register (Prodoptchoice, ProdoptchoiceAdmin)
admin.site.register (Option, OptionAdmin)
admin.site.register (Choice, ChoiceAdmin)
admin.site.register (ChoiceCategory, ChoiceCategoryAdmin)

#admin.site.register ([Optchoices])  #, Optionchoices])

