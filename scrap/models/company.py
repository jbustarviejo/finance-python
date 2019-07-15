from django.db import models
from django.contrib.postgres.fields import JSONField

from scrap.models import Industry

class Company(models.Model):

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Companies'
        unique_together = ['name', 'symbol', 'industry']

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

    industry = models.ForeignKey(
        Industry,
        on_delete=models.CASCADE,
        related_name='companies'
    )

    incorporated = models.CharField(
        help_text="Incorporation year of the company",
        max_length=100,
        null=True,
        blank=True
    )

    employees = models.CharField(
        help_text="Number of employees of the company",
        max_length=100,
        null=True,
        blank=True
    )

    revenue = models.CharField(
        help_text="Revenue in the local currency",
        max_length=100,
        null=True,
        blank=True
    )

    net_income = models.CharField(
        help_text="Web of the company",
        max_length=100,
        null=True,
        blank=True
    )

    website = models.CharField(
        help_text="Web of the company",
        max_length=300,
        null=True,
        blank=True
    )

    location = models.CharField(
        help_text="Headquarters address",
        max_length=5000,
        null=True,
        blank=True
    )

    description = models.CharField(
        help_text="About the company",
        max_length=10000,
        null=True,
        blank=True
    )

    history = JSONField(
        help_text="Company full history",
        null=True,
        blank=True
    )

    history_updated_at = models.DateTimeField(
        help_text="Updated history time",
        null=True,
        blank=True
    )

    profile_updated_at = models.DateTimeField(
        help_text="Updated profile time",
        null=True,
        blank=True
    )

    analysis_updated_at = models.DateTimeField(
        help_text="Updated analysis time",
        null=True,
        blank=True
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
    def info_scraping_link(self):
        return "https://markets.ft.com/data/investment-trust/tearsheet/summary?s=" + self.symbol

    def profile_scraping_link(self):
        return "https://markets.ft.com/data/equities/tearsheet/profile?s=" + self.symbol

    def history_scraping_link(self):
        return "https://markets.ft.com/data/chartapi/series"

    def history_payload(self):
        return {
            "days":36500, #100 years
            "dataNormalized":False,
            "dataPeriod":"Day",
            "dataInterval":1,
            "endOffsetDays":0,
            "exchangeOffset":0,
            "realtime":False,
            "yFormat":"0.###",
            "timeServiceFormat":"JSON",
            "rulerIntradayStart":26,
            "rulerIntradayStop":3,
            "rulerInterdayStart":10957,
            "rulerInterdayStop":365,
            "returnDateType":"ISO8601",
            "elements":[
                {
                    "Label":"d475c065",
                    "Type":"price",
                    "Symbol":str(self.xid),
                    "OverlayIndicators":[],
                    "Params":{}
                },
                {
                    "Label":"079e5104",
                    "Type":"volume",
                    "Symbol":str(self.xid),
                    "OverlayIndicators":[],
                    "Params":{}
                }
            ]
        }

    def history_headers(self):
        return {
            "Content-Type": "application/json",
            "Content-Length": "999999"
        }

    def getHistory(self, length):
        return self.history[-length:]
