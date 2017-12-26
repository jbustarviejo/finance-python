from scrapping.Scrap import *

print ("--Staring scrapping script--")

print ("\nScrapping sectors...")
Scrap().scrapSectors()
print ("Finished sectors scrapping!")

print ("\nScrapping industries...")
Scrap().scrapIndustries()
print ("Finished industries scrapping!")

print ("\nScrapping companies list...")
Scrap().scrapCompanies()
print ("Finished companies scrapping!")

print ("\nScrapping companies history...")
#Scrap().scrapHistories() #Scrap all histories
Scrap().scrapHistories("INR") #Scrap a currency histories
print ("Finished companies history scrapping!")

print( "\nScrapping currencies...")
Scrap().scrapCurrencies()
print ("Finished currencies scrapping!")

print("\n--Scrapping script finished--")
exit()
