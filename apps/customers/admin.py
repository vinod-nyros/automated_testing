#from django.db import models
#from django.contrib.auth.models import User
from django.contrib import admin

from customers.models import Address, CustomerImage, Customer, Testimonial
from orders.models import Order
from apps.utils import modified, created, updated, publish, unpublish


#### Globals

trace = 0


#### Admin

class AddressInline (admin.StackedInline):
    model = Address
    extra = 0

    #formfield_overrides = {
    #    models.CharField: { 'widget': DropDownMultiple },
    #}


class OrderInline (admin.StackedInline):
    model = Order
    extra = 0


class CustomerAdmin (admin.ModelAdmin):
    list_display = ('user', 'organization', 'title','department','email','phone', 'comments', 'default_shipping', created, updated) #, 'address_set')
    list_display_links = ('user', 'organization', 'email')
    # nope: list_editable = ('comments',)
    list_filter = ('created','updated','department',)
    search_fields = ('user__username', 'organization','comments', 'title','department', 'email', 'phone', 'email2', 'phone2')
    list_per_page = 50
    save_as = True
    readonly_fields = ('created','updated', 'user')

    inlines = [AddressInline, OrderInline]


class CustomerImageAdmin (admin.ModelAdmin):
    list_display = ('caption', 'location', 'published', 'sortorder', created, updated)
    list_filter = ('published','created','updated')
    search_fields = ('caption','location','link', 'title')
    list_editable = ('sortorder',)
    list_per_page = 50
    save_as = True
    actions = [publish, unpublish]
    readonly_fields = ('created','updated')

    #class Media:
    #    js = (reverse_lazy('bfm_opt'),)


class TestimonialAdmin (admin.ModelAdmin):
    list_display = ('quote', 'attribution','published', 'sortorder', created, updated)
    list_filter = ('published', 'created','updated')
    search_fields = ('quote','attribution')
    list_editable = ('sortorder',)
    list_per_page = 50
    save_as = True
    actions = [publish, unpublish]
    readonly_fields = ('created','updated')


# register admin objs

#now done by userena:
#try:
#    admin.site.unregister (Customer)
#except Exception, e:
#    print e

# so add Customer2
#class Customer2 (Customer):
#    class Meta:
#        proxy = True   # db_table = "product_category"
#        verbose_name = 'eRacks Customer'
#        verbose_name_plural = 'eRacks Customer'

#from userena import admin
#admin.site.unregister (Customer)
#admin.site.register (Customer, CustomerAdmin)
admin.site.register (CustomerImage, CustomerImageAdmin)
admin.site.register (Testimonial, TestimonialAdmin)
#admin.site.register (Address, AddressAdmin)
