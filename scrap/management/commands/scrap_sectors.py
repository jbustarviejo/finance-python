import requests
from lxml import html

from django.core.management.base import BaseCommand

from scrap.models import Sector

class Command(BaseCommand):
    help = "Scrap sectors data from FT.com"

    def handle(self, *args, **kwargs):
        #Get sectors array
        page = requests.get('https://markets.ft.com/data/sectors')
        tree = html.fromstring(page.content)

        sectors = []
        for matchingElement in tree.xpath("//tr[@class='mod-ui-accordion__content--const']"):
            sectorName = matchingElement.xpath(".//a['@class=mod-ui-link mod-sector-performance__sector-link']/text()")[0]
            sectorLink = matchingElement.xpath(".//a['@class=mod-ui-link mod-sector-performance__sector-link']")[0].attrib['href'];
            sectorSize = matchingElement.xpath(".//td/text()")

            Sector(name=sectorName, slug=sectorName.replace(" ","-").replace("&","and").lower()).save()
