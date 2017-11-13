from analysis.Analize import *

print "--Staring analysis script--"

#companies = DbGet().getCompaniesByCurrency(["USD", "JPY"]);
#print companies
#optParams = optParamsSVR(9999)
Analize().analizeSVRCompanies()

print("--Analysis script finished--")

exit()
