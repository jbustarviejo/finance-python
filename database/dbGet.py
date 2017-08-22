from Connect import Database
import Settings

class DbGet:

    #--------SCRAP--------

    #Get sector to scrap
    def getSectorToScrap(self):
        # Get a sector that never has been updated or is NULL
        query = "SELECT * from sectors WHERE (last_full_update IS NULL OR last_full_update < NOW() - INTERVAL " + str(Settings.maxTimeForUpdateDB) + " HOUR) ORDER BY RAND() LIMIT 1"
        update = {"table": "sectors", "column": "last_full_update"} #Block the column for not being update in multithread cases
        result = Database().runQuery(query, update)
        if not result or not result[0]:
            return False
        return result[0]

    #Get industries to scrap
    def getIndustryToScrap(self):
        # Get a industry that never has been updated or is NULL
        query = "SELECT * from industries WHERE (last_full_update IS NULL OR last_full_update < NOW() - INTERVAL " + str(Settings.maxTimeForUpdateDB) + " HOUR) ORDER BY RAND() LIMIT 1"
        update = {"table": "industries", "column": "last_full_update"} #Block the column for not being update in multithread cases
        result = Database().runQuery(query, update)
        if not result or not result[0]:
            return False
        return result[0]

    #Get company to scrap
    def getCompanyToScrap(self):
        # Get a company that never has been updated or is NULL
        query = "SELECT * from companies WHERE (last_full_update IS NULL OR last_full_update < NOW() - INTERVAL " + str(Settings.maxTimeForUpdateDB) + " HOUR) ORDER BY RAND() LIMIT 1"
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
        query = "SELECT * from currencies WHERE (last_full_update IS NULL OR last_full_update < NOW() - INTERVAL " + str(Settings.maxTimeForUpdateDB) + " HOUR) ORDER BY RAND() LIMIT 1"
        update = {"table": "currencies", "column": "last_full_update"} #Block the column for not being update in multithread cases
        result = Database().runQuery(query, update)
        if not result or not result[0]:
            return False
        return result[0]

    #--------Get to be analyzed--------

    #Get history of a company in USD by its id
    def getHistoryInUSD(self, company_id, limit):
        # Get company history in USD
        query = "SELECT * from (SELECT ROUND(IF(currency = 'USD', histories.open, histories.open * currencyHistoryToUSD.price),3) as conversion FROM histories left join currencies on currencies.symbol = histories.currency left JOIN currencyHistoryToUSD ON (currencies.id = currencyHistoryToUSD.currency_id AND currencyHistoryToUSD.date = histories.date) WHERE company_id = '%s' ORDER BY histories.date ASC LIMIT %s) as query where conversion is not null" % (company_id, limit)
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return result

    #Get history of a company by its id
    def getHistory(self, company_id, limit):
        # Get company history in USD
        query = "SELECT * from (SELECT histories.open as conversion FROM histories left join currencies on currencies.symbol = histories.currency WHERE company_id = '%s' ORDER BY histories.date ASC LIMIT %s) as query where conversion is not null" % (company_id, limit)
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return result

    #Get company
    def getCompaniesByCurrency(self, currencySymbol):
        # Get company history in USD
        query = "SELECT id, currency FROM companies WHERE currency = '%s'" % (currencySymbol)
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return result
