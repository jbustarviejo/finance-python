from datetime import datetime

import scrap.Settings
from database.connect import Database

class DbGet:

    #--------SCRAP--------

    #Get sector to scrap
    def getSectorToScrapIndustries(self):
        # Get a sector that never has been updated or is NULL
        query = "SELECT * from sectors WHERE (last_full_update IS NULL OR last_full_update < NOW() - INTERVAL " + str(scrap.Settings.maxTimeForUpdateDB) + " HOUR) ORDER BY RAND() LIMIT 1"
        update = {"table": "sectors", "column": "last_full_update"} #Block the column for not being update in multithread cases
        result = Database().runQuery(query, update)
        if not result or not result[0]:
            return False
        return result[0]

    #Get industries to scrap
    def getIndustryToScrapCompanies(self):
        # Get a industry that never has been updated or is NULL
        query = "SELECT * from industries WHERE (last_full_update IS NULL OR last_full_update < NOW() - INTERVAL " + str(scrap.Settings.maxTimeForUpdateDB) + " HOUR) ORDER BY RAND() LIMIT 1"
        update = {"table": "industries", "column": "last_full_update"} #Block the column for not being update in multithread cases
        result = Database().runQuery(query, update)
        if not result or not result[0]:
            return False
        return result[0]

    #Get company to scrap
    def getCompanyToScrapHistory(self, currency = None):
        # Get a company that never has been updated or is NULL

        filterByCurrency = "" #Filter by currency?
        if currency is not None:
            filterByCurrency = "AND currency='"+currency+"'"

        query = "SELECT * from companies WHERE (last_full_update IS NULL OR last_full_update < NOW() - INTERVAL " + str(scrap.Settings.maxTimeForUpdateDB) + " HOUR) %s ORDER BY RAND() LIMIT 1" % (filterByCurrency)
        update = {"table": "companies", "column": "last_full_update"} #Block the column for not being update in multithread cases
        result = Database().runQuery(query, update)
        if not result or not result[0]:
            return False
        return result[0]

    #Get company to scrap from MCE
    def getCompanyToScrapHistoryMCE(self):
        # Get a company that never has been updated or is NULL

        query = "SELECT * from companies c WHERE (last_full_update IS NULL OR last_full_update < NOW() - INTERVAL " + str(scrap.Settings.maxTimeForUpdateDB) + " HOUR) AND c.symbol LIKE '%:MCE' ORDER BY RAND() LIMIT 1"
        update = {"table": "companies", "column": "last_full_update"} #Block the column for not being update in multithread cases
        result = Database().runQuery(query, update)
        if not result or not result[0]:
            return False
        return result[0]

    # #Get currency to scrap xid
    # def getCurrencyToScrapXidToUSD(self):
    #     # Get a company that never has been updated or is NULL
    #     query = "SELECT * from currencies WHERE xidToUSD IS NULL ORDER BY RAND() LIMIT 1"
    #     result = Database().runQuery(query)
    #     if not result or not result[0]:
    #         return False
    #     return result[0]
    #
    # #Get currency to scrap xid
    # def getCurrencyToScrapXidFromUSD(self):
    #     # Get a company that never has been updated or is NULL
    #     query = "SELECT * from currencies WHERE xidFromUSD IS NULL ORDER BY RAND() LIMIT 1"
    #     result = Database().runQuery(query)
    #     if not result or not result[0]:
    #         return False
    #     return result[0]
    #
    # #Get currency to scrap
    # def getCurrencyToScrap(self):
    #     # Get a company that never has been updated or is NULL
    #     query = "SELECT * from currencies WHERE (last_full_update IS NULL OR last_full_update < NOW() - INTERVAL " + str(scrap.Settings.maxTimeForUpdateDB) + " HOUR) ORDER BY RAND() LIMIT 1"
    #     update = {"table": "currencies", "column": "last_full_update"} #Block the column for not being update in multithread cases
    #     result = Database().runQuery(query, update)
    #     if not result or not result[0]:
    #         return False
    #     return result[0]
