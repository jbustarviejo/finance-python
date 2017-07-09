from lxml import html
import requests
import Helper

class ScrapSectors:
    """Scrap data from FT.com"""

    #Get sectors array
    def scrap_sectors(self):
        page = requests.get('https://markets.ft.com/data/sectors')
        tree = html.fromstring(page.content)

        sectors = []
        for matchingElement in tree.xpath("//tr[@class='mod-ui-accordion__content--const']"):
            sectorInfo = {}
            sectorName = matchingElement.xpath(".//a['@class=mod-ui-link mod-sector-performance__sector-link']/text()")[0]
            sectorLink = matchingElement.xpath(".//a['@class=mod-ui-link mod-sector-performance__sector-link']")[0].attrib['href'];
            sectorSize = matchingElement.xpath(".//td/text()")

            sectorInfo["sector_name"] = sectorName
            sectorInfo["sector_link"] = Helper.rootUrl + sectorLink
            sectorInfo["sector_industries"] = sectorSize[0]
            sectorInfo["sector_companies"] = sectorSize[1].replace(",", "")

            sectors.append(sectorInfo)

        return sectors
