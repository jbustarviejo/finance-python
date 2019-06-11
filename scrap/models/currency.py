from django.db import models
from django.contrib.postgres.fields import JSONField

class Currency(models.Model):

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Currencies'
        unique_together = ['name', 'symbol']

    name = models.CharField(
        help_text="Currency name",
        max_length=200
    )

    symbol = models.CharField(
        help_text="Currency symbol",
        max_length=50
    )

    xid_to_usd = models.CharField(
        help_text="Xid to USD conversion",
        max_length=100,
        null=True
    )

    xid_from_usd = models.CharField(
        help_text="Xid to USD inverse conversion",
        max_length=100,
        null=True
    )

    history_to_usd = JSONField(
        help_text="Currency full history to USD",
        null=True,
        blank=True
    )

    history_from_usd = JSONField(
        help_text="Currency full history to USD inverse",
        null=True,
        blank=True
    )

    history_updated_at = models.DateTimeField(
        help_text="Updated history time",
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
    def scrap_conversion_to_USD(self):
        return "https://markets.ft.com/data/currencies/tearsheet/summary?s=" + self.symbol + "USD"

    @property
    def scrap_reverse_conversion_to_USD(self):
        return "https://markets.ft.com/data/currencies/tearsheet/summary?s=USD" + self.symbol

    def history_scraping_link(self):
        return "https://markets.ft.com/data/chartapi/series"

    def history_payload(self, xid):
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
                    "Symbol":str(xid),
                    "OverlayIndicators":[],
                    "Params":{}
                },
                {
                    "Label":"079e5104",
                    "Type":"volume",
                    "Symbol":str(xid),
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
