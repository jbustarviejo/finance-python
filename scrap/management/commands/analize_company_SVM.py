import os
import numpy as np
import operator
from sklearn.svm import SVC
from scrap.models import Analisys, Company

from django.utils import timezone
from django.db import transaction
from django.db.models import Q
from django.core.management.base import BaseCommand

from config import settings

class Command(BaseCommand):
    help = "Analize company SVM data from FT.com"

    @transaction.non_atomic_requests
    def handle(self, *args, **kwargs):
        imTheFather = True
        children = []

        for i in range(settings.number_of_threads): #Run multiple threads
            child = os.fork()
            if child:
                children.append(child)
            else:
                imTheFather = False
                while(True):
                    if(self.analize_company()):
                        os._exit(0)
                        break

        #Father must wait to all children before continue
        for childP in children:
            os.waitpid(childP, 0)
            print("Finished! 🏁")

    #Get companies list array
    @transaction.non_atomic_requests
    def analize_company(self):
        time_threshold = timezone.now() - timezone.timedelta(hours=24)
        # company = Company.objects.get(id=31444)
        company = Company.objects.filter(Q(svm_updated_at__isnull=True) | Q(svm_updated_at__lt=time_threshold) ).order_by('?').first()
        if not company:
            return True

        self.optParamsSVC(company, "SVC")
        self.optParamsSVC(company, "SVCR")

        company.svm_updated_at = timezone.now()
        company.save()

    def optParamsSVC(self, company, svmType):
        predictions = []
        repeats = settings.repeats
        for kernel in ["linear", "sigmoid", "rbf"]:
            for numberOfDaysSample in [5, 19, 61, 122, 244]:
                for numberOfTrainVectors in [5, 19, 61, 122, 244]:
                    print (svmType + " - "+str(company)+" -  Kernel: "+kernel+", sample: "+str(numberOfDaysSample)+", train vectors="+str(numberOfTrainVectors)+", repeats= "+str(repeats))
                    if svmType == "SVC":
                        profibility = False
                    elif svmType == "SVCR":
                        profibility = True

                    rate = self.getPredictionRate(company, profibility, kernel, numberOfDaysSample, numberOfTrainVectors, repeats)
                    print ("Rate " + str(rate) + "%")
                    if rate is None:
                        rate = -1

                    analisys, created = Analisys.objects.get_or_create(
                        company=company,
                        kernel=kernel,
                        svm=svmType,
                        number_of_days_sample=numberOfDaysSample,
                        number_of_train_vectors=numberOfTrainVectors
                    )

                    analisys.rate = rate
                    analisys.save()

    def getPredictionRate(self, company, profibility, kernel, numberOfDaysSample, numberOfTrainVectors, repeats):
        numberOfDaysSample = numberOfDaysSample + 1

        data = company.getHistory(numberOfDaysSample + numberOfTrainVectors + repeats -1)

        if data == False or len(data) < numberOfDaysSample + numberOfTrainVectors + repeats - 1:
            print ("Not enough length")
            return -1

        data = [s['open'] for s in data] #Transform tuples to number array

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
            # print ("C"+str(company)+": "+profibilityString+str(i)+"/"+str(repeats)+". Kernel: "+str(kernel)+". Days: "+ str(numberOfDaysSample-1)+ ". TrainVectors: "+str(numberOfTrainVectors))
            finalPos = i+1-repeats
            if finalPos != 0:
                x = np.asarray(X[i:finalPos])
                y = np.asarray(Y[i:finalPos])
            else:
                x = np.asarray(X[i:])
                y = np.asarray(Y[i:])

            ###print "x=" + str(x)
            ###print "y=" + str(y)

            predictions.append(self.testPrediction(x, y, kernel))

        return np.average(predictions)

    def testPrediction(self, X, Y, kernel):
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
