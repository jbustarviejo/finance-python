from Connect import Database
import Settings

class DbGet:

    #Get sector to scrap
    def getSectorToScrap(self):
        # Get a sector that never has been updated or is NULL
        query = "SELECT * from sectors WHERE (last_full_update IS NULL OR last_full_update > NOW() + INTERVAL " + str(Settings.maxTimeForUpdateDB) + " HOUR) ORDER BY RAND() LIMIT 1"
        update = {"table": "sectors", "column": "last_full_update"} #Block the column for not being update in multithread cases
        result = Database().runQuery(query, update)
        if not result or not result[0]:
            return False
        return result[0]

    #Get industries to scrap
    def getIndustryToScrap(self):
        # Get a industry that never has been updated or is NULL
        query = "SELECT * from industries WHERE (last_full_update IS NULL OR last_full_update > NOW() + INTERVAL " + str(Settings.maxTimeForUpdateDB) + " HOUR) ORDER BY RAND() LIMIT 1"
        update = {"table": "industries", "column": "last_full_update"} #Block the column for not being update in multithread cases
        result = Database().runQuery(query, update)
        if not result or not result[0]:
            return False
        return result[0]

    #Get company to scrap
    def getCompanyToScrap(self):
        # Get a company that never has been updated or is NULL
        query = "SELECT * from companies WHERE (last_full_update IS NULL OR last_full_update > NOW() + INTERVAL " + str(Settings.maxTimeForUpdateDB) + " HOUR) ORDER BY RAND() LIMIT 1"
        update = {"table": "companies", "column": "last_full_update"} #Block the column for not being update in multithread cases
        result = Database().runQuery(query, update)
        if not result or not result[0]:
            return False
        return result[0]

    #Get currency to scrap xid
    def getCurrencyToScrapXidToUSD(self):
        # Get a company that never has been updated or is NULL
        query = "SELECT * from currencies WHERE xidToUSD IS NULL ORDER BY RAND() LIMIT 1"
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return result[0]

    #Get currency to scrap xid
    def getCurrencyToScrapXidFromUSD(self):
        # Get a company that never has been updated or is NULL
        query = "SELECT * from currencies WHERE xidFromUSD IS NULL ORDER BY RAND() LIMIT 1"
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return result[0]

    #Get currency to scrap
    def getCurrencyToScrap(self):
        # Get a company that never has been updated or is NULL
        query = "SELECT * from currencies WHERE (last_full_update IS NULL OR last_full_update > NOW() + INTERVAL " + str(Settings.maxTimeForUpdateDB) + " HOUR) ORDER BY RAND() LIMIT 1"
        update = {"table": "currencies", "column": "last_full_update"} #Block the column for not being update in multithread cases
        result = Database().runQuery(query, update)
        if not result or not result[0]:
            return False
        return result[0]
