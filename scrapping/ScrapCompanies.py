from lxml import html
import requests
from database.DbGet import *
import Settings
import json

class ScrapCompanies:
    """Scrap companies from industries from FT.com"""

    #Get companies list array
    def scrapCompaniesList(self):
        industry = DbGet().getIndustryToScrap();
        #Return false if not found
        if not industry:
            return False

        industryId = industry[0]
        slug = industry[2].replace("&","%26")
        link = Settings.industriesInCompaniesUrl + slug
        print "->Scrapping industry: "+industry[2],

        link = Settings.industriesInCompaniesUrl + "?industry="+ slug + "&RowsPerPage=100"
        return self.scrapIndustry(link, industryId)

    #iterate over industry
    def scrapIndustry(self, link, industryId):
        startRow = 0
        companies = []
        while(True):
            print ".",
            companyList = self.getPageContent(link + "&startRow=" + str(startRow), industryId)
            if(not companyList):
                break;
            startRow += 100
            companies = companies + companyList

        print "!"
        return companies

    #Scrap industry link
    def getPageContent(self, link, industryId):
        page = requests.get(link)
        parsedJson=json.loads(page.content);
        tree = html.fromstring(parsedJson["html"])

        companies = []
        for matchingElement in tree.xpath("//a"):
            companyInfo = {}
            companyLink = matchingElement.attrib['href'];
            companySymbol = companyLink[companyLink.index("?s=")+3:]
            companyName = matchingElement.text

            companyInfo["industry_id"] = industryId
            companyInfo["company_name"] = companyName
            companyInfo["company_symbol"] = companySymbol
            companyInfo["company_link"] = companyLink

            companies.append(companyInfo)

        return companies
