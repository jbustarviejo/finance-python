from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html

from scrap.models import Analisys
from scrap.actions import ExportCsvMixin

@admin.register(Analisys)
class AnalisysAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('company', 'svm', 'kernel', 'rate', 'fractal_points', 'number_of_days_sample', 'created_at')
    list_filter = ('kernel', 'svm')
    actions = ['export_as_csv']
    readonly_fields = ('company',)
