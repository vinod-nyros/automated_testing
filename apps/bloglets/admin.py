# encoding: utf-8

#from __future__ import absolute_import

from django.contrib import admin

from bloglets.models import Post, Category
from apps.utils import created, updated, publish, unpublish


post_categories = lambda x: ', '.join ([str(c) for c in x.categories.all()])
post_categories.short_description = 'Categories'
#post_categories.admin_order_field = 'admin order field'


class PostAdmin (admin.ModelAdmin):
    # NFG - pub_date doesn't show.
    #fields = ('title', 'slug', 'published', 'pub_date', 'body', 'author', 'categories')
    date_hierarchy = 'created'
    list_display = ['title', post_categories, 'published', 'pub_date', 'author', updated, created] # 'tags']
    prepopulated_fields = { 'slug': ('title',) }
    search_fields = ['title', 'body']
    list_filter = ['published', 'pub_date', 'updated', 'categories', 'author'] # , 'tags'] nope - doesn't work
    filter_horizontal = ['categories']
    actions = (publish, unpublish)
    save_as = True


class CategoryAdmin (admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ['title', 'published', updated, created]
    prepopulated_fields = { 'slug': ('title',) }
    list_filter = ['published', 'created', 'updated']
    search_fields = ['title', 'slug']
    actions = (publish, unpublish)


admin.site.register (Post, PostAdmin)
admin.site.register (Category, CategoryAdmin)

