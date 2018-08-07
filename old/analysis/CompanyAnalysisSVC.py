from database.dbGet import *
from database.dbInsert import *

import numpy as np
import operator
from copy import copy as copy
from sklearn.svm import SVC
from functools import reduce

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

def optParamsSVCR2(company_id): #Opt SVC with profibility
    predictions = []
    repeats = 244 #244
    kernel = "rbf"
    numberOfDaysSample = 1
    numberOfTrainVectors = 350 #350

    development and print()
    print ("===> SVCR2 - "+str(company_id)+" -  Kernel: "+kernel+", sample: "+str(numberOfDaysSample)+", train vectors="+str(numberOfTrainVectors)+", repeats= "+str(repeats))

    data = DbGet().getHistory2(company_id, numberOfDaysSample + numberOfTrainVectors + repeats + 1);
    if data == False or len(data) < numberOfDaysSample + numberOfTrainVectors + repeats + 1:
        print ("Not enough length: "+str(numberOfDaysSample + numberOfTrainVectors + repeats + 1))
        return -1

    new_data = []
    profitability = []

    #Profitability
    for k in range(1,len(data)):
        r = data[k][0]/data[k-1][0]
        profitability.append( r )
        new_data.append( (r > 1) *1 )

    development and print("data="+str(data)+"\r")
    development and print("profitability="+str(profitability)+"\r")
    development and print("new_data="+str(new_data)+"\r")

    X = []
    Y = []
    for j in range(1, len(new_data)):
        X.append([new_data[j-1]])
        Y.append(new_data[j])

    development and print("X="+str(X)+"\r")
    development and print("Y="+str(Y)+"\r")

    predictions=[]
    predictions_ems=[]
    probas=[]
    number_of_ones=[]
    prof_perc_with_alg = 1
    prof_perc_with_ems = 1

    for i in range(0, repeats):
        development and print()
        print ("==> C"+str(company_id)+": SVCR2 "+str(i+1)+"/"+str(repeats)+". Kernel: "+str(kernel)+". Days: "+ str(numberOfDaysSample)+ ". TrainVectors: "+str(numberOfTrainVectors))
        finalPos = i+1-repeats+len(X)
        development and print("finalPos="+str(finalPos))
        if finalPos != 0:
            x = np.asarray(X[i:finalPos])
            y = np.asarray(Y[i:finalPos])
        else:
            x = np.asarray(X[i:])
            y = np.asarray(Y[i:])
        development and print("x="+str(x))
        development and print("y="+str(y))
        pr = testPrediction2(x, y, kernel)
        development and print(pr)
        predictions.append(pr["result"])
        predictions_ems.append(pr["result_ems"])
        probas.append(pr["proba"][0][1])
        number_of_ones.append(pr["number_of_ones"])

        development and print("\nPredictions = "+str(predictions))
        development and print("Predictions EMS = "+str(predictions_ems))
        development and print("Probas = "+str(probas))
        development and print("Number_of_ones = "+str(number_of_ones))

        if(pr["perc_with_alg"]):
            development and print("\n->Alg decided to invest! = "+str(profitability[finalPos]))
            prof_perc_with_alg = prof_perc_with_alg * profitability[finalPos]
            development and print("->New alg profitability = "+str(prof_perc_with_alg))
        if(pr["perc_with_ems"]):
            development and print("->Ems decided to invest! = "+str(pr["perc_with_ems"]))
            prof_perc_with_ems = prof_perc_with_ems * profitability[finalPos]
            development and print("->New ems profitability = "+str(prof_perc_with_ems))

    development and print("\n--Results--\n")
    development and print("predictions="+str(predictions)+"\r")
    development and print("avg predictions (rate)="+str(np.average(predictions))+"\r")
    development and print("predictions ems="+str(predictions_ems)+"\r")
    development and print("avg predictions ems (rate_ems)="+str(np.average(predictions_ems))+"\r")
    development and print("probas="+str(probas)+"\r")
    development and print("avg probas="+str(np.average(probas))+"\r")
    development and print("number_of_ones="+str(number_of_ones)+"\r")
    development and print("avg number_of_ones="+str(np.average(number_of_ones))+"\r")
    development and print("->Buy & Hold: prof_perc="+str(prod(profitability))+"\r")
    development and print("->Alg: prof_perc_with_alg="+str(prof_perc_with_alg)+"\r")
    development and print("->EMS: prof_perc_with_ems="+str(prof_perc_with_ems)+"\n")

    DbInsert().saveOptSVC(company_id, "svcr", kernel, np.average(predictions), np.average(probas), prod(profitability), prof_perc_with_alg, prof_perc_with_ems, np.average(predictions_ems), np.average(number_of_ones), numberOfDaysSample, numberOfTrainVectors)

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

#Productorio
def prod(iterable):
    return reduce(operator.mul, iterable, 1)

def getPredictionRate(company, profibility, kernel, numberOfDaysSample, numberOfTrainVectors, repeats, dateQ = None):
    prediction = predictCompany(company, profibility, kernel, numberOfDaysSample, numberOfTrainVectors, repeats, dateQ)
    print ("Prediction " + str(prediction) + "%")
    return prediction

def predictCompany(company_id, profibility, kernel, numberOfDaysSample, numberOfTrainVectors, repeats, dateQ):
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

def testPrediction2(X, Y, kernel):
    #Train
    x_train = np.asarray(X[:-1])
    y_train = np.asarray(Y[:-1])

    #Test
    x_test = np.asarray([X[-1]])
    y_test = np.asarray(Y[-1])

    development and print("x_train="+str(x_train)+"\r")
    development and print("x_test="+str(x_test)+"\r")
    development and print("y_train="+str(y_train)+"\r")
    development and print("y_test="+str(y_test)+"\r")

    import warnings
    warnings.filterwarnings('ignore')
    try:
        predictionModel = SVC(kernel=kernel, probability=True).fit(x_train, y_train)
        predictions = predictionModel.predict(x_test)
        proba = predictionModel.predict_proba(x_test)

        development and print("predicted="+str(predictions)+"\r")
    except ValueError:
        if(sum(x_train) == len(x_train) or sum(x_train) <= 1):
            return {"result": np.asarray([True]), "result_ems": x_test == y_test, "proba": {0: {1: -1}}, "perc_with_alg": sum(x_train[1])>1, "number_of_ones": sum(X > 0)/len(X), "perc_with_ems": x_test == 1 } #All are the same
        print((x_train))
        print("ERROR")
        raise

    predicted = predictions[0]

    number_of_ones = sum(X > 0)/len(X)

    perc_with_alg = False
    if(predicted>0):
        perc_with_alg = True

    return {"result": (y_test == predicted), "result_ems": x_test == y_test, "proba": proba , "perc_with_alg": perc_with_alg, "number_of_ones": number_of_ones, "perc_with_ems": x_test == 1}


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
