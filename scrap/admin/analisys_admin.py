from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html

from scrap.models import Analisys
from scrap.actions import ExportCsvMixin

@admin.register(Analisys)
class AnalisysAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('company', 'kernel', 'svm', 'rate', 'number_of_days_sample', 'number_of_train_vectors', 'created_at')
    search_fields = ['kernel', 'svm']
    list_filter = ('kernel', 'svm')
    actions = ['export_as_csv']
