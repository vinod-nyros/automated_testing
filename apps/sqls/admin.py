from django.contrib import admin
from .models import Sql


class SqlAdmin (admin.ModelAdmin):
    def description_ (self, obj):
        if len(obj.description) > 50:
            return obj.description [:50] + ' ...'
        else:
            return obj.description

    def sql_ (self, obj):
        if len(obj.sql) > 80:
            return obj.sql [:80] + ' ...'
        else:
            return obj.sql

    # nope, shows as 'true' not red/green: def inq (self, obj): return True  #not obj.updates
    def u (self, obj):
        if obj.updates:
            tupl = ('red','Y')
        else:
            tupl = ('green','N')

        return '<span style="color:%s">%s</span>' % tupl
    u.allow_tags = True
    u.admin_order_field = 'updates'

    fieldsets = (
        (None, { 'fields': (('description', 'updates',),
                            ('sql',),
                            )   }),
        #('Params', { 'fields': ('parm1','parm2','parm3','parm4','parm5',), 'classes': ('collapse',), }),
        #('Notes',  { 'fields': ('notes',), 'classes': ('collapse',), }),
        ('Params', { 'fields': ('parm1','parm2','parm3','parm4','parm5',), }),
        ('Notes',  { 'fields': ('notes',), }),
    )

    list_filter = ('created', 'modified', 'updates', 'parm1','parm2','parm3')  #, 'description')
    list_display = ('description_', 'u', 'sql_', 'modified',)
    list_per_page = 50
    search_fields = ('description','sql')
    date_hierarchy = 'created'
    change_form_template = 'admin_change_form.html'
    change_list_template = 'admin_change_list.html'
    save_on_top = True
    save_as = True

    #class Media:
        #css = { "all": ("my_styles.css",)  }
        #js = ("/js/jquery.js",)

admin.site.register (Sql, SqlAdmin)
