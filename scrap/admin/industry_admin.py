from django.db.models import Count
from django.contrib import admin
from django.utils.html import format_html

from scrap.models import Industry
from scrap.actions import ExportCsvMixin

@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('name', 'sector', 'industry_link', 'companies_count', 'updated_at', 'created_at')
    search_fields = ['name', 'slug']
    list_filter = ('updated_at', 'created_at', 'sector')
    actions = ['export_as_csv']

    def industry_link(self, obj):
        return format_html('<a target="blank" href="{}">{}</a>',obj.link, obj.link)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _companies_count=Count("companies", distinct=True)
        )
        return queryset

    def companies_count(self, obj):
        return obj._companies_count

    companies_count.admin_order_field = '_companies_count'
