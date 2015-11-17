from django.contrib import admin
from apps.utils import created, updated
from .models import Catax

class CataxAdmin (admin.ModelAdmin):
    list_display = ('name', 'tax','count',created, updated)
    list_filter = ('created','updated','tax', 'county', 'count',)
    list_per_page = 50
    save_as = True


admin.site.register (Catax, CataxAdmin)


