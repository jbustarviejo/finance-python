from lxml import html
import requests

from database.scrap.dbInsert import *

class ScrapSectors:
    """Scrap sectors data from FT.com"""

    #Get sectors array
    def scrapAllSectors(self):
        page = requests.get('https://markets.ft.com/data/sectors')
        tree = html.fromstring(page.content)

        sectors = []
        for matchingElement in tree.xpath("//tr[@class='mod-ui-accordion__content--const']"):
            sectorInfo = {}
            sectorName = matchingElement.xpath(".//a['@class=mod-ui-link mod-sector-performance__sector-link']/text()")[0]
            sectorLink = matchingElement.xpath(".//a['@class=mod-ui-link mod-sector-performance__sector-link']")[0].attrib['href'];
            sectorSize = matchingElement.xpath(".//td/text()")

            sectorInfo["sector_name"] = sectorName
            sectorInfo["sector_slug"] = sectorName.replace(" ","-").replace("&","and");
            sectorInfo["sector_industries"] = sectorSize[0]
            sectorInfo["sector_companies"] = sectorSize[1].replace(",", "")

            sectors.append(sectorInfo)

        if not sectors:
            print("--No sectors detected to be scrapped--")
            return

        DbInsert().saveSectors(sectors)
