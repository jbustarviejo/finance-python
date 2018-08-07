from lxml import html
from lxml import etree
import requests

import scrap.Settings
from database.scrap.dbGet import *
from database.scrap.dbInsert import *

class ScrapIndustries:
    """Scrap industries from sectors from FT.com"""

    #Get all industries list and save it
    def scrapAllIndustries(self):
        while(True):
            industries = self.scrapIndustries()
            if not industries:
                print("--No more industries to scrap--")
                break;
            DbInsert().saveIndustries(industries)

    #Get industries array
    def scrapIndustries(self):
        sector = DbGet().getSectorToScrapIndustries();
        #Return if not found
        if not sector:
            return False

        sectorId = sector[0]
        slug = sector[2]
        link = scrap.Settings.industriesInSectorsUrl + slug

        return self.scrapSectorIndustries(link, sectorId)

    #Scrap sector industries
    def scrapSectorIndustries(self, link, sectorId):
        page = requests.get(link)
        tree = html.fromstring(page.content)

        industries = []
        for matchingElement in tree.xpath("//div[@data-module-name='IndustryListApp']//a[@class='mod-ui-link']"): #/a[@class='mod-ui-link']/text()
            industryInfo = {}

            industryName = matchingElement.text

            industrySlug = industryName.replace(" ","-").replace("&","and");

            industryInfo["sector_id"] = sectorId
            industryInfo["industry_name"] = industryName
            industryInfo["industry_slug"] = industrySlug

            industries.append(industryInfo)

        return industries
