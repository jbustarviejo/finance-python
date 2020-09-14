import os
import numpy as np
import operator
import random
import math
import datetime

from sklearn.svm import SVR
from scrap.models import Analisys, Company, Sector, Industry

from django.utils import timezone
from django.db import transaction
from django.db.models import Q
from django.core.management.base import BaseCommand

from config.settings import local as settings

class Command(BaseCommand):
    help = "Analize the A matrix"
    debug = False
    initial_date='2019-01-01'
    # industries_num=19
    number_of_companies=20000000

    def handle(self, *args, **kwargs):
        for number_of_dates in [1]:
            print("\n\r\n\rNew number_of_dates "+str(number_of_dates)+"\n\r\n\r")
            self.createCSV(number_of_dates*365)

    def createCSV(self, number_of_dates):
        industries = Industry.objects.all() #[:self.industries_num]

        industriesLength=[]
        X=[]
        MAX=0
        for industry in industries:
            print("=========> New industry", industry)
            companies = Company.objects.raw("SELECT * FROM public.scrap_company WHERE currency='USD' AND JSONB_ARRAY_LENGTH(history)>1000 AND history->-1->>'date' >'"+self.initial_date+"' AND industry_id = %s LIMIT %s" % (industry.id, self.number_of_companies))
            # companies = Company.objects.raw("SELECT * FROM public.scrap_company WHERE currency='USD' AND JSONB_ARRAY_LENGTH(history)>1000 AND history->-1->>'date' >'"+self.initial_date+"' AND industry_id = %s LIMIT %s" % (industry.id, random.randint(3, 6)))
            industriesLength.append([industry.id,len(companies)])

            date = datetime.datetime.strptime(self.initial_date, '%Y-%m-%d')
            index = 0

            for t in range(number_of_dates):
                self.debug and print("---New date", date)
                for company in companies:
                    try:
                       X[index].append(company.getOpenAt(date.strftime('%Y-%m-%d')))
                    except IndexError:
                       X.append([company.getOpenAt(date.strftime('%Y-%m-%d'))])
                    self.debug and print("mira company at date", company, date, company.getOpenAt(date.strftime('%Y-%m-%d')))
                self.debug and print("---Actual", X)
                date = date - datetime.timedelta(days=1)

                index=index+1
            MAX=MAX+1
            if(MAX==2):
                break

        np.savetxt("X_"+str(number_of_dates)+"_blocks.csv", X, delimiter=",")
        np.savetxt("X_industries_len_"+str(number_of_dates)+".csv", industriesLength, delimiter=",")
        os.system('say "Finish '+str(number_of_dates)+' analysis"')
        return
    #
    # def getRandomADistance(self, X, industriesLength, reductionFactor):
    #     # industriesNewLength = [int(x / reductionFactor) for x in industriesLength]
    #     # self.debug and print("--- industriesNewLength", industriesNewLength)
    #
    #     distsX=[]
    #     for i in range(len(X)):
    #         for j in range(i+1, len(X)):
    #             distsX.append( np.linalg.norm(np.array(X[i])-np.array(X[j])) )
    #     self.debug and print('----Orig distances---', distsX)
    #
    #     # A=[]
    #     # offset=0
    #     # for i in range(len(industriesNewLength)):
    #     #     for j in range(industriesNewLength[i]):
    #     #         init_zeros = np.zeros(offset)
    #     #         final_zeros = np.zeros(len(X[0])-industriesLength[i]-offset)
    #     #         # randomElems = 0.1 * np.ones(industriesLength[i])
    #     #         # randomElems = np.random.randn(1, industriesLength[i])[0]
    #     #         randomElems = np.random.uniform(0.5, 1, industriesLength[i])
    #     #         randomMatrix = np.concatenate([init_zeros, randomElems, final_zeros])
    #     #         A.append(randomMatrix)
    #     #     offset+=industriesLength[i]
    #     #
    #     # A=np.transpose(A)
    #
    #     X=np.array(X)
    #     (N, M) = X.shape
    #     self.debug and print('Shape X!', N, M)
    #     A = np.random.randn(int(N/reductionFactor), M)
    #     A=np.transpose(A)
    #     self.debug and print('Shape A!', A.shape)
    #     self.debug and print('----Result----')
    #     self.debug and print('A',A)
    #     self.debug and print('X',X)
    #     Y=X.dot(A)
    #     self.debug and print('Y',Y)
    #
    #     distsY=[]
    #     for i in range(len(Y)):
    #         for j in range(i+1, len(Y)):
    #             # dists.append( str(i)+str(j) )
    #             distsY.append( np.linalg.norm(np.array(Y[i])-np.array(Y[j])) )
    #     self.debug and print('----Final distances---', distsY)
    #     dist = np.power( np.sum( np.power(np.array(distsX)-np.array(distsY),2) ), 1/2 )
    #     self.debug and print('----Final difference---', dist )
    #     return dist
    #
    # def handle(self, *args, **kwargs):
    #
    #     print("=>Start!")
    #     (X, industriesLength) = self.createXVector()
    #     print("X calculated")
    #
    #     allDist=[]
    #     for reductionFactor in [1, 2, 4]:
    #         min_dist = float("inf")
    #         for i in range(self.iterations):
    #             dist = self.getRandomADistance(X, industriesLength, reductionFactor)
    #             self.debug and print("New dist", i, reductionFactor, dist)
    #             if dist<min_dist:
    #                 min_dist=dist
    #
    #         allDist.append(min_dist)
    #         print("min dist:", reductionFactor, ":", min_dist)
    #         self.notification(reductionFactor)
    #
    #     print("allDist:", allDist)
    #     self.notification('WOLOLOLOOOO')
    #     return
