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
Analize().analizeSVCCompanies()

print("\n\n------Analysis script finished------\n")

exit()
