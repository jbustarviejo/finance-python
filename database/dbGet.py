from database.connect import Database
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
    def getCompanyToScrap(self, currency = None):
        # Get a company that never has been updated or is NULL

        filterByCurrency = "" #Filter by currency?
        if type(currency) is not None:
            filterByCurrency = "AND currency='"+currency+"'"

        query = "SELECT * from companies WHERE (last_full_update IS NULL OR last_full_update < NOW() - INTERVAL " + str(Settings.maxTimeForUpdateDB) + " HOUR) %s ORDER BY RAND() LIMIT 1" % (filterByCurrency)
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

    #Get history to optimize SVR
    def getCompanyToOptSVR(self, currency):
        if type(currency) is not None:
            currencyFilter = " AND currency = '"+currency+"'"
        query = "SELECT companies.id FROM companies LEFT JOIN companiesSVR on companiesSVR.company_id = companies.id WHERE (companiesSVR.company_id IS NULL %s) ORDER BY RAND() LIMIT 1" % (currencyFilter)
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return result[0]

    #Get history to optimize SVM
    def getCompanyToOptSVM(self, currency):
        if type(currency) is not None:
            currencyFilter = " AND currency = '"+currency+"'"
        query = "SELECT companies.id FROM companies LEFT JOIN companiesSVM on companiesSVM.company_id = companies.id WHERE (companiesSVM.company_id IS NULL %s) ORDER BY RAND() LIMIT 1" % (currencyFilter)
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return result[0]

    def getCompanyToOptPendingSVM(self):
        query = "SELECT company_id FROM (SELECT count(*) as count, company_id, MAX(updated_at) as updated_at FROM companiesSVM GROUP BY company_id) as t WHERE t.count < 300 AND updated_at < NOW() - INTERVAL 15 MINUTE ORDER BY RAND() LIMIT 1"
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return result[0]

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

    #Get companies by currencies
    def getCompaniesByCurrency(self, currencySymbols):
        # Get company history in USD
        inQuery = ""
        if type(currencySymbols) is list:
            for i in range(0, len(currencySymbols)):
                inQuery+="'"+currencySymbols[i]+"',"
            inQuery = "IN ("+inQuery[:-1]+")"
        else:
            inQuery = "IN ('"+currencySymbols+"')"

        query = "SELECT id FROM companies WHERE currency %s" % (inQuery)
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return result

    #Get companies by symbol like
    def getCompaniesBySymbolLike(self, symbolLike):
        # Get company history in USD
        query = "SELECT id FROM companies WHERE symbol LIKE '%s'" % (symbolLike)
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return result

    #Get if company has been processed
    def getIfCompanyProcessed(self, company, svm, kernel, numberOfDaysSample, numberOfTrainVectors):
        # Get company history in USD
        query = "SELECT id FROM companiesSVM WHERE company_id = '%s' AND svm = '%s' AND kernel = '%s' AND number_of_days_sample = '%s' AND number_of_train_vectors = '%s' " % (company, svm, kernel, numberOfDaysSample, numberOfTrainVectors)
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return True
