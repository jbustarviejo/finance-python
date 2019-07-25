from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html

from scrap.models import Analisys
from scrap.actions import ExportCsvMixin

@admin.register(Analisys)
class AnalisysAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('company', 'svm', 'degree', 'rate', 'number_of_days_sample', 'created_at')
    list_filter = ('degree', 'svm')
    actions = ['export_as_csv']
