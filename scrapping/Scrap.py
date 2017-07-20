from scrapping.ScrapSectors import ScrapSectors
from scrapping.ScrapIndustries import ScrapIndustries
from scrapping.ScrapCompanies import ScrapCompanies
from scrapping.ScrapHistory import ScrapHistory
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

    #Save companies list array in database
    def scrapCompanies(self):
        imTheFather = True
        children = []

        for i in range(Settings.numberOfThreads): #Run multiple threads
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


    def scrapCompaniesProcess(self):
        while(True):
            companies = ScrapCompanies().scrapCompaniesList()
            if not companies:
                break;
            DbInsert().saveCompanies(companies)

    #Save histories from companies in database
    def scrapHistories(self):
        imTheFather = True
        children = []

        for i in range(Settings.numberOfThreads): #Run multiple threads
            child = os.fork()
            if child:
                children.append(child)
            else:
                imTheFather = False
                self.scrapHistoriesProcess()
                os._exit(0)
                break

        #Father must wait to all children before continue
        for childP in children:
            os.waitpid(childP, 0)


    def scrapHistoriesProcess(self):
        while(True):
            histories = ScrapHistory().scrapHistory()
            if not histories:
                break;
            DbInsert().saveHistory(histories)
