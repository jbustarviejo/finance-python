from django.db import models
from scrap.models import Sector

class Industry(models.Model):

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Industries'
        unique_together = ['name', 'slug', 'sector_id']

    name = models.CharField(
        help_text="Sector name",
        max_length=50
    )

    slug = models.CharField(
        help_text="Slug",
        max_length=50
    )

    sector_id = models.ForeignKey(
        Sector,
        on_delete=models.CASCADE,
        related_name='industries'
    )

    updated_at = models.DateTimeField(
        help_text="Updated time",
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Creation time",
    )

    @property
    def link(self):
        return "https://markets.ft.com/data/sectors/" + self.sector_id.slug + "/" + self.slug
