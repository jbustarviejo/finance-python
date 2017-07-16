from lxml import html
import requests
from database.dbGet import *
import Settings

class ScrapIndustries:
    """Scrap industries from sectors from FT.com"""

    #Get sectors array
    def scrapIndustries(self):
        sector = dbGet().getSectorToScrap()[0];
        slug = sector[2]
        link = Settings.industriesInSectorsUrl + "?sector = "+ slug + "&RowsPerPage=100"
        return self.scrapIndustry(Settings.industriesInSectorsUrl + slug)

        return sector

    #iterate over industry
    def scrapIndustry(self, link):
        startRow = 0
        self.getPageContent(link + "&startRow=" + str(startRow))

    #Scrap industry link
    def getPageContent(self, link):
        page = requests.get(link)
        tree = html.fromstring(page.content)

        import sys
        sys.exit()

        industries = []
        for matchingElement in tree.xpath("//tr[@class='company-link']"):
            industryInfo = {}
            industryLink = matchingElement.attrib['href'];
            industryName = matchingElement.xpath("./text()")

            industryInfo["industry_name"] = industryName
            industryInfo["industry_link"] = industryLink

            sectors.append(sectorInfo)

        return sectors
