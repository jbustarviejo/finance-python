from django.contrib import admin
from django.utils.html import format_html

from scrap.models import Industry
from scrap.actions import ExportCsvMixin

@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('name', 'show_link', 'sector_id','updated_at', 'created_at')
    search_fields = ['name', 'slug']
    list_filter = ('updated_at', 'created_at')
    actions = ['export_as_csv']

    def show_link(self, obj):
        return format_html('<a target="blank" href="{}">{}</a>',obj.link, obj.link)
