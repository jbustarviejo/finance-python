from django.db import models

from scrap.models import Sector

class Industry(models.Model):

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Industries'
        unique_together = ['name', 'slug', 'sector_id']

    name = models.CharField(
        help_text="Industry name",
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
        return " http://markets.ft.com/research/Browse-Companies/" + self.sector_id.slug.lower() + "/" + self.slug.lower()

    @property
    def companies_count(self):
        return self.companies.count()

    @property
    def companies_scraping_link(self):
        return "http://markets.ft.com/Research/Remote/UK/BrowseCompanies/UpdateCompanyList/?industry=" + self.name.replace("&","%26") + "&RowsPerPage=100"
