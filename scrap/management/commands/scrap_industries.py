import requests
from lxml import html
from django.utils import timezone

from django.db.models import Q
from django.db import transaction
from django.core.management.base import BaseCommand

from scrap.models import Sector, Industry

class Command(BaseCommand):
    help = "Industries sectors data from FT.com"

    @transaction.non_atomic_requests
    def handle(self, *args, **kwargs):
        time_threshold = timezone.now() - timezone.timedelta(hours=24)
        sector = Sector.objects.filter(Q(updated_at__isnull=True) | Q(updated_at__lt=time_threshold)).order_by('?')[1]
        if not sector:
            print("Finished! 🏁")
            exit()

        page = requests.get(sector.link)
        tree = html.fromstring(page.content)

        industries_count = 0
        for matchingElement in tree.xpath("//div[@data-module-name='IndustryListApp']//a[@class='mod-ui-link']"): #/a[@class='mod-ui-link']/text()
            industry, created = Industry.objects.get_or_create(
                name=matchingElement.text,
                industry_slug=industryName.replace(" ","-").replace("&","and"),
                sector_id=sector.id
            )
            industry.save()
            industries_count+=1

        if industries_count == 0:
            print("No industries were scrapped for sector %s! ⚠️" % (sector.name))
            exit()

        sector.updated_at=timezone.now()
        sector.save()
