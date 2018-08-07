from lxml import html
import requests
import json
import os

import scrap.Settings
from database.scrap.dbGet import *
from database.scrap.dbInsert import *

class ScrapCompanies:
    """Scrap companies from industries from FT.com"""

    #Get companies list array
    def scrapAllCompanies(self):
        imTheFather = True
        children = []

        for i in range(scrap.Settings.numberOfThreads): #Run multiple threads
            child = os.fork()
            if child:
                children.append(child)
            else:
                imTheFather = False
                self.scrapCompaniesProcess()
                os._exit(0)
                break

        #Father must wait to all children before continue
        for childP in children:
            os.waitpid(childP, 0)

    #Scrap companies proccess
    def scrapCompaniesProcess(self):
        while(True):
            companies = self.scrapCompaniesList()
            if not companies:
                print("--No more companies to scrap--")
                break;
            DbInsert().saveCompanies(companies)

    #Get companies list array
    def scrapCompaniesList(self):
        industry = DbGet().getIndustryToScrapCompanies();
        #Return false if not found
        if not industry:
            return False

        industryId = industry[0]
        slug = industry[2].replace("&","%26")
        link = scrap.Settings.industriesInCompaniesUrl + slug
        print ("->Scrapping industry: "+industry[2],)

        link = scrap.Settings.industriesInCompaniesUrl + "?industry="+ slug + "&RowsPerPage=100"
        return self.scrapIndustry(link, industryId)

    #iterate over industry
    def scrapIndustry(self, link, industryId):
        startRow = 0
        companies = []
        while(True):
            print (".",)
            companyList = self.getPageContent(link + "&startRow=" + str(startRow), industryId)
            if(not companyList):
                break;
            startRow += 100
            companies = companies + companyList

        print ("!")
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
