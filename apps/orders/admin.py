# -*- coding: utf-8 -*-

from django.contrib import admin
from apps.utils import created, updated #, publish, unpublish, modified,
from .models import Order, ImportedOrder, ImportedOrderLine, OrderPayment
from customers.models import Customer  #,Address
#from customers.admin import AddressInline
from sqls.minitags import a as link

### helper functions - inline links, etc

def customer_link (instance):
    if instance:
        cust = instance.customer
        return link (cust,
            href='/admin/customers/customer/%s' % cust.id,
            title='Go to the customer for Order #%s: %s' % (instance.id, cust))
    return 'None'

customer_link.short_description = 'Customer'
customer_link.description = 'Customer referenced by this Order'
customer_link.allow_tags = True


#### Admin

#class ImportedOrderLineAdmin (admin.StackedInline):
class ImportedOrderLineAdmin (admin.TabularInline):
    model = ImportedOrderLine
    extra = 0


class ImportedOrderAdmin (admin.ModelAdmin):
    list_display = ('id', 'title','billname', 'billorg', 'refnum','orderstatus', 'orderdate')
    list_filter = ('orderstatus', 'orderdate',
                    'shipmethod', 'shipper','shippay','shipcountry',
                    'billcountry','billinitials','saleinitials', 'shipinitials','payinitials','cc_initials',
                    'paymeth','payterms',
                    'reftyp', 'refsrc',
                )
    search_fields = ('billname','billorg','billaddr1','billaddr2','billcity','billregn','billphone',
                    'shipname','shiporg','shipaddr1','shipaddr2','shipcity','shipregn','shipphone',
                    'email','title','refnum','instr','internalnotes','adjustments','tracknumbers',
                    )
    list_per_page = 50
    inlines = [ImportedOrderLineAdmin]
    save_as = True


class PaymentInline (admin.TabularInline):
    model = OrderPayment
    readonly_fields = ('user',)
    extra = 0


class OrderAdmin (admin.ModelAdmin):
    fieldsets = (
        (None, { 'fields': (('customer', 'ship_to_address', 'bill_to_address', 'agree_to_terms'),
                        ('reference_number','shipping','shipping_method','preferred_shipper','shipping_payment',),
                        ('referral_type','referral_source'),
                        ('status','source','processed','california_tax',)
                    ),
            }),
        ('Advanced options', { 'fields': ('special_instructions', 'cart', 'comment'),
                'classes': ('collapse',),
            }),
    )
    #list_display = ('id', 'customer','reference_number','status', 'ship_to_address', 'bill_to_address', created, updated)
    list_display = ('id', customer_link,'reference_number','status', 'ship_to_address', 'bill_to_address', created, updated)
    list_filter = ('created','updated','status', 'shipping_method', 'preferred_shipper',
                   'shipping_payment', 'referral_type', 'referral_source',
                )
    search_fields = ('customer__organization', 'customer__user__username', 'customer__user__first_name', 'customer__user__last_name',
        'ship_to_address__name', 'ship_to_address__address1', 'ship_to_address__address2', 'ship_to_address__city','ship_to_address__state', 'ship_to_address__zip',
        'bill_to_address__name', 'bill_to_address__address1', 'bill_to_address__address2', 'bill_to_address__city','bill_to_address__state', 'bill_to_address__zip',
        'reference_number','status',
        )
    readonly_fields = ('customer', 'ship_to_address','bill_to_address','agree_to_terms','source')

    list_per_page = 50
    save_as = True

    inlines = (PaymentInline,)
    #inlines = (PaymentInline, CustomerInline)


'''
class OrderLineItemAdmin (admin.ModelAdmin):
    list_display = ('caption', 'location', 'published', 'sortorder', created, updated)
    list_filter = ('published','created','updated')
    search_fields = ('caption','location','link', 'title')
    list_editable = ('sortorder',)
    list_per_page = 50
    save_as = True
    actions = [publish, unpublish]
'''


#### Register all relevant Admins

admin.site.register (ImportedOrder, ImportedOrderAdmin)
admin.site.register (Order, OrderAdmin)





second_attempt='''
120813_NFG_still_need_more_deep_dive_into_formset_factories

from django.forms.models import BaseInlineFormSet
class CustomerInlineFormSet(BaseInlineFormSet):
    def __init__(self, data=None, files=None, instance=None,
                 save_as_new=False, prefix=None, queryset=None, **kwargs):
        from django.db.models.fields.related import RelatedObject
        if instance is None:
            self.instance = self.fk.rel.to()
        else:
            self.instance = instance
        self.save_as_new = save_as_new
        # is there a better way to get the object descriptor?
        self.rel_name = 'orders' #RelatedObject(self.fk.rel.to, self.model, self.fk).get_accessor_name()
        if queryset is None:
            queryset = self.model._default_manager
        if self.instance.pk:
            #qs = queryset.filter(**{self.fk.name: self.instance})
            qs = queryset.filter(**{'orders': self.instance})
        else:
            qs = queryset.filter(pk__in=[])

        print 'INSTANCE', self.instance
        print 'FK', self.fk, self.fk.name

        #self.fk.name = 'orders' # kluge / monkey patch to fool other methods
        self.fk.verbose_name = 'orders' # kluge / monkey patch to fool other methods

        super(BaseInlineFormSet, self).__init__(data, files, prefix=prefix,
                                                queryset=qs, **kwargs)

    #@property
    def _media (self):
        print 'MEDIA', self.form.media
        return self.form.media

    # shortened from django forms models 760
    def add_fields(self, form, index):
        super(BaseInlineFormSet, self).add_fields(form, index)

    # shortened from django forms models 730
    def _construct_form(self, i, **kwargs):
        form = super(BaseInlineFormSet, self)._construct_form(i, **kwargs)

    @classmethod
    def get_default_prefix(cls):
        return 'orders'
        #from django.db.models.fields.related import RelatedObject
        #return RelatedObject(cls.fk.rel.to, cls.model, cls.fk).get_accessor_name().replace('+','')


# NFG 7/2/13 JJW :-(
#
class CustomerInline (admin.StackedInline):
    #def get_queryset(self, request):
    #    self.parent_model.
        #qs = Customer.objects.filter (
        #qs = super(MyModelAdmin, self).get_queryset(request)
        #if request.user.is_superuser:
        #    return qs
        #return qs.filter(author=request.user)

    model = Customer
    formset = CustomerInlineFormSet

#    readonly_fields = ('order_set',)
#    model = Order
#    fk_name = 'Order.customer'
#    fk_name = 'order'  # 'order'  'order_set'
    #fk_name = 'orders'
    extra = 0

    # see django.contrib.admin.options 1440
    def get_formset(self, request, obj=None, **kwargs):
        """Returns a BaseInlineFormSet class for use in admin add/change views."""
        if self.declared_fieldsets:
            fields = flatten_fieldsets(self.declared_fieldsets)
        else:
            fields = None
        if self.exclude is None:
            exclude = []
        else:
            exclude = list(self.exclude)
        exclude.extend(self.get_readonly_fields(request, obj))
        if self.exclude is None and hasattr(self.form, '_meta') and self.form._meta.exclude:
            # Take the custom ModelForm's Meta.exclude into account only if the
            # InlineModelAdmin doesn't define its own.
            exclude.extend(self.form._meta.exclude)
        # if exclude is an empty list we use None, since that's the actual
        # default
        exclude = exclude or None
        can_delete = self.can_delete and self.has_delete_permission(request, obj)

        from functools import partial

        defaults = {
            "form": self.form,
            "formset": self.formset,
            #"fk_name": self.fk_name,
            "fields": fields,
            "exclude": exclude,
            "formfield_callback": partial(self.formfield_for_dbfield, request=request),
            "extra": self.extra,
            "max_num": self.max_num,
            "can_delete": can_delete,
        }
        defaults.update(kwargs)
        # JJW return inlineformset_factory(self.parent_model, self.model, **defaults)

    #included inline from django.forms.models 829
    #def inlineformset_factory(parent_model, model, form=ModelForm,
    #                      formset=BaseInlineFormSet, fk_name=None,
    #                      fields=None, exclude=None,
    #                      extra=3, can_order=False, can_delete=True, max_num=None,
    #                      formfield_callback=None):
    #"""
    #Returns an ``InlineFormSet`` for the given kwargs.
    #
    #You must provide ``fk_name`` if ``model`` has more than one ``ForeignKey``
    #to ``parent_model``.
    #"""
    #fk = _get_foreign_key(parent_model, model, fk_name=fk_name)
    # enforce a max_num=1 when the foreign key to the parent model is unique.
    #if fk.unique:
    #    max_num = 1

        #kwargs = {
        #    'form': form,
        #    'formfield_callback': formfield_callback,
        #    'formset': formset,
        #    'extra': extra,
        #    'can_delete': can_delete,
        #    'can_order': can_order,
        #    'fields': fields,
        #    'exclude': exclude,
        #    'max_num': max_num,
        #}

        from django.forms.models import modelformset_factory
        #FormSet = modelformset_factory(model, **kwargs)
        FormSet = modelformset_factory(self.model, **defaults)
        FormSet.fk = Customer._meta.get_field_by_name ('orders')[0] #fk
        return FormSet
'''

