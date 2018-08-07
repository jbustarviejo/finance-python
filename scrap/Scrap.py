import os

import scrap.Settings
from scrap.ScrapSectors import *
from scrap.ScrapIndustries import *
from scrap.ScrapCompanies import *
from scrap.ScrapHistory import *

class Scrap:

    #Save sectors list in database
    def scrapSectors(self):
        ScrapSectors().scrapAllSectors()

    #Save industries list in database
    def scrapIndustries(self):
        ScrapIndustries().scrapAllIndustries()

    #Save companies list array in database
    def scrapCompanies(self):
        ScrapCompanies().scrapAllCompanies()

    #Save histories from companies in database
    def scrapHistories(self, currency = None):
        ScrapHistory().scrapAllHistories()

    #
    # #Save currencies in database
    # def scrapCurrencies(self):
    #     ScrapCurrency().scrapCurrencyList()
    #     ScrapCurrency().scrapCurrencyXid(True)
    #     ScrapCurrency().scrapCurrencyXid(False)
    #     self.scrapCurrencyHistories()
    #
    # #Save histories from currencies in database
    # def scrapCurrencyHistories(self):
    #     imTheFather = True
    #     children = []
    #
    #     for i in range(Settings.numberOfThreads): #Run multiple threads
    #         child = os.fork()
    #         if child:
    #             children.append(child)
    #         else:
    #             imTheFather = False
    #             self.scrapCurrenciesHistoriesProcess()
    #             os._exit(0)
    #             break
    #
    #     #Father must wait to all children before continue
    #     for childP in children:
    #         os.waitpid(childP, 0)
    #
    # #Scrap currencies histories proccess
    # def scrapCurrenciesHistoriesProcess(self):
    #     while(True):
    #         histories = ScrapCurrency().scrapCurrencyHistory()
    #         if histories is False:
    #             break;
    #         elif histories is True:
    #             continue;
    #         DbInsert().saveCurrencyHistory(histories)
