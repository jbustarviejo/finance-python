from database.dbGet import *
from database.dbInsert import *

import numpy as np
import operator
from sklearn.svm import SVC

def optParamsSVC(companies, recover):
    predictions = []
    repeats = 244
    for kernel in ["linear", "sigmoid", "rbf"]:
        for numberOfDaysSample in [5, 19, 61, 122, 244]:
            for numberOfTrainVectors in [5, 19, 61, 122, 244]:
                print ("SVC - "+str(companies[0])+" -  Kernel: "+kernel+", sample: "+str(numberOfDaysSample)+", train vectors="+str(numberOfTrainVectors)+", repeats= "+str(repeats))
                prediction = {}
                if recover is True:
                    if DbGet().getIfCompanyProcessed(companies[0], "svc", kernel, numberOfDaysSample, numberOfTrainVectors) is True:
                        continue
                rate = getPredictionRate(companies[0], False, kernel, numberOfDaysSample, numberOfTrainVectors, repeats);
                if rate is None:
                    rate = -2
                # prediction["rate"] = rate
                # prediction["kernel"] = kernel;
                # prediction["numberOfDaysSample"] = numberOfDaysSample;
                # prediction["numberOfTrainVectors"] = numberOfTrainVectors;
                # prediction["repeats"] = repeats;
                # predictions.append(prediction);
                DbInsert().saveOptSVM(companies[0], "svc", kernel, rate, numberOfDaysSample, numberOfTrainVectors)
    # #print predictions
    # #Get the maximun and minimun value
    # if not predictions or len(predictions) <1:
    #     return None
    # #Return result
    # result = getMaxAndMin(predictions)
    # return result

def optParamsSVCR(companies, recover): #Opt SVC with profibility
    predictions = []
    repeats = 244
    for kernel in ["linear", "sigmoid", "rbf"]:
        for numberOfDaysSample in [5, 19, 61, 122, 244]:
            for numberOfTrainVectors in [5, 19, 61, 122, 244]:
                print ("SVCR - "+str(companies[0])+" -  Kernel: "+kernel+", sample: "+str(numberOfDaysSample)+", train vectors="+str(numberOfTrainVectors)+", repeats= "+str(repeats))
                prediction = {}
                if recover is True:
                    if DbGet().getIfCompanyProcessed(companies[0], "svcr", kernel, numberOfDaysSample, numberOfTrainVectors) is True:
                        continue
                rate = getPredictionRate(companies[0], True, kernel, numberOfDaysSample, numberOfTrainVectors, repeats);
                if rate is None:
                    rate = -2
                # prediction["rate"] = rate
                # prediction["kernel"] = kernel;
                # prediction["numberOfDaysSample"] = numberOfDaysSample;
                # prediction["numberOfTrainVectors"] = numberOfTrainVectors;
                # prediction["repeats"] = repeats;
                # predictions.append(prediction);
                DbInsert().saveOptSVM(companies[0], "svcr", kernel, rate, numberOfDaysSample, numberOfTrainVectors)
    # #print predictions
    # #Get the maximun and minimun value
    # if not predictions or len(predictions) <1:
    #     return None
    # #Return result
    # result = getMaxAndMin(predictions)
    # return result

def getMaxAndMin(predictions):
    max = predictions[0]
    min = predictions[0]
    for i in range(1, len(predictions)):
        if predictions[i]["rate"] is None:
            continue
        if max["rate"] < predictions[i]["rate"]:
            max = predictions[i]
        if min["rate"] > predictions[i]["rate"]:
            min = predictions[i]

    result = {}
    result["max"] = max
    result["min"] = min
    return result;


def getPredictionRate(company, profibility, kernel, numberOfDaysSample, numberOfTrainVectors, repeats):
    prediction = predictCompany(company, profibility, kernel, numberOfDaysSample, numberOfTrainVectors, repeats)
    print ("Prediction " + str(prediction) + "%")
    return prediction

def predictCompany(company_id, profibility, kernel, numberOfDaysSample, numberOfTrainVectors, repeats):
    #Config
    #outputLength=1
    #numberOfTestVectors=1

    numberOfDaysSample = numberOfDaysSample + 1

    data = DbGet().getHistory(company_id, numberOfDaysSample + numberOfTrainVectors + repeats -1);
    if data == False or len(data) < numberOfDaysSample + numberOfTrainVectors + repeats - 1:
        print ("Not enough length")
        return -1

    data = [s[0] for s in data if s[0]] #Transform tuples to int array
    # print "data=" + str(data);

    if profibility is True:
        for k in reversed(range(1,len(data))):
            data[k] = data[k]/data[k-1]

        data[0] = 1
        # print "data2=" + str(data);

    for l in reversed(range(1,len(data))):
        if data[l] > data[l-1]:
            data[l] = 1
        else:
            data[l] = -1

    data[0] = 1

    #Give format to Y and X in chunks
    X = []
    Y = []
    for j in range(0, len(data) - numberOfDaysSample + 1):
        chunk = data[j : j+numberOfDaysSample]
        X.append(chunk[:-1])
        Y.append(chunk[-1])

    ###print "X0=" + str(np.asarray(X))
    ###print "Y0=" + str(np.asarray(Y))
    ###print ""

    #Iterate to get average result
    predictions=[]
    for i in range(0, repeats):
        profibilityString = "SVC"
        if profibility:
            profibilityString = "SVCR"
        print ("C"+str(company_id)+": "+profibilityString+str(i)+"/"+str(repeats)+". Kernel: "+str(kernel)+". Days: "+ str(numberOfDaysSample-1)+ ". TrainVectors: "+str(numberOfTrainVectors))
        finalPos = i+1-repeats
        if finalPos != 0:
            x = np.asarray(X[i:finalPos])
            y = np.asarray(Y[i:finalPos])
        else:
            x = np.asarray(X[i:])
            y = np.asarray(Y[i:])

        ###print "x=" + str(x)
        ###print "y=" + str(y)

        predictions.append(testPrediction(x, y, kernel))

    return np.average(predictions)

def testPrediction(X, Y, kernel):
        #Train
        x_train = np.asarray(X[:-1])
        y_train = np.asarray(Y[:-1])

        #Test
        x_test = np.asarray(X[-1])
        y_test = np.asarray(Y[-1])

        x_test_1 = x_test[-1]

        import warnings
        warnings.filterwarnings('ignore')
        try:
            predictions = SVC(kernel=kernel).fit(x_train, y_train).predict(x_test.reshape(1, -1))
        except ValueError:
            return np.asarray([True]) #All are the same

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
