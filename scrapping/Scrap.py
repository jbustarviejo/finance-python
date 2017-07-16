from scrapping.ScrapSectors import ScrapSectors
from scrapping.ScrapIndustries import ScrapIndustries
from scrapping.ScrapCompanies import ScrapCompanies
from database.DbInsert import *
import Settings
import os

class Scrap:

    #Save sectors array in database
    def scrapSectors(self):
        sectors = ScrapSectors().scrapSectors()
        DbInsert().saveSectors(sectors)

    #Save industries array in database
    def scrapIndustries(self):
        while(True):
            industries = ScrapIndustries().scrapIndustries()
            if not industries:
                break;
            DbInsert().saveIndustries(industries)

    #Save companies array in database
    def scrapCompanies(self):
        self.scrapCompaniesList()

    #Save companies list array in database
    def scrapCompaniesList(self):
        imTheFather = True
        children = []

        for i in range(Settings.numberOfThreads-1): #Run multiple threads
            child = os.fork()
            if child:
                children.append(child)
            else:
                imTheFather = False
                self.scrapCompaniesProcess()
                os._exit(0)
                break

        #Father must wait to all children before continue
        for childd in children:
            os.waitpid(childd, 0)


    def scrapCompaniesProcess(self):
        while(True):
            companies = ScrapCompanies().scrapCompaniesList()
            if not companies:
                break;
            DbInsert().saveCompanies(companies)
