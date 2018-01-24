from analysis.Analize import *

print ("--Staring analysis script--")

#companies = DbGet().getCompaniesByCurrency(["USD", "JPY"]);
#print companies
#optParams = optParamsSVR(9999)

# SVRAndSVRR for a given currency
Analize().analizeSVRAndSVCCompanies("USD", False)
#Recover!
# Analize().analizeSVRAndSVCCompanies("USD", True)

print("--Analysis script finished--")

exit()
