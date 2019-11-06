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
    help = "Analize company SVM data from FT.com"
    debug = False

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
        company = Company.objects.filter(Q(analysis_updated_at__isnull=True) | Q(analysis_updated_at__lt=time_threshold) ).order_by('?').first()
        if not company:
            return True

        self.optParamsSVR(company)

        company.analysis_updated_at = timezone.now()
        company.save()

    def optParamsSVR(self, company):
        predictions = []
        repeats = settings.repeats
        kernel = "rbf"
        numberOfDaysSample = 1
        numberOfTrainVectors = 5

        print ("SVR - "+str(company)+" -  Kernel: "+kernel+", sample: "+str(numberOfDaysSample)+", train vectors="+str(numberOfTrainVectors)+", repeats= "+str(repeats))

        rate = self.getPredictionRate(company, kernel, numberOfDaysSample, numberOfTrainVectors, repeats)
        print ("Rate " + str(rate) + "%")
        if rate is None:
            rate = -1

        analisys, created = Analisys.objects.get_or_create(
            company=company,
            kernel=kernel,
            svm="SVRR",
            number_of_days_sample=numberOfDaysSample,
            number_of_train_vectors=numberOfTrainVectors
        )

        analisys.rate = rate
        analisys.save()

    def getPredictionRate(self, company, kernel, numberOfDaysSample, numberOfTrainVectors, repeats):
        numberOfDaysSample = numberOfDaysSample + 1

        data = company.getHistoryOpen(numberOfDaysSample + numberOfTrainVectors + repeats -1)
        self.debug and print("data= ", data)

        if data == False or len(data) < numberOfDaysSample + numberOfTrainVectors + repeats - 1:
            print ("Not enough length")
            return -1

         # profibility
        for k in reversed(range(1,len(data))):
            data[k] = data[k]/data[k-1]

        data[0] = 1

        self.debug and print("data prof= ", data)

        #Give format to Y and X in chunks
        X = []
        Y = []
        for j in range(0, len(data) - numberOfDaysSample + 1):
            chunk = data[j : j+numberOfDaysSample]
            X.append(chunk[:-1])
            Y.append(chunk[-1])

        self.debug and print("X0= ", X)
        self.debug and print("Y0= ", Y)

        #Iterate to get average result
        predictions=[]
        for i in range(0, repeats):
            finalPos = i+1-repeats
            if finalPos != 0:
                x = np.asarray(X[i:finalPos])
                y = np.asarray(Y[i:finalPos])
            else:
                x = np.asarray(X[i:])
                y = np.asarray(Y[i:])

            self.debug and print("x0= ", x)
            self.debug and print("y0= ", y)

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
                predictions = SVR(kernel=kernel).fit(x_train, y_train).predict(x_test.reshape(1, -1))
            except ValueError:
                self.debug and print("=>>>>>All are the same!!! ")
                return np.asarray([True]) #All are the same

            self.debug and print("x_train=", x_train)
            self.debug and print("y_train=", y_train)
            self.debug and print("x_test=", x_test)
            self.debug and print("y_test=", y_test)
            self.debug and print("x_test_1=", x_test_1)
            self.debug and print("predictions=", predictions)

            expected = y_test > x_test_1
            predicted = predictions > x_test_1
            self.debug and print("expected, ", y_test, ">", x_test_1, expected)
            self.debug and print("predicted, ", predictions, ">", x_test_1, predicted)
            self.debug and print("expected == predicted=", expected, predicted, expected == predicted)

            return expected == predicted
