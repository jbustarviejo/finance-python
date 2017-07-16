from scrapping.Scrap import *

print "--Staring scrapping script--"

print "\nScrapping sectors..."
Scrap().scrapSectors
print "Finished sectors scrapping!"

print "\nScrapping industries..."
Scrap().scrapIndustries()
print "Finished industries scrapping!"

print "\nScrapping companies list..."
Scrap().scrapCompanies()
print "Finished companies scrapping!"

print("\n--Scrapping script finished--")
exit()
