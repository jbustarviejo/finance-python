from django.contrib import admin
from django.utils.html import format_html

from scrap.models import Company
from scrap.actions import ExportCsvMixin

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('name', 'symbol', 'currency', 'xid', 'show_link', 'industry','updated_at', 'created_at')
    search_fields = ['name', 'symbol']
    list_filter = ('updated_at', 'created_at', 'industry')
    actions = ['export_as_csv']

    def show_link(self, obj):
        return format_html('<a target="blank" href="{}">{}</a>',obj.link, obj.link)
