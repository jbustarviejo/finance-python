from scrapping.ScrapSectors import ScrapSectors
from scrapping.ScrapIndustries import ScrapIndustries
from database.dbInsert import *

print "--Staring scrapping script--"

print "\nScrapping sectors..."
sectors = ScrapSectors().scrapSectors()
dbInsert().saveSectors(sectors)
print "Finished!"

print "\nScrapping industries..."
while(True):
    industries = ScrapIndustries().scrapIndustries()
    if not industries:
        break;
    dbInsert().saveIndustries(industries)
print "Finished!"

print("\n--Scrapping script finished--")
