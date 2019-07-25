import os
import numpy as np
import operator
from sklearn.svm import SVR
from scrap.models import Analisys, Company

from django.utils import timezone
from django.db import transaction
from django.db.models import Q
from django.core.management.base import BaseCommand

from config.settings import local as settings

class Command(BaseCommand):
    help = "Analize company SVM data from FT.com. analize_company_SVM_poly"
    debug=False

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
        company = Company.objects.filter(Q(analysis_updated_at__isnull=True) | Q(analysis_updated_at__lt=time_threshold) ).order_by('?').first()
        if not company:
            return True

        self.optParamsSVM(company, "SVR")
        self.optParamsSVM(company, "SVRR")
        self.optParamsSVM(company, "SVRC")

        company.analysis_updated_at = timezone.now()
        company.save()
        exit()

    def optParamsSVM(self, company, svmType):
        predictions = []
        numberOfTrainVectors = 1

        print("%s analisys of %s" % (svmType, company.name))

        kernel='poly'

        for degree in [2,3,4,5,7,10,15,20,30]:
            for numberOfDaysSample in [5, 19, 61, 122, 244]:
                self.debug and print(svmType + " - "+str(company)+" -  Kernel: "+kernel+" "+str(degree)+"º, sample: "+str(numberOfDaysSample)+", train vectors="+str(numberOfTrainVectors)+", repeats= "+str(settings.repeats))
                if svmType == "SVR" or svmType == "SVRC":
                    profibility = False
                elif svmType == "SVRR":
                    profibility = True

                rate = self.getPredictionRate(company, profibility, kernel, numberOfDaysSample, numberOfTrainVectors, degree, svmType)
                self.debug and print("Rate " + str(rate) + "%")
                if rate is None:
                    rate = -1

                analisys, created = Analisys.objects.get_or_create(
                    company=company,
                    svm=svmType,
                    degree=degree,
                    number_of_days_sample=numberOfDaysSample
                )

                analisys.rate = rate
                analisys.save()

    def getPredictionRate(self, company, profibility, kernel, numberOfDaysSample, numberOfTrainVectors, degree, svmType):
        numberOfDaysSample = numberOfDaysSample + 1

        data = company.getHistory(numberOfDaysSample + numberOfTrainVectors + settings.repeats -1)
        self.debug and print("Original data", data)

        if data == False or len(data) < numberOfDaysSample + numberOfTrainVectors + settings.repeats - 1:
            self.debug and print("Not enough length")
            return -1

        data = [s['open'] for s in data] #Transform tuples to number array
        self.debug and print("Untupled data", data)
        if profibility is True:
            for k in reversed(range(1,len(data))):
                data[k] = data[k]/data[k-1]

            data[0] = 1
            self.debug and print("Data prof ",data);

        # WARNING this is for SV*C* only
        if svmType=="SVRC":
            self.debug and print("SVRC!!", str(np.asarray(data)))
            for l in reversed(range(1,len(data))):
                if data[l] > data[l-1]:
                    data[l] = 1
                else:
                    data[l] = -1

            data[0] = 1

        if svmType=="SVRR":
            self.debug and print("SVRR!!", str(np.asarray(data)))
            for l in reversed(range(1,len(data))):
                if data[l-1] == 0:
                    data[l-1] = 0.00001
                data[l] = data[l]/data[l-1]

            data[0] = 1

        self.debug and print("Vector", str(np.asarray(data)))

        #Give format to Y and X in chunks
        X = []
        Y = []
        for j in range(0, len(data) - numberOfDaysSample + 1):
            chunk = data[j : j+numberOfDaysSample]
            X.append(chunk[:-1])
            Y.append(chunk[-1])

        self.debug and print("X0 ", str(np.asarray(X)))
        self.debug and print("Y0 ", str(np.asarray(Y)))

        #Iterate to get average result
        predictions=[]
        for i in range(0, settings.repeats):
            self.debug and print("C"+str(company)+": "+svmType+str(i)+"/"+str(settings.repeats)+". Kernel: "+str(kernel)+" "+str(degree)+"º. Days: "+ str(numberOfDaysSample-1)+ ". TrainVectors: "+str(numberOfTrainVectors))
            finalPos = i+1-settings.repeats
            if finalPos != 0:
                x = np.asarray(X[i:finalPos])
                y = np.asarray(Y[i:finalPos])
            else:
                x = np.asarray(X[i:])
                y = np.asarray(Y[i:])

            self.debug and print("x=", x)
            self.debug and print("y=", y)

            predictions.append(self.testPrediction(x, y, kernel, degree, svmType))

        return np.average(predictions)

    def testPrediction(self, X, Y, kernel, degree, svmType):
            #Train
            x_train = np.asarray(X[:-1])
            y_train = np.asarray(Y[:-1])

            #Test
            x_test = np.asarray(X[-1])
            y_test = np.asarray(Y[-1])

            x_test_1 = x_test[-1]

            # import warnings
            # warnings.filterwarnings('ignore')
            try:
                predictions = SVR(kernel=kernel, degree=degree, gamma='scale').fit(x_train, y_train).predict(x_test.reshape(1, -1))[0]
                #HIPERWARNING, [0] destroys the array prediction!
            except ValueError:
                return np.asarray([True]) #All are the same

            self.debug and print("x_train=", x_train)
            self.debug and print("y_train=", y_train)
            self.debug and print("x_test=", x_test)
            self.debug and print("x_test_1=", x_test_1)
            self.debug and print("y_test=", y_test, " (", y_test-x_test_1,")")
            self.debug and print("predictions=", predictions, " (", predictions-x_test_1,")")

            #TODO: svmType!!

            if svmType=="SVRC":
                expected = y_test == x_test_1
                predicted = predictions == x_test_1
            else:
                expected = y_test > x_test_1
                predicted = predictions > x_test_1

            self.debug and print("expected (%s) == predicted (%s)?" % (expected, predicted), expected == predicted)

            return expected == predicted
