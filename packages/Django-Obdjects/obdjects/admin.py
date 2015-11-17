from django.contrib import admin
from codemirror2.widgets import CodeMirrorEditor
from .models import Snippet

class SnippetAdmin (admin.ModelAdmin):
    #form = TemplateAdminForm

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.attname == "body":
            kwargs ['widget'] = CodeMirrorEditor (
                options = {'mode': 'htmlmixed'},
                modes = ['css', 'xml', 'javascript', 'htmlmixed']
            )

        return super (SnippetAdmin, self).formfield_for_dbfield (db_field, **kwargs)

    fieldsets = (
        (None, { 'fields': (('name', 'title', 'published'),) }),
        ('Body', { 'fields': ('body',), 'classes': ('codemirroreditor',), }),  # 'collapse',
    )
    #fields = ('title', 'slug', 'published', 'pub_date', 'body', 'author', 'categories')
    date_hierarchy = 'updated'
    list_display = ['name', 'title', 'published', 'updated']
    #prepopulated_fields = { 'slug': ('name',) }
    search_fields = ['name', 'title', 'body',]
    list_filter = ['published', 'created', 'updated', ]
    #filter_horizontal = ['meta']

    # perhaps do it this way:  https://github.com/pydanny/django-wysiwyg
    #class Media:
    #    css = { "all": ('/static/codemirror2/codemirror.css',) }
    #    js  = ( '/static/codemirror2/codemirror.js',
    #            '/static/obdjects/js/codemirror_init.js',
    #    )


admin.site.register (Snippet, SnippetAdmin)
