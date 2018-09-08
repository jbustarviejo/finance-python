from analysis.Analize import *
import os

os.system('clear') #Clear
print ("--Staring analysis script--")

#companies = DbGet().getCompaniesByCurrency(["USD", "JPY"]);
#print companies
#optParams = optParamsSVR(9999)

# SVRAndSVRR for a given currency
#Analize().analizeSVRAndSVCCompanies("INR")
#All!
#Analize().analizeSVRAndSVCCompanies()
#Recover
# Analize().analizeSVRAndSVCCompanies(True)
#AllWothQ
# Analize().analizeSVRAndSVCCompaniesWithQ()
# All companies for SVC
for year in [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016]:
    for min_month in [1, 4, 7, 10]:
        Analize().analizeSVCCompanies(year, min_month, min_month+2)

print("\n\n------Analysis script finished------\n")

exit()
