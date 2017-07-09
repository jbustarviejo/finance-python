from scrapping.ScrapSectors import ScrapSectors
from database.dbInsert import *

print "--Staring scrapping script--"

print "\nScrapping sectors..."
sectors = ScrapSectors().scrap_sectors()
dbInsert().saveSectors(sectors)
print "Finished!"

print("\n--Scrapping script finished--")
