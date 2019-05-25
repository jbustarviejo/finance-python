from django.contrib import admin

from scrap.models import Sector
from scrap.actions import ExportCsvMixin


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('name', 'slug', 'updated_at', 'created_at')
    search_fields = ['name', 'slug']
    list_filter = ('updated_at', 'created_at')
    actions = ['export_as_csv']
