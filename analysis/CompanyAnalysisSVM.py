from database.dbGet import *
from database.dbInsert import *

import numpy as np
import operator
from copy import copy as copy
from sklearn.svm import SVC
from sklearn.svm import SVR
from functools import reduce

development = False

def optParamsSVM(company_id, withR, svc): #Opt SVC with profibility
    predictions = []
    repeats = 244 #244
    if svc:
        method = "svc"
    else:
        method = "svr"
    if withR:
        method = method + "r"
    for kernel in ["linear", "sigmoid", "rbf"]:
        for numberOfDaysSample in [1, 5, 19, 61, 122, 244]:
            for numberOfTrainVectors in [1, 5, 19, 61, 122, 244]:

                development and print()
                print ("===> "+str(method)+" - "+str(company_id)+" -  Kernel: "+kernel+", sample: "+str(numberOfDaysSample)+", train vectors="+str(numberOfTrainVectors)+", repeats= "+str(repeats))
                if(DbGet().isThisCombinationCalculated(company_id, kernel, numberOfDaysSample, numberOfTrainVectors, method)):
                    print("Combination already calculated. Continue...")
                    continue
                data = DbGet().getHistory(company_id, numberOfDaysSample + numberOfTrainVectors + repeats + 1);
                if data is False or len(data) < numberOfDaysSample + numberOfTrainVectors + repeats + 1:
                    if data is False:
                        print("Not data in this period")
                    else:
                        print ("Not enough length. Wanted: "+str(numberOfDaysSample + numberOfTrainVectors + repeats + 1)+". Get: "+str(len(data)))
                    DbInsert().saveOptSVMResult(company_id, method, kernel, -1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1)
                    return -1

                new_data = []
                profitability = []

                #Profitability
                for k in range(1,len(data)):
                    r = data[k][0]/data[k-1][0]
                    profitability.append( r )
                    if method == "svc" or method == "svcr":
                        new_data.append( (r > 1) *1 )
                    elif withR:
                        new_data.append( r )
                    else:
                        new_data.append( data[k][0] *1 )

                development and print("data="+str(data)+"\r")
                development and print("profitability="+str(profitability)+"\r")
                development and print("new_data="+str(new_data)+"\r")

                #Give format to Y and X in chunks
                X = []
                Y = []
                for j in range(0, numberOfTrainVectors + repeats):
                    chunk = new_data[j : j+1+numberOfDaysSample]
                    X.append(chunk[:-1])
                    Y.append(chunk[-1])

                development and print("X="+str(X)+"\r")
                development and print("Y="+str(Y)+"\r")

                predictions=[]
                predictions_ems=[]
                probas=[]
                number_of_ones=[]
                prof_perc_with_alg = 1
                prof_perc_with_ems = 1
                prof_perc_b_and_h = 1

                prof_perc_worst = 1
                prof_perc_better = 1

                for i in range(0, repeats):
                    development and print()
                    print ("==> C"+str(company_id)+": "+str(method)+" "+str(i+1)+"/"+str(repeats)+". Kernel: "+str(kernel)+". Days: "+ str(numberOfDaysSample)+ ". TrainVectors: "+str(numberOfTrainVectors))
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
                    pr = testPredictionSVM(x, y, kernel, svc)
                    development and print(pr)
                    predictions.append(pr["result"])
                    predictions_ems.append(pr["result_ems"])
                    probas.append(pr["proba"][0][1])
                    number_of_ones.append(pr["number_of_ones"])

                    development and print("\nPredictions = "+str(predictions))
                    development and print("Predictions EMS = "+str(predictions_ems))
                    development and print("Probas = "+str(probas))
                    development and print("Number_of_ones = "+str(number_of_ones))

                    development and print("\n->Profitability this day = "+str(profitability[finalPos]))
                    if(pr["perc_with_alg"]):
                        development and print("\n->Alg decided to invest! = "+str(profitability[finalPos]))
                        prof_perc_with_alg = prof_perc_with_alg * profitability[finalPos]
                        development and print("->New alg profitability = "+str(prof_perc_with_alg))
                    if(pr["perc_with_ems"]):
                        development and print("->Ems decided to invest! = "+str(pr["perc_with_ems"]))
                        prof_perc_with_ems = prof_perc_with_ems * profitability[finalPos]
                        development and print("->New ems profitability = "+str(prof_perc_with_ems))
                    prof_perc_b_and_h = prof_perc_b_and_h * profitability[finalPos]
                    development and print("->New B&H profitability = "+str(prof_perc_b_and_h))

                    if(profitability[finalPos]>1):
                        prof_perc_better = prof_perc_better * profitability[finalPos]
                        development and print("->New better profitability = "+str(prof_perc_better))
                    else:
                        prof_perc_worst = prof_perc_worst * profitability[finalPos]
                        development and print("->New worst profitability = "+str(prof_perc_worst))
                predictions = [int(val) for val in predictions] #Boolean to int
                predictions_ems = [int(val) for val in predictions_ems] #Boolean to int

                development and print("\n--Results--\n")
                development and print("predictions="+str(predictions)+"\r")
                development and print("avg predictions (rate)="+str(np.average(predictions))+"\r")
                development and print("predictions ems="+str(predictions_ems)+"\r")
                development and print("avg predictions ems (rate_ems)="+str(np.average(predictions_ems))+"\r")
                development and print("probas="+str(probas)+"\r")
                development and print("avg probas="+str(np.average(probas))+"\r")
                development and print("number_of_ones="+str(number_of_ones)+"\r")
                development and print("avg number_of_ones="+str(np.average(number_of_ones))+"\r")
                development and print("->Buy & Hold: prof_perc="+str(prof_perc_b_and_h)+"\r")
                development and print("->Alg: prof_perc_with_alg="+str(prof_perc_with_alg)+"\r")
                development and print("->EMS: prof_perc_with_ems="+str(prof_perc_with_ems)+"\r")
                development and print("->Best: prof_perc_better="+str(prof_perc_better)+"\r")
                development and print("->Worst: prof_perc_worst="+str(prof_perc_worst)+"\n")

                DbInsert().saveOptSVMResult(company_id, method, kernel, np.average(predictions), np.average(probas), prof_perc_b_and_h, prof_perc_with_alg, prof_perc_with_ems, np.average(predictions_ems), np.average(number_of_ones), numberOfDaysSample, numberOfTrainVectors, prof_perc_better, prof_perc_worst)

def testPredictionSVM(X, Y, kernel, svc):
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
        if svc:
            predictionModel = SVC(kernel=kernel, probability=True).fit(x_train, y_train)
        else:
            predictionModel = SVR(kernel=kernel).fit(x_train, y_train)
        predictions = predictionModel.predict(x_test)
        if svc:
            proba = predictionModel.predict_proba(x_test)
        else:
            proba = {0: {1: 1}}

        development and print("predicted="+str(predictions)+"\r")
    except ValueError:
        if(sum(x_train[-1]) == len(x_train[-1]) or sum(x_train[-1]) <= 1 or sum(y_train) == len(y_train) or sum(y_train) <= 1):
            return {"result": np.asarray([True]), "result_ems": x_test[-1][-1] == y_test, "proba": {0: {1: 1}}, "perc_with_alg": sum(x_train[1])>1, "number_of_ones": sum(X > 0)/len(X), "perc_with_ems": x_test[-1][-1] == 1 } #All are the same
        print((x_train))
        print("ERROR")
        raise

    predicted = predictions[0]

    number_of_ones = sum(X > 0)/len(X)

    alg_invested = False
    ems_invested = False

    development and print("last x_test="+str(x_test[-1][-1])+"\r")

    if svc:
        if(predicted == 1):
            alg_invested = True
        if(x_test[-1][-1] == 1):
            ems_invested = True
            result_ems_is_right = (y_test == 1)
        else:
            result_ems_is_right = (y_test == 0)

        result_alg_is_right = (y_test == predicted)
    else:
        try:
            pre_last_elem=x_test[-1][-2]
        except IndexError:
            try:
                pre_last_elem=x_test[-2][-1]
            except IndexError:
                pre_last_elem=x_train[-1][-1]
        development and print("pre-last x_test="+str(pre_last_elem)+"\r")
        if(predicted > x_test[-1][-1]):
            alg_invested = True
        if(x_test[-1][-1] > pre_last_elem):
            ems_invested = True
        result_alg_is_right = ( alg_invested == (x_test[-1][-1] < y_test) )
        result_ems_is_right = ( ems_invested == (x_test[-1][-1] < y_test) )

    return {"result": (result_alg_is_right), "result_ems": result_ems_is_right, "proba": proba , "perc_with_alg": alg_invested, "number_of_ones": number_of_ones, "perc_with_ems": ems_invested}
