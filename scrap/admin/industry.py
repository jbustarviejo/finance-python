from django.contrib import admin

from scrap.models import Industry
from scrap.actions import ExportCsvMixin

@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('name', 'slug', 'sector_id','updated_at', 'created_at')
    search_fields = ['name', 'slug']
    list_filter = ('updated_at', 'created_at')
    actions = ['export_as_csv']
