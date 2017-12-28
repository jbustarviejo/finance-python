from database.dbGet import *
import numpy as np
import operator
from sklearn.svm import SVC

def optParamsSVC(companies):
    predictions = []
    for kernel in ["linear", "rbf", "sigmoid"]:
        for numberOfDaysSample in [122, 244, 488]:
            for numberOfTrainVectors in [122, 244, 488]:
                for repeats in [244]:
                    print ("SVC - "+str(companies)+" -  Kernel: "+kernel+", sample: "+str(numberOfDaysSample)+", train vectors="+str(numberOfTrainVectors)+", repeats= "+str(repeats))
                    prediction = {}
                    rate = getPredictionRate(companies, False, kernel, numberOfDaysSample, numberOfTrainVectors, repeats);
                    if rate is None:
                        continue
                    prediction["rate"] = rate
                    prediction["kernel"] = kernel;
                    prediction["numberOfDaysSample"] = numberOfDaysSample;
                    prediction["numberOfTrainVectors"] = numberOfTrainVectors;
                    prediction["repeats"] = repeats;
                    predictions.append(prediction);
    #print predictions
    #Get the maximun and minimun value
    if not predictions or len(predictions) <1:
        return None
    #Return result
    result = getMaxAndMin(predictions)
    return result

def optParamsSVCR(companies): #Opt SVC with profibility
    predictions = []
    for kernel in ["linear", "rbf", "sigmoid"]:
        for numberOfDaysSample in [122, 244, 488]:
            for numberOfTrainVectors in [122, 244, 488]:
                for repeats in [244]:
                    print ("SVCR - "+str(companies)+" -  Kernel: "+kernel+", sample: "+str(numberOfDaysSample)+", train vectors="+str(numberOfTrainVectors)+", repeats= "+str(repeats))
                    prediction = {}
                    rate = getPredictionRate(companies, True, kernel, numberOfDaysSample, numberOfTrainVectors, repeats);
                    if rate is None:
                        continue
                    prediction["rate"] = rate
                    prediction["kernel"] = kernel;
                    prediction["numberOfDaysSample"] = numberOfDaysSample;
                    prediction["numberOfTrainVectors"] = numberOfTrainVectors;
                    prediction["repeats"] = repeats;
                    predictions.append(prediction);
    #print predictions
    #Get the maximun and minimun value
    if not predictions or len(predictions) <1:
        return None
    #Return result
    result = getMaxAndMin(predictions)
    return result

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


def getPredictionRate(companies, profibility, kernel, numberOfDaysSample, numberOfTrainVectors, repeats):
    predictions = []
    if len(companies) == 1:
        prediction = predictCompany(companies[0], profibility, kernel, numberOfDaysSample, numberOfTrainVectors, repeats)
        print ("Prediction " + str(prediction) + "%")
        return prediction
    else:
        for i in range(0, len(companies)):
            prediction = predictCompany(companies[i][0], kernel)
            if prediction:
                predictions.append(prediction)
            if i>0 and i%10==0:
                print (str(i*100/len(companies)) + "%: prediction " + str(np.average(predictions)))

                return np.average(predictions)

def predictCompany(company_id, profibility, kernel, numberOfDaysSample, numberOfTrainVectors, repeats):
    #Config
    #outputLength=1
    #numberOfTestVectors=1

    data = DbGet().getHistory(company_id, numberOfDaysSample + numberOfTrainVectors + repeats -1);
    if data == False or len(data) < numberOfDaysSample + numberOfTrainVectors + repeats - 1:
        #print "Not enough length"
        return

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
        print ("company_id: "+str(i)+"/"+str(repeats))
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
        predictions = SVC(kernel=kernel).fit(x_train, y_train).predict(x_test)

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
