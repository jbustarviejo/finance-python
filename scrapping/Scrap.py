from scrapping.ScrapSectors import ScrapSectors
from scrapping.ScrapIndustries import ScrapIndustries
from scrapping.ScrapCompanies import ScrapCompanies
from scrapping.ScrapHistory import ScrapHistory
from scrapping.ScrapCurrency import ScrapCurrency
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
    def scrapHistories(self, currency = None):
        imTheFather = True
        children = []

        for i in range(Settings.numberOfThreads): #Run multiple threads
            child = os.fork()
            if child:
                children.append(child)
            else:
                imTheFather = False
                self.scrapHistoriesProcess(currency)
                os._exit(0)
                break

        #Father must wait to all children before continue
        for childP in children:
            os.waitpid(childP, 0)


    def scrapHistoriesProcess(self, currency):
        while(True):
            histories = ScrapHistory().scrapHistory(currency)
            if histories is False:
                break;
            elif histories is True:
                continue;
            DbInsert().saveHistory(histories)

    #Save currencies in database
    def scrapCurrencies(self):
        ScrapCurrency().scrapCurrencyList()
        ScrapCurrency().scrapCurrencyXid(True)
        ScrapCurrency().scrapCurrencyXid(False)
        self.scrapCurrencyHistories()

    #Save histories from currencies in database
    def scrapCurrencyHistories(self):
        imTheFather = True
        children = []

        for i in range(Settings.numberOfThreads): #Run multiple threads
            child = os.fork()
            if child:
                children.append(child)
            else:
                imTheFather = False
                self.scrapCurrenciesHistoriesProcess()
                os._exit(0)
                break

        #Father must wait to all children before continue
        for childP in children:
            os.waitpid(childP, 0)


    def scrapCurrenciesHistoriesProcess(self):
        while(True):
            histories = ScrapCurrency().scrapCurrencyHistory()
            if histories is False:
                break;
            elif histories is True:
                continue;
            DbInsert().saveCurrencyHistory(histories)
