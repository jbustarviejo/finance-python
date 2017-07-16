from database.connect import database

class dbInsert:

    #Save sectors array in database
    def saveSectors(self, sectors):

        valuesQuery = []
        for sector in sectors:
            valuesQuery.append("('%s', '%s', '%s', '%s', NOW(), NOW())" % (sector["sector_name"], sector["sector_slug"], sector["sector_industries"], sector["sector_companies"]) )

        queryValues = ",".join(str(item) for item in valuesQuery)
        query = "INSERT INTO sectors (name, slug, industries, companies, created_at, updated_at) VALUES %s ON DUPLICATE KEY UPDATE name=VALUES(name), slug=VALUES(slug), industries=VALUES(industries), companies=VALUES(companies), updated_at=NOW()" % queryValues
        database().runQuery(query)

    #Save industries array in database
    def saveIndustries(self, industries):

        valuesQuery = []
        for industry in industries:
            valuesQuery.append("('%s', '%s', '%s', NOW(), NOW())" % (industry["industry_name"], industry["industry_slug"], industry["sector_id"]) )

        queryValues = ",".join(str(item) for item in valuesQuery)
        query = "INSERT INTO industries (name, slug, sector_id, created_at, updated_at) VALUES %s ON DUPLICATE KEY UPDATE name=VALUES(name), slug=VALUES(slug), sector_id=VALUES(sector_id), updated_at=NOW()" % queryValues
        database().runQuery(query)
