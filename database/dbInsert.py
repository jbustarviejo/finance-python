from database.connect import database

class dbInsert:

    #Save sectors array in database
    def saveSectors(self, sectors):

        valuesQuery = []
        for sector in sectors:
            valuesQuery.append("('%s', '%s', '%s', '%s', NOW(), NOW())" % (sector["sector_name"], sector["sector_link"], sector["sector_industries"], sector["sector_companies"]) )

        queryValues = ",".join(str(item) for item in valuesQuery)
        query = "INSERT INTO sectors (name, link, industries, companies, created_at, updated_at) VALUES %s ON DUPLICATE KEY UPDATE name=VALUES(name), link=VALUES(link), industries=VALUES(industries), companies=VALUES(companies), updated_at=NOW()" % queryValues
        database().runQuery(query)
