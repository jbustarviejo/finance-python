from database.DbGet import *
import numpy as np
from sklearn.svm import SVR

def predictCompany(company_id):
    numberOfDaysSample = 100;
    #outputLength=1
    #numberOfTestVectors=1
    numberOfTrainVectors = 40;
    repeats = 100;
    data = DbGet().getHistoryInUSD(company_id, numberOfDaysSample + numberOfTrainVectors + repeats -1);
    if len(data) < numberOfDaysSample + numberOfTrainVectors + repeats - 1:
        print "Not enough length"
        return

    data = [s[0] for s in data if s[0]] #Transform tuples to int array
    ##print "data=" + str(data);

    #Give format to Y and X in chunks
    X = []
    Y = []
    for j in xrange(0, len(data) - numberOfDaysSample + 1):
        chunk = data[j : j+numberOfDaysSample]
        X.append(chunk[:-1])
        Y.append(chunk[-1])

    ###print "X0=" + str(np.asarray(X))
    ###print "Y0=" + str(np.asarray(Y))
    ###print ""

    #Iterate to get average result
    predictions=[]
    for i in xrange(0, repeats):
        ###print "--------------iter:"+str(i)
        finalPos = i+1-repeats
        if finalPos != 0:
            x = np.asarray(X[i:finalPos])
            y = np.asarray(Y[i:finalPos])
        else:
            x = np.asarray(X[i:])
            y = np.asarray(Y[i:])

        initialValue = x[0][0] #Get profibility
        x = x/initialValue
        y = y/initialValue

        ###print "x=" + str(x)
        ###print "y=" + str(y)

        predictions.append(testPrediction(x, y))

    print np.average(predictions)
    return


def testPrediction(X, Y):
        #Train
        x_train = np.asarray(X[:-1])
        y_train = np.asarray(Y[:-1])

        #Test
        x_test = np.asarray(X[-1])
        y_test = np.asarray(Y[-1])

        x_test_1 = x_test[-1]

        import warnings
        warnings.filterwarnings('ignore')
        predictions = SVR().fit(x_train, y_train).predict(x_test)

        ### print "x_train=" + str(x_train)
        ### print "y_train=" + str(y_train)
        ### print "x_test=" + str(x_test)
        ### print "y_test=" + str(y_test)
        ### print "x_test_1=" + str(x_test_1)
        ### print "predictions=" + str(predictions)

        expected = y_test > x_test_1
        predicted = predictions > x_test_1
        ###print expected == predicted

        return expected == predicted
