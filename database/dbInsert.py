from database.Connect import Database
from mysql.connector.errors import OperationalError

class DbInsert:

    #Save sectors array in database
    def saveSectors(self, sectors):

        valuesQuery = []
        for sector in sectors:
            valuesQuery.append("('%s', '%s', '%s', '%s', NOW(), NOW())" % (sector["sector_name"], sector["sector_slug"], sector["sector_industries"], sector["sector_companies"]) )

        queryValues = ",".join(str(item) for item in valuesQuery)
        query = "INSERT INTO sectors (name, slug, industries, companies, created_at, updated_at) VALUES %s ON DUPLICATE KEY UPDATE name=VALUES(name), slug=VALUES(slug), industries=VALUES(industries), companies=VALUES(companies), updated_at=NOW()" % queryValues
        Database().runQuery(query)


    #Save industries array in database
    def saveIndustries(self, industries):

        valuesQuery = []
        for industry in industries:
            valuesQuery.append("('%s', '%s', '%s', NOW(), NOW())" % (industry["industry_name"], industry["industry_slug"], industry["sector_id"]) )

        queryValues = ",".join(str(item) for item in valuesQuery)
        query = "INSERT INTO industries (name, slug, sector_id, created_at, updated_at) VALUES %s ON DUPLICATE KEY UPDATE name=VALUES(name), slug=VALUES(slug), sector_id=VALUES(sector_id), updated_at=NOW()" % queryValues
        Database().runQuery(query)


    #Save companies array in database
    def saveCompanies(self, companies):

        valuesQuery = []
        for company in companies:
            valuesQuery.append("('%s', '%s', '%s', NOW(), NOW())" % (company["company_symbol"].replace("'","\\'"), company["company_name"].replace("'","\\'"), company["industry_id"]) )

        queryValues = ",".join(str(item) for item in valuesQuery)
        query = "INSERT INTO companies (symbol, name, industry_id, created_at, updated_at) VALUES %s ON DUPLICATE KEY UPDATE symbol=VALUES(symbol), name=VALUES(name), industry_id=VALUES(industry_id), updated_at=NOW()" % queryValues
        try:
            Database().runQuery(query)
        except OperationalError:
            #If lock error don't do nothing
            print "========Thread doing lock violantion========"
