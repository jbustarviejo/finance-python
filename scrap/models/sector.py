from django.db import models

class Sector(models.Model):

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Creation time",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Updated time",
    )

    name = models.CharField(
        help_text="Sector name",
        max_length=50
    )

    slug = models.CharField(
        help_text="Slug",
        max_length=50
    )
