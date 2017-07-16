from connect import database
import Settings

class dbGet:

    #Get sector to scrap
    def getSectorToScrap(self):
        # Get a sector that never has been updated or is NULL
        query = "SELECT * from sectors WHERE (last_full_update IS NULL OR last_full_update > NOW() + INTERVAL " + str(Settings.maxTimeForUpdateIndustries) + " HOUR) LIMIT 1 FOR UPDATE"
        update = {"table": "sectors", "column": "last_full_update"} #Block the column for not being update in multithread cases
        result = database().runQuery(query, update)
        if not result or not result[0]:
            return False
        return result[0]
