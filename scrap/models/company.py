from django.db import models
from django.contrib.postgres.fields import JSONField

from scrap.models import Industry

class Company(models.Model):

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Companies'
        unique_together = ['name', 'symbol', 'industry_id']

    name = models.CharField(
        help_text="Company name",
        max_length=200
    )

    symbol = models.CharField(
        help_text="Company symbol",
        max_length=50
    )

    link = models.CharField(
        help_text="Company url",
        max_length=200,
        null=True
    )

    currency = models.CharField(
        help_text="Company currency",
        max_length=50,
        null=True
    )

    xid = models.CharField(
        help_text="Company currency",
        max_length=100,
        null=True
    )

    industry_id = models.ForeignKey(
        Industry,
        on_delete=models.CASCADE,
        related_name='companies'
    )

    histories = JSONField(
        help_text="Company full history",
        null=True
    )

    updated_at = models.DateTimeField(
        help_text="Updated time",
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Creation time",
    )
