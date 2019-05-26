from django.db import models

class Sector(models.Model):

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['name', 'slug']

    name = models.CharField(
        help_text="Sector name",
        max_length=50
    )

    slug = models.CharField(
        help_text="Slug",
        max_length=50
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
        return "https://markets.ft.com/data/sectors/" + self.slug

    @property
    def industries_count(self):
        return self.industries.count()
