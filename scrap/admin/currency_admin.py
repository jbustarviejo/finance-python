from django.contrib import admin
from django.utils.html import format_html

from scrap.models import Currency
from scrap.actions import ExportCsvMixin

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('name', 'symbol', 'xid_to_usd', 'xid_from_usd', 'history_updated_at', 'updated_at', 'created_at')
    search_fields = ['name', 'symbol']
    list_filter = ('updated_at', 'created_at')
    actions = ['export_as_csv']
