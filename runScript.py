from analysis.Analize import *
import os
import random

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
years=[2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016]
random.shuffle(years)
for year in years:
    months = [1, 4, 7, 10]
    random.shuffle(months)
    for min_month in months:
        print("=====> Analize "+str(year)+" month: "+str(min_month))
        Analize().analizeSVCCompanies(year, min_month, min_month+2)

print("\n\n------Analysis script finished------\n")

exit()
