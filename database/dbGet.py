from database.connect import Database
from datetime import datetime
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
    def getCompanyToOptSVM(self, currencySymbols):
        inQuery = ""
        if type(currencySymbols) is list:
            for i in range(0, len(currencySymbols)):
                inQuery+="'"+currencySymbols[i]+"',"
            inQuery = "AND currency IN ("+inQuery[:-1]+")"
        elif currencySymbols is None:
            inQuery = ""
        else:
            inQuery = "AND currency IN ('"+currencySymbols+"')"
        query = "SELECT companies.id FROM companies LEFT JOIN companiesSVM4 on companiesSVM4.company_id = companies.id WHERE companiesSVM4.company_id IS NULL %s ORDER BY RAND() LIMIT 1" % (inQuery)
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return result[0]

    def getCompanyToOptPendingSVM(self):
        query = "SELECT company_id FROM (SELECT count(*) as count, company_id, MAX(updated_at) as updated_at FROM companiesSVM4 GROUP BY company_id) as t WHERE t.count < 300 AND updated_at < NOW() - INTERVAL 24*60 MINUTE ORDER BY RAND() LIMIT 1"
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return result[0]

    def getCompanyToOptSVMWithQ(self, currencySymbols):
        inQuery = ""
        if type(currencySymbols) is list:
            for i in range(0, len(currencySymbols)):
                inQuery+="'"+currencySymbols[i]+"',"
            inQuery = "AND currency IN ("+inQuery[:-1]+")"
        elif currencySymbols is None:
            inQuery = ""
        else:
            inQuery = "AND currency IN ('"+currencySymbols+"')"
        query = "SELECT companies.id FROM companies LEFT JOIN companiesSVMWithQ2 svmWQ on svmWQ.company_id = companies.id WHERE svmWQ.company_id IS NULL %s ORDER BY RAND() LIMIT 1" % (inQuery)
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return result[0]

    def getCompanyToOptSVC(self):
        query = "SELECT DISTINCT(c.id) FROM companies c JOIN histories h ON h.company_id = c.id AND c.currency = 'EUR' OR c.currency='USD' LEFT JOIN companiesSVC svmWQ on svmWQ.company_id = h.company_id WHERE svmWQ.company_id IS NULL AND YEAR(h.date) = 2017 ORDER BY RAND() LIMIT 1"
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return result[0]

    def getCompanyToOptSVM(self):
        query = "SELECT c_id from (SELECT c.id as c_id FROM companies c LEFT JOIN companiesSVM svmWQ on svmWQ.company_id = c.id WHERE svmWQ.company_id IS NULL LIMIT 1) as c_id LEFT JOIN histories h on h.company_id = c_id AND YEAR(h.date) = '2017' GROUP BY c_id"
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return result[0]

    def getCompanyToOptSVCWithMaxAndMin(self, year, min_month, max_month):
        # query = "SELECT h.company_id, COUNT(*) as repeats FROM histories h LEFT JOIN companiesSVC svmWQ on svmWQ.company_id = h.company_id AND year='%s' AND min_month = '%s' AND max_month = '%s' WHERE svmWQ.company_id IS NULL AND YEAR(h.date) = '%s' AND MONTH(h.date) BETWEEN '%s' AND '%s' GROUP BY h.company_id LIMIT 1"  % (year, min_month, max_month, year, min_month, max_month)
        # Faster!!
        # query = "SELECT h.company_id, COUNT(*) as repeats FROM histories h WHERE YEAR(h.date) = '%s' AND MONTH(h.date) BETWEEN '%s' AND '%s' AND h.company_id = (SELECT c.id as c_id FROM companies c LEFT JOIN companiesSVC svmWQ on svmWQ.company_id = c.id AND year='%s' AND min_month = '%s' AND max_month = '%s' WHERE svmWQ.company_id IS NULL LIMIT 1) GROUP BY h.company_id LIMIT 1"  % (year, min_month, max_month, year, min_month, max_month)
        query = "SELECT c_id, count(*) as repeats from (SELECT c.id as c_id FROM companies c LEFT JOIN companiesSVC svmWQ on svmWQ.company_id = c.id AND year='%s' AND min_month = '%s' AND max_month = '%s' WHERE svmWQ.company_id IS NULL LIMIT 1) as c_id LEFT JOIN histories h on h.company_id = c_id AND YEAR(h.date) = '%s' AND MONTH(h.date) BETWEEN '%s' AND '%s' GROUP BY c_id"  % (year, min_month, max_month, year, min_month, max_month)

        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return result[0]

    def getCompanyToOptPendingSVMWithQ(self):
        query = "SELECT company_id FROM (SELECT count(*) as count, company_id, MAX(updated_at) as updated_at FROM companiesSVMWithQ2 svmWQ GROUP BY company_id) as t WHERE t.count < 300 AND updated_at < NOW() - INTERVAL 24*60 MINUTE ORDER BY RAND() LIMIT 1"
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

    def getHistory2(self, company_id, limit, year, max_month):
        # Get company history in
        max_month_str = str(max_month)
        if(max_month<10):
            max_month_str="0"+max_month_str
        date = str(year)+"-"+max_month_str+"-01"
        query = "SELECT conversion FROM (SELECT histories.open as conversion, histories.date as date FROM histories left join currencies on currencies.symbol = histories.currency WHERE company_id = '%s' AND date <= '%s' ORDER BY histories.date DESC LIMIT %s) as q ORDER BY q.date" % (company_id, date, limit)
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return result

    def getHistoryWithQ(self, company_id, limit, dateQ):
        query = "SELECT histories.date as conversion FROM histories left join currencies on currencies.symbol = histories.currency WHERE company_id = '%s' AND histories.date<'%s' ORDER BY histories.date DESC LIMIT 1" % (company_id, dateQ)
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False

        date = dateQ.split()[0].split("-");
        dateT = datetime(int(date[0]), int(date[1]), int(date[2]))
        diff = result[0][0]-dateT.date()
        if abs(diff.days)>10:
            return False

        query = "SELECT * from (SELECT histories.open as conversion FROM histories left join currencies on currencies.symbol = histories.currency WHERE company_id = '%s' AND histories.date<'%s' ORDER BY histories.date DESC LIMIT %s) as query where conversion is not null" % (company_id, dateQ, limit)
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
        query = "SELECT id FROM companiesSVM4 WHERE company_id = '%s' AND svm = '%s' AND kernel = '%s' AND number_of_days_sample = '%s' AND number_of_train_vectors = '%s' " % (company, svm, kernel, numberOfDaysSample, numberOfTrainVectors)
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return True

#plot

    def getCompanyToPlotSVM(self, currencySymbols):
        inQuery = ""
        if type(currencySymbols) is list:
            for i in range(0, len(currencySymbols)):
                inQuery+="'"+currencySymbols[i]+"',"
            inQuery = " AND currency IN ("+inQuery[:-1]+")"
        else:
            inQuery = " AND currency IN ('"+currencySymbols+"')"

        query = "SELECT (rate*100), profitability_percentage*100 FROM companiesSVM4 svm JOIN companies c ON c.id = svm.company_id WHERE rate > 0 %s"  % (inQuery) #AND profitability_percentage > -1.1 AND profitability_percentage < 1.1
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return result

    def getCompanyToPlotSector(self, currencySymbols):
        inQuery = ""
        if type(currencySymbols) is list:
            inQueryP = ""
            for i in range(0, len(currencySymbols)):
                inQueryP+="'"+currencySymbols[i]+"',"
            inQuery = " AND s.name IN ("+inQueryP[:-1]+")"
        else:
            inQuery = " AND s.name IN ('"+currencySymbols+"')"

        query = "SELECT (rate*100), profitability_percentage  FROM companiesSVMWithQ2 svm JOIN companies c ON c.id = svm.company_id JOIN industries i ON i.id = c.industry_id JOIN sectors s ON s.id = i.sector_id WHERE rate > 0 %s"  % (inQuery)
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return result

    def getCompanyToPlotSectorDiff(self, currencySymbols):
        inQuery = ""
        if type(currencySymbols) is list:
            inQueryP = ""
            for i in range(0, len(currencySymbols)):
                inQueryP+="'"+currencySymbols[i]+"',"
            inQuery = " AND s.name IN ("+inQueryP[:-1]+")"
        else:
            inQuery = " AND s.name IN ('"+currencySymbols+"')"

        query = "SELECT (rate*100), (profitability_percentage_with_alg-profitability_percentage)*100  FROM companiesSVMWithQ2 svm JOIN companies c ON c.id = svm.company_id JOIN industries i ON i.id = c.industry_id JOIN sectors s ON s.id = i.sector_id WHERE rate > 0 %s"  % (inQuery)
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return result

    def getCompanyToPlotSectorByQ(self, currencySymbols, qDates, withAlg=""):
        inQuery = ""
        if type(currencySymbols) is list:
            for i in range(0, len(currencySymbols)):
                inQuery+="'"+currencySymbols[i]+"',"
            inQuery = " AND S.name IN ("+inQuery[:-1]+")"
        else:
            inQuery = " AND S.name IN ('"+currencySymbols+"')"
        if type(qDates) is list:
            for i in range(0, len(qDates)):
                inQueryP+="'"+qDates[i]+"',"
            inQuery += " AND svm.date_q IN ("+inQueryP[:-1]+")"
        else:
            inQuery += " AND svm.date_q IN ('"+qDates+"')"

        query = "SELECT (rate*100), profitability_percentage%s*100 FROM companiesSVMWithQ2 svm JOIN companies c ON c.id = svm.company_id JOIN industries i ON i.id = c.industry_id JOIN sectors s ON s.id = i.sector_id WHERE rate > 0 %s AND profitability_percentage%s > 0"  % (withAlg, inQuery, withAlg)
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return result

    def getCompanyToPlotSectorByQDiff(self, currencySymbols, qDates):
        inQuery = ""
        if type(currencySymbols) is list:
            for i in range(0, len(currencySymbols)):
                inQuery+="'"+currencySymbols[i]+"',"
            inQuery = " AND S.name IN ("+inQuery[:-1]+")"
        else:
            inQuery = " AND S.name IN ('"+currencySymbols+"')"
        if type(qDates) is list:
            for i in range(0, len(qDates)):
                inQueryP+="'"+qDates[i]+"',"
            inQuery += " AND svm.date_q IN ("+inQueryP[:-1]+")"
        else:
            inQuery += " AND svm.date_q IN ('"+qDates+"')"

        query = "SELECT (rate*100), (profitability_percentage_with_alg-profitability_percentage)*100 FROM companiesSVMWithQ2 svm JOIN companies c ON c.id = svm.company_id JOIN industries i ON i.id = c.industry_id JOIN sectors s ON s.id = i.sector_id WHERE rate > 0 %s AND profitability_percentage >0 AND profitability_percentage_with_alg > 0"  % (inQuery)
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return result

    def getCompanyToPlotCurrencyByQ(self, currencySymbols, qDates, withAlg=""):
        inQuery = ""
        if type(currencySymbols) is list:
            for i in range(0, len(currencySymbols)):
                inQuery+="'"+currencySymbols[i]+"',"
            inQuery = " AND currency IN ("+inQuery[:-1]+")"
        else:
            inQuery = " AND currency IN ('"+currencySymbols+"')"
        if type(qDates) is list:
            inQueryP = ""
            for i in range(0, len(qDates)):
                inQueryP+="'"+qDates[i]+"',"
            inQuery += " AND svm.date_q IN ("+inQuery[:-1]+")"
        else:
            inQuery += " AND svm.date_q IN ('"+qDates+"')"

        query = "SELECT (rate*100), profitability_percentage%s*100 FROM companiesSVMWithQ2 svm JOIN companies c ON c.id = svm.company_id JOIN industries i ON i.id = c.industry_id JOIN sectors s ON s.id = i.sector_id WHERE rate > 0 %s AND profitability_percentage%s > 0"  % (withAlg, inQuery, withAlg)
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return result

    def getCompanyToPlotCurrencyByQDiff(self, currencySymbols, qDates):
        inQuery = ""
        if type(currencySymbols) is list:
            for i in range(0, len(currencySymbols)):
                inQuery+="'"+currencySymbols[i]+"',"
            inQuery = " AND currency IN ("+inQuery[:-1]+")"
        else:
            inQuery = " AND currency IN ('"+currencySymbols+"')"
        if type(qDates) is list:
            inQueryP = ""
            for i in range(0, len(qDates)):
                inQueryP+="'"+qDates[i]+"',"
            inQuery += " AND svm.date_q IN ("+inQuery[:-1]+")"
        else:
            inQuery += " AND svm.date_q IN ('"+qDates+"')"

        query = "SELECT (rate*100), (profitability_percentage_with_alg-profitability_percentage)*100 FROM companiesSVMWithQ2 svm JOIN companies c ON c.id = svm.company_id JOIN industries i ON i.id = c.industry_id JOIN sectors s ON s.id = i.sector_id WHERE rate > 0 %s AND profitability_percentage > 0 AND profitability_percentage_with_alg>0"  % (inQuery)
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return result

    def getCompanyToPlotCurrencyDiff(self, currencySymbols):
        inQuery = ""
        if type(currencySymbols) is list:
            for i in range(0, len(currencySymbols)):
                inQuery+="'"+currencySymbols[i]+"',"
            inQuery = " AND currency IN ("+inQuery[:-1]+")"
        else:
            inQuery = " AND currency IN ('"+currencySymbols+"')"

        query = "SELECT (rate*100), (profitability_percentage_with_alg-profitability_percentage)*100 FROM companiesSVMWithQ2 svm JOIN companies c ON c.id = svm.company_id JOIN industries i ON i.id = c.industry_id JOIN sectors s ON s.id = i.sector_id WHERE rate > 0 %s AND profitability_percentage > 0 AND profitability_percentage_with_alg>0"  % (inQuery)
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return result

    def getCompaniesToPlotDiff(self):

        query = "SELECT (rate*100), (profitability_percentage_with_alg-profitability_percentage)*100 FROM companiesSVMWithQ2 svm JOIN companies c ON c.id = svm.company_id JOIN industries i ON i.id = c.industry_id JOIN sectors s ON s.id = i.sector_id WHERE rate > 0 AND profitability_percentage > 0 AND profitability_percentage_with_alg>0"
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return result

    def getCompaniesToPlotPercentage(self):

        query = "SELECT rate, profitability_percentage FROM companiesSVC svm JOIN companies c ON c.id = svm.company_id JOIN industries i ON i.id = c.industry_id JOIN sectors s ON s.id = i.sector_id WHERE rate > 0 AND profitability_percentage > 0 AND profitability_percentage_with_alg>0 ORDER BY rate"
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return result

    def getCompaniesToPlotAlg(self):

        query = "SELECT rate, profitability_percentage_with_alg FROM companiesSVC svm JOIN companies c ON c.id = svm.company_id JOIN industries i ON i.id = c.industry_id JOIN sectors s ON s.id = i.sector_id WHERE rate > 0 AND profitability_percentage > 0 AND profitability_percentage_with_alg>0 ORDER BY rate"
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return result

    def getCompaniesToPlotEMS(self):

        query = "SELECT rate_ems, profitability_percentage_with_ems FROM companiesSVC svm JOIN companies c ON c.id = svm.company_id JOIN industries i ON i.id = c.industry_id JOIN sectors s ON s.id = i.sector_id WHERE rate > 0 AND profitability_percentage > 0 AND profitability_percentage_with_alg>0 ORDER BY rate"
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return result

    def getCompanyToPlotQ(self, qDates):
        inQuery = ""
        if type(qDates) is list:
            for i in range(0, len(qDates)):
                inQuery+="'"+qDates[i]+"',"
            inQuery = " AND svm.date_q IN ("+inQuery[:-1]+")"
        else:
            inQuery = " AND svm.date_q IN ('"+qDates+"')"

        query = "SELECT (rate*100), profitability_percentage_with_alg*100 FROM companiesSVMWithQ2 svm WHERE rate > 0 %s"  % (inQuery) #AND profitability_percentage > -1.1 AND profitability_percentage < 1.1
        result = Database().runQuery(query)
        if not result or not result[0]:
            return False
        return result
