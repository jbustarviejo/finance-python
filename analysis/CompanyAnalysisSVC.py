from database.DbGet import *
import numpy as np
import operator
from sklearn.svm import SVC

def optParamsSVC(companies):
    predictions = []
    for kernel in ["linear", "rbf", "sigmoid"]: #"poly",
        print "---------- Kernel: "+kernel+" ----------"
        for shrinking in [True, False]:
            print "---------- Shrinking: "+str(shrinking)+" ----------"
            for C in range(1,100,5):
                print "---------- C: %f ----------" % (float(C/10))
                prediction = {}
                prediction["rate"] = getPredictionRate(companies, kernel, shrinking, C);
                prediction["kernel"] = kernel;
                prediction["C"] = C;
                predictions.append(prediction);
    # print predictions
    #Get the maximun and minimun value
    maxIndex, maxValue = max(enumerate(predictions), key=operator.itemgetter(0))
    minIndex, minValue = min(enumerate(predictions), key=operator.itemgetter(0))
    #Return result
    result = {}
    result["max"] = maxValue
    result["min"] = minValue
    return result

def getPredictionRate(companies, kernel, shrinking, C):
    predictions = []
    for i in xrange(0, len(companies)):
        prediction = predictCompany(companies[i][0], kernel, shrinking, C)
        if prediction:
            predictions.append(prediction)
        if i>0 and i%10==0:
            print str(i*100/len(companies)) + "%: prediction " + str(np.average(predictions))

    return np.average(predictions)

def predictCompany(company_id, kernel, shrinking, C):
    #Config
    numberOfDaysSample = 5;
    #outputLength=1
    #numberOfTestVectors=1
    numberOfTrainVectors = 40;
    repeats = 100;

    data = DbGet().getHistory(company_id, numberOfDaysSample + numberOfTrainVectors + repeats -1);
    if data == False or len(data) < numberOfDaysSample + numberOfTrainVectors + repeats - 1:
        #print "Not enough length"
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

        predictions.append(testPrediction(x, y, kernel, shrinking, C))

    return np.average(predictions)

def testPrediction(X, Y, kernel, shrinking, C):
        #Train
        x_train = np.asarray(X[:-1])
        y_train = np.asarray(Y[:-1])

        #Test
        x_test = np.asarray(X[-1])
        y_test = np.asarray(Y[-1])

        x_test_1 = x_test[-1]

        import warnings
        warnings.filterwarnings('ignore')
        predictions = C
        #predictions = SVC(kernel, shrinking=shrinking, C=C).fit(x_train, y_train).predict(x_test)

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
