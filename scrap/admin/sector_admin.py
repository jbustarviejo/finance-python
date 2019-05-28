from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html

from scrap.models import Sector
from scrap.actions import ExportCsvMixin

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('name', 'industries_count', 'sector_link', 'updated_at', 'created_at')
    search_fields = ['name', 'slug']
    list_filter = ('updated_at', 'created_at')
    readonly_fields = ('link',)
    actions = ['export_as_csv']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _industries_count=Count("industries", distinct=True)
        )
        return queryset

    def industries_count(self, obj):
        return obj._industries_count

    industries_count.admin_order_field = '_industries_count'

    def sector_link(self, obj):
        return format_html('<a target="blank" href="{}">{}</a>',obj.link, obj.link)
