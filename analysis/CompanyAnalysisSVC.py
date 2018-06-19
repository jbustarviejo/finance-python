from database.dbGet import *
from database.dbInsert import *

import numpy as np
import operator
from copy import copy as copy
from sklearn.svm import SVC

development = False

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
    for kernel in ["rbf"]:
        for numberOfDaysSample in [1]:
            for numberOfTrainVectors in [366]:
                print ("SVCR - "+str(companies[0])+" -  Kernel: "+kernel+", sample: "+str(numberOfDaysSample)+", train vectors="+str(numberOfTrainVectors)+", repeats= "+str(repeats))
                prediction = {}
                # if recover is True:
                #     if DbGet().getIfCompanyProcessed(companies[0], "svcr", kernel, numberOfDaysSample, numberOfTrainVectors) is True:
                #         continue
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


def optParamsSVCRWithQ(companies, recover): #Opt SVC with profibility
    predictions = []
    datesQ = ["2017-07-01 00:00:00", "2017-04-01 00:00:00", "2017-01-01 00:00:00", "2016-10-01 00:00:00", "2016-07-01 00:00:00", "2016-04-01 00:00:00", "2016-01-01 00:00:00", "2015-10-01 00:00:00", "2015-07-01 00:00:00", "2015-04-01 00:00:00", "2015-01-01 00:00:00", "2014-10-01 00:00:00", "2014-07-01 00:00:00", "2014-04-01 00:00:00", "2014-01-01 00:00:00"]
    repeats = 244
    for kernel in ["rbf"]:
        for numberOfDaysSample in [1]:
            for numberOfTrainVectors in [366]:
                for dateQ in datesQ:
                    print ("SVCR - "+str(dateQ)+" - "+str(companies[0])+" -  Kernel: "+kernel+", sample: "+str(numberOfDaysSample)+", train vectors="+str(numberOfTrainVectors)+", repeats= "+str(repeats))
                    prediction = {}

                    rate = getPredictionRate(companies[0], True, kernel, numberOfDaysSample, numberOfTrainVectors, repeats, dateQ);
                    if rate is None:
                        rate = -2

                    DbInsert().saveOptSVMWithQ(companies[0], "svcr", kernel, rate, numberOfDaysSample, numberOfTrainVectors, dateQ)

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

def getPredictionRate(company, profibility, kernel, numberOfDaysSample, numberOfTrainVectors, repeats, dateQ = None):
    prediction = predictCompany(company, profibility, kernel, numberOfDaysSample, numberOfTrainVectors, repeats, dateQ)
    print ("Prediction " + str(prediction) + "%")
    return prediction

def predictCompany(company_id, profibility, kernel, numberOfDaysSample, numberOfTrainVectors, repeats, dateQ):
    #Config
    #outputLength=1
    #numberOfTestVectors=1

    numberOfDaysSample = numberOfDaysSample + 1
    if dateQ is not None:
        data = DbGet().getHistoryWithQ(company_id, numberOfDaysSample + numberOfTrainVectors + repeats -1, dateQ);
    else:
        data = DbGet().getHistory(company_id, numberOfDaysSample + numberOfTrainVectors + repeats -1);
    if data == False or len(data) < numberOfDaysSample + numberOfTrainVectors + repeats - 1:
        print ("Not enough length: "+str(numberOfDaysSample + numberOfTrainVectors + repeats - 1))
        return -1

    data = [s[0] for s in reversed(data) if s[0]] #Transform tuples to int array
    development and print ("data=" + str(data))

    prof_perc = []
    prof_perc_with_alg = 1

    if profibility is True:
        for k in reversed(range(1,len(data))):
            data[k] = data[k]/data[k-1]

        data[0] = 1
        prof_perc = copy(data)
        # print "data2=" + str(data);

    for l in reversed(range(1,len(data))):
        if data[l] > data[l-1]:
            data[l] = 1
        else:
            data[l] = -1

    data[0] = 1

    development and print ("prof_perc=" + str(prof_perc))
    development and print ("data=" + str(data))

    #Give format to Y and X in chunks
    X = []
    Y = []
    for j in range(0, len(data) - numberOfDaysSample + 1):
        chunk = data[j : j+numberOfDaysSample]
        X.append(chunk[:-1])
        Y.append(chunk[-1])

    #Iterate to get average result
    predictions=[]
    probas=[]
    number_of_ones=[]
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

        # print ("x=" + str(x))
        # print ("y=" + str(y))

        pr = testPrediction(x, y, kernel)
        predictions.append(pr["result"])
        probas.append(pr["proba"][0][1])
        number_of_ones.append(pr["number_of_ones"])

        if(pr["perc_with_alg"]):
            prof_perc_with_alg = prof_perc_with_alg * prof_perc[i+1]

        development and print ("prof_perc_with_alg=" + str(prof_perc_with_alg))
        development and print ("prof_perc=" + str(prof_perc[i+1]))

    return {"rate": np.average(predictions), "proba": np.average(probas), "prof_perc": np.average(prof_perc), "prof_perc_with_alg": prof_perc_with_alg, "number_of_ones": np.average(number_of_ones),}

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
            x_reshape = x_test.reshape(1, -1)
            predictionModel = SVC(kernel=kernel, probability=True).fit(x_train, y_train)
            predictions = predictionModel.predict(x_reshape)
            proba = predictionModel.predict_proba(x_reshape)
        except ValueError:
            return {"result": np.asarray([True]), "proba": {0: {0: -1}} } #All are the same

        development and print ("x_train=" + str(x_train))
        development and print ("y_train=" + str(y_train))
        development and print ("x_test=" + str(x_test))
        development and print ("y_test=" + str(y_test))
        development and print ("x_test_1=" + str(x_test_1))
        development and print ("predictions=" + str(predictions))

        expected = y_test > x_test_1
        predicted = predictions > x_test_1
        ###print (expected == predicted)

        number_of_ones = sum(X > 0)/len(X)

        perc_with_alg = False
        if(predictions[0]>0):
            perc_with_alg = True

        return {"result": (expected == predicted), "proba": proba , "perc_with_alg": perc_with_alg, "number_of_ones": number_of_ones}
