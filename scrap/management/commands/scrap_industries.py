import requests
from lxml import html

from django.utils import timezone
from django.db.models import Q
from django.db import transaction
from django.core.management.base import BaseCommand

from scrap import settings
from scrap.models import Sector, Industry

class Command(BaseCommand):
    help = "Industries sectors data from FT.com"

    @transaction.non_atomic_requests
    def handle(self, *args, **kwargs):
        while(True):
            time_threshold = timezone.now() - timezone.timedelta(hours=24)
            sector = Sector.objects.filter(Q(updated_at__isnull=True) | Q(updated_at__lt=time_threshold)).order_by('?').first()
            if not sector:
                print("Finished! 🏁")
                exit()

            headers = {"Cookie": settings.cookieHeader}

            page = requests.get(sector.link, headers=headers)
            tree = html.fromstring(page.content)

            industries_count = 0
            for matchingElement in tree.xpath("//div[@data-module-name='IndustryListApp']//a[@class='mod-ui-link']"): #/a[@class='mod-ui-link']/text()
                industry_name = matchingElement.text
                industry, created = Industry.objects.get_or_create(
                    name=industry_name,
                    slug=industry_name.replace(" ","-").replace("&","and").lower(),
                    sector_id=sector
                )
                industry.save()
                industries_count+=1

            if industries_count == 0:
                print("No industries were scraped for sector %s! ⚠️" % (sector.name))
                exit()

            sector.updated_at=timezone.now()
            sector.save()
            print("Scraped sector %s" % (sector.name))
