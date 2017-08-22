from analysis.CompanyAnalysis import *
import numpy as np
from database.DbGet import *

print "--Staring analysis script--"
predictions = []

print DbGet().getCompaniesByCurrency("USD");

exit
for i in xrange(0, 50000):
    prediction = predictCompany(i)
    if prediction:
        predictions.append(prediction)
    if i>0 and i%10==0:
        print np.average(predictions)

print np.average(predictions)
print("--Analysis script finished--")
exit()
