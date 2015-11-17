from django.contrib import admin
from .models import Quote, QuoteLineItem

#class LineItemInline(admin.TabularInline):
class LineItemInline(admin.StackedInline):
    model = QuoteLineItem
    extra = 1

class QuoteAdmin (admin.ModelAdmin):
    list_display = ('quote_number', 'customer','valid_for','customer_reference','target','created','modified')
    list_filter = ('created','modified','approved_by','customer',)
    #list_editable = ('closed','purchase_order')
    search_fields = ('quote_number', 'customer__user__username','customer__email','purchase_order',
                     'customer_reference','comments','quotelineitem__description', 'quotelineitem__comments')
    list_per_page = 50
    save_as = True

    fieldsets = (
        (None, { 'fields': (('customer', 'quote_number', 'approved_by',),
                            ('valid_for', 'purchase_order', 'customer_reference',),
                            ('terms', 'discount', 'discount_type'),
                            ('shipping', 'shipping_method','comments'),
                            ('target','image')
                            )   }),
        #('Description', { 'fields': ('description',), 'classes': ('collapse', 'edit'), }),
    )

    inlines = [LineItemInline]


# register admin objs

admin.site.register (Quote, QuoteAdmin)
#admin.site.register (Customer, CustomerAdmin)
#admin.site.register (QuoteLineItem, QuoteLineItemAdmin)
