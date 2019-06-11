import json
import requests
from lxml import html

from django.utils import timezone
from django.db.models import Q
from django.core.management.base import BaseCommand

from scrap.models import Currency

class Command(BaseCommand):
    help = "Scrap currencies list from FT.com"

    def handle(self, *args, **kwargs):
        while(True):
            time_threshold = timezone.now() - timezone.timedelta(hours=24)
            currency = Currency.objects.filter(Q(updated_at__isnull=True) | Q(updated_at__lt=time_threshold) ).order_by('?').first()
            if not currency:
                print("Finished! 🏁")
                break

            print("->Scrapping currency: %s" % (currency.name),)

            self.scrapXid(currency, True)
            self.scrapXid(currency, False)
            currency.updated_at=timezone.now()
            currency.save()

            print("Scraped currency %s" % (currency.name))

    #iterate over currency
    def scrapXid(self, currency, direct):
        if direct:
            link =currency.scrap_conversion_to_USD
        else:
            link =currency.scrap_reverse_conversion_to_USD

        page = requests.get(link)
        tree = html.fromstring(page.content)

        matchingElement = tree.xpath("//section[@class='mod-tearsheet-add-to-watchlist']")
        if (not matchingElement or len(matchingElement)==0):
            print("Not found xid. Direct? ", direct)
            return False
        jsonScript = json.loads(matchingElement[0].attrib['data-mod-config'])

        xid = jsonScript["xid"]
        if (not xid or not currency):
            return False

        if direct:
            currency.xid_to_usd = xid
        else:
            currency.xid_from_usd = xid

        currency.updated_at=timezone.now()
        currency.save()
