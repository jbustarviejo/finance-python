from database.connect import Database

class DbInsert:

    #Save sectors array in database
    def saveSectors(self, sectors):
        valuesQuery = []
        for sector in sectors:
            valuesQuery.append("('%s', '%s', '%s', '%s', NOW(), NOW())" % (sector["sector_name"], sector["sector_slug"], sector["sector_industries"], sector["sector_companies"]) )

        if not valuesQuery:
            return
        queryValues = ",".join(str(item) for item in valuesQuery)
        query = "INSERT INTO sectors (name, slug, industries, companies, created_at, updated_at) VALUES %s ON DUPLICATE KEY UPDATE name=VALUES(name), slug=VALUES(slug), industries=VALUES(industries), companies=VALUES(companies), updated_at=NOW()" % queryValues
        Database().runQuery(query)


    #Save industries array in database
    def saveIndustries(self, industries):
        valuesQuery = []
        for industry in industries:
            valuesQuery.append("('%s', '%s', '%s', NOW(), NOW())" % (industry["industry_name"], industry["industry_slug"], industry["sector_id"]) )

        if not valuesQuery:
            return
        queryValues = ",".join(str(item) for item in valuesQuery)
        query = "INSERT INTO industries (name, slug, sector_id, created_at, updated_at) VALUES %s ON DUPLICATE KEY UPDATE name=VALUES(name), slug=VALUES(slug), sector_id=VALUES(sector_id), updated_at=NOW()" % queryValues
        Database().runQuery(query)


    #Save companies array in database
    def saveCompanies(self, companies):
        valuesQuery = []
        for company in companies:
            valuesQuery.append("('%s', '%s', '%s', NOW(), NOW())" % (company["company_symbol"].replace("'","\\'"), company["company_name"].replace("'","\\'"), company["industry_id"]) )

        if not valuesQuery:
            return
        queryValues = ",".join(str(item) for item in valuesQuery)
        query = "INSERT INTO companies (symbol, name, industry_id, created_at, updated_at) VALUES %s ON DUPLICATE KEY UPDATE symbol=VALUES(symbol), name=VALUES(name), industry_id=VALUES(industry_id), updated_at=NOW()" % queryValues
        try:
            Database().runQuery(query)
        except MySQLError:
            #If lock error don't do nothing
            print ("========Thread doing lock violantion========")

    #Save company Xid array in database
    def updateCompanyXidAndCurrency(self, company_id, values):
        if(not values or not values["xid"] or not values["currency"]):
            return
        query = "UPDATE companies SET xid = %s, currency= '%s' WHERE id = %s" % (values["xid"], values["currency"], company_id)
        try:
            Database().runQuery(query)
        except MySQLError:
            #If lock error don't do nothing
            print ("========Thread doing lock violantion========")

    #Save company currency array in database
    def updateCompanyCurrency(self, company_id, currency):
        query = "UPDATE companies SET currency = %s WHERE id = %s" % (xid, company_id)
        try:
            Database().runQuery(query)
        except MySQLError:
            #If lock error don't do nothing
            print ("========Thread doing lock violantion========")

    #Save history array in database
    def saveHistory(self, histories):
        valuesQuery = []
        for history in histories:
            valuesQuery.append("('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', NOW(), NOW())" % (history["company_id"], history["currency"], history["date"], history["open"], history["high"], history["low"], history["close"], history["volume"]) )

        if not valuesQuery:
            return
        queryValues = ",".join(str(item) for item in valuesQuery)
        query = "INSERT INTO histories (company_id, currency, date, open, high, low, close, volume, created_at, updated_at) VALUES %s ON DUPLICATE KEY UPDATE company_id=VALUES(company_id), currency=VALUES(currency), date=VALUES(date), open=VALUES(open), high=VALUES(high), close=VALUES(close), volume=VALUES(volume), updated_at=NOW()" % queryValues
        try:
            Database().runQuery(query)
        except MySQLError:
            #If lock error don't do nothing
            print ("========Thread doing lock violantion========")

    #Save currenciy list array in database
    def saveCurrencies(self, currencies):
        valuesQuery = []
        for currency in currencies:
            valuesQuery.append("('%s', '%s', NOW(), NOW())" % (currency["name"].replace("'","\\'"), currency["symbol"]) )

        if not valuesQuery:
            return
        queryValues = ",".join(str(item) for item in valuesQuery)
        query = "INSERT INTO currencies (name, symbol, created_at, updated_at) VALUES %s ON DUPLICATE KEY UPDATE symbol=VALUES(symbol), name=VALUES(name), updated_at=NOW()" % queryValues
        try:
            Database().runQuery(query)
        except MySQLError:
            #If lock error don't do nothing
            print ("========Thread doing lock violantion========")

    #Save currency Xid array in database
    def updateCurrencyXidToUSD(self, currency_id, xid):
        query = "UPDATE currencies SET xidToUSD = %s WHERE id = %s" % (xid, currency_id)
        try:
            Database().runQuery(query)
        except MySQLError:
            #If lock error don't do nothing
            print ("========Thread doing lock violantion========")

    #Save currency Xid array in database
    def updateCurrencyXidFromUSD(self, currency_id, xid):
        query = "UPDATE currencies SET xidFromUSD = %s WHERE id = %s" % (xid, currency_id)
        try:
            Database().runQuery(query)
        except MySQLError:
            #If lock error don't do nothing
            print ("========Thread doing lock violantion========")

    #Save currency history array in database
    def saveCurrencyHistory(self, histories):
        valuesQuery = []
        for history in histories:
            valuesQuery.append("('%s', '%s', '%s', NOW(), NOW())" % (history["currency_id"], history["date"], history["price"]) )

        if not valuesQuery:
            return
        queryValues = ",".join(str(item) for item in valuesQuery)
        query = "INSERT INTO currencyHistoryToUSD (currency_id, date, price, created_at, updated_at) VALUES %s ON DUPLICATE KEY UPDATE currency_id=VALUES(currency_id), date=VALUES(date), price=VALUES(price), updated_at=NOW()" % queryValues
        try:
            Database().runQuery(query)
        except MySQLError:
            #If lock error don't do nothing
            print ("========Thread doing lock violantion========")

    #--------From analysis--------

    #Save optimized SVR of company
    def saveOptSVR(self, companyId, max, min):
        query = "INSERT INTO companiesSVR (company_id, max_kernel, max_rate, max_repeats, max_samples, max_train_vectors, min_kernel, min_rate, min_repeats, min_samples, min_train_vectors, created_at, updated_at) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s', NOW(), NOW()) ON DUPLICATE KEY UPDATE max_rate = IF(VALUES(max_rate) > max_rate, VALUES(max_rate), max_rate), max_kernel = IF(VALUES(max_rate) > max_rate, VALUES(max_kernel), max_kernel), max_repeats = IF(VALUES(max_rate) > max_rate, VALUES(max_repeats), max_repeats), max_samples = IF(VALUES(max_rate) > max_rate, VALUES(max_samples), max_samples), max_train_vectors = IF(VALUES(max_rate) > max_rate, VALUES(max_train_vectors), max_train_vectors), min_rate = IF(VALUES(min_rate) < min_rate, VALUES(min_rate), min_rate), min_kernel = IF(VALUES(min_rate) < min_rate, VALUES(min_kernel), min_kernel), min_repeats = IF(VALUES(min_rate) < min_rate, VALUES(min_repeats), min_repeats), min_samples = IF(VALUES(min_rate) < min_rate, VALUES(min_samples), min_samples), min_train_vectors = IF(VALUES(min_rate) < min_rate, VALUES(min_train_vectors), min_train_vectors)" % (companyId, max["kernel"], max["rate"],  max["repeats"], max["numberOfDaysSample"], max["numberOfTrainVectors"], min["kernel"], min["rate"], min["repeats"], min["numberOfDaysSample"], min["numberOfTrainVectors"])
        Database().runQuery(query)

    #Save optimized SVR of company with profibility
    def saveOptSVRR(self, companyId, max, min):
        query = "INSERT INTO companiesSVRR (company_id, max_kernel, max_rate, max_repeats, max_samples, max_train_vectors, min_kernel, min_rate, min_repeats, min_samples, min_train_vectors, created_at, updated_at) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s', NOW(), NOW()) ON DUPLICATE KEY UPDATE max_rate = IF(VALUES(max_rate) > max_rate, VALUES(max_rate), max_rate), max_kernel = IF(VALUES(max_rate) > max_rate, VALUES(max_kernel), max_kernel), max_repeats = IF(VALUES(max_rate) > max_rate, VALUES(max_repeats), max_repeats), max_samples = IF(VALUES(max_rate) > max_rate, VALUES(max_samples), max_samples), max_train_vectors = IF(VALUES(max_rate) > max_rate, VALUES(max_train_vectors), max_train_vectors), min_rate = IF(VALUES(min_rate) < min_rate, VALUES(min_rate), min_rate), min_kernel = IF(VALUES(min_rate) < min_rate, VALUES(min_kernel), min_kernel), min_repeats = IF(VALUES(min_rate) < min_rate, VALUES(min_repeats), min_repeats), min_samples = IF(VALUES(min_rate) < min_rate, VALUES(min_samples), min_samples), min_train_vectors = IF(VALUES(min_rate) < min_rate, VALUES(min_train_vectors), min_train_vectors)" % (companyId, max["kernel"], max["rate"],  max["repeats"], max["numberOfDaysSample"], max["numberOfTrainVectors"], min["kernel"], min["rate"], min["repeats"], min["numberOfDaysSample"], min["numberOfTrainVectors"])
        Database().runQuery(query)

    #Save optimized SVC of company
    def saveOptSVC(self, companyId, max, min):
        query = "INSERT INTO companiesSVC (company_id, max_kernel, max_rate, max_repeats, max_samples, max_train_vectors, min_kernel, min_rate, min_repeats, min_samples, min_train_vectors, created_at, updated_at) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s', NOW(), NOW()) ON DUPLICATE KEY UPDATE max_rate = IF(VALUES(max_rate) > max_rate, VALUES(max_rate), max_rate), max_kernel = IF(VALUES(max_rate) > max_rate, VALUES(max_kernel), max_kernel), max_repeats = IF(VALUES(max_rate) > max_rate, VALUES(max_repeats), max_repeats), max_samples = IF(VALUES(max_rate) > max_rate, VALUES(max_samples), max_samples), max_train_vectors = IF(VALUES(max_rate) > max_rate, VALUES(max_train_vectors), max_train_vectors), min_rate = IF(VALUES(min_rate) < min_rate, VALUES(min_rate), min_rate), min_kernel = IF(VALUES(min_rate) < min_rate, VALUES(min_kernel), min_kernel), min_repeats = IF(VALUES(min_rate) < min_rate, VALUES(min_repeats), min_repeats), min_samples = IF(VALUES(min_rate) < min_rate, VALUES(min_samples), min_samples), min_train_vectors = IF(VALUES(min_rate) < min_rate, VALUES(min_train_vectors), min_train_vectors)" % (companyId, max["kernel"], max["rate"],  max["repeats"], max["numberOfDaysSample"], max["numberOfTrainVectors"], min["kernel"], min["rate"], min["repeats"], min["numberOfDaysSample"], min["numberOfTrainVectors"])
        Database().runQuery(query)

    #Save optimized SVC of company with profibility
    def saveOptSVCR(self, companyId, max, min):
        query = "INSERT INTO companiesSVCR (company_id, max_kernel, max_rate, max_repeats, max_samples, max_train_vectors, min_kernel, min_rate, min_repeats, min_samples, min_train_vectors, created_at, updated_at) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s', NOW(), NOW()) ON DUPLICATE KEY UPDATE max_rate = IF(VALUES(max_rate) > max_rate, VALUES(max_rate), max_rate), max_kernel = IF(VALUES(max_rate) > max_rate, VALUES(max_kernel), max_kernel), max_repeats = IF(VALUES(max_rate) > max_rate, VALUES(max_repeats), max_repeats), max_samples = IF(VALUES(max_rate) > max_rate, VALUES(max_samples), max_samples), max_train_vectors = IF(VALUES(max_rate) > max_rate, VALUES(max_train_vectors), max_train_vectors), min_rate = IF(VALUES(min_rate) < min_rate, VALUES(min_rate), min_rate), min_kernel = IF(VALUES(min_rate) < min_rate, VALUES(min_kernel), min_kernel), min_repeats = IF(VALUES(min_rate) < min_rate, VALUES(min_repeats), min_repeats), min_samples = IF(VALUES(min_rate) < min_rate, VALUES(min_samples), min_samples), min_train_vectors = IF(VALUES(min_rate) < min_rate, VALUES(min_train_vectors), min_train_vectors)" % (companyId, max["kernel"], max["rate"],  max["repeats"], max["numberOfDaysSample"], max["numberOfTrainVectors"], min["kernel"], min["rate"], min["repeats"], min["numberOfDaysSample"], min["numberOfTrainVectors"])
        Database().runQuery(query)

    #Save SVM analysis
    def saveOptSVM(self, companyId, svm, kernel, rates, numberOfDaysSample, numberOfTrainVectors):
        if (rates == -1 or rates ==-2):
            rate = -1
            proba = -1
            prof_total = 0
            prof_perc = 0
        else:
            rate = rates["rate"]
            proba = rates["proba"]
            prof_total = rates["prof_total"]
            prof_perc = rates["prof_perc"]
        query = "INSERT INTO companiesSVM4 (company_id, svm, kernel, rate, proba, number_of_days_sample, number_of_train_vectors, profitability_total, profitability_percentage, created_at, updated_at) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s', NOW(), NOW()) ON DUPLICATE KEY UPDATE company_id='%s', svm='%s', kernel='%s', rate='%s', proba='%s', number_of_days_sample='%s', number_of_train_vectors='%s', profitability_total='%s', profitability_percentage='%s'" % (companyId, svm, kernel, rate, proba, numberOfDaysSample, numberOfTrainVectors, prof_total, prof_perc, companyId, svm, kernel, rate, proba, numberOfDaysSample, numberOfTrainVectors, prof_total, prof_perc)
        Database().runQuery(query)

    def saveOptSVMWithQ(self, companyId, svm, kernel, rates, numberOfDaysSample, numberOfTrainVectors, dateQ):
        if (rates == -1 or rates ==-2):
            rate = -1
            proba = -1
            prof_total = 0
            prof_perc = 0
        else:
            rate = rates["rate"]
            proba = rates["proba"]
            prof_total = rates["prof_total"]
            prof_perc = rates["prof_perc"]
        query = "INSERT INTO companiesSVMWithQ (company_id, svm, kernel, rate, proba, number_of_days_sample, number_of_train_vectors, profitability_total, profitability_percentage, date_q, created_at, updated_at) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s', NOW(), NOW()) ON DUPLICATE KEY UPDATE company_id='%s', svm='%s', kernel='%s', rate='%s', proba='%s', number_of_days_sample='%s', number_of_train_vectors='%s', profitability_total='%s', profitability_percentage='%s', date_q='%s'" % (companyId, svm, kernel, rate, proba, numberOfDaysSample, numberOfTrainVectors, prof_total, prof_perc, dateQ, companyId, svm, kernel, rate, proba, numberOfDaysSample, numberOfTrainVectors, prof_total, prof_perc, dateQ)
        Database().runQuery(query)
