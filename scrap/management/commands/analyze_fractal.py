import os
import numpy as np
import operator
import nolds
import matplotlib
import matplotlib.pyplot as plt
from pylab import *

from sklearn.svm import SVR
from scrap.models import Analisys, Company

from django.utils import timezone
from django.db import transaction
from django.db.models import Q
from django.core.management.base import BaseCommand

from config.settings import local as settings

class Command(BaseCommand):
    help = "Analize company SVM data from FT.com. analize_fractal"
    debug=True

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

        self.analysis(company)

        # company.analysis_updated_at = timezone.now()
        # company.save()
        exit()

    def analysis(self, company):
        # Get history
        history=company.getHistoryOpen(50)
        # print("history", history)

        # Initialize variables
        len_history = len(history)
        self.debug and print("len_history", len_history)

        if len_history == 0:
            print('Company without enough history:', len_history)
            return

        epmin=1e6
        epmax=-1
        epsilonl=[]
        Crl = []

        DIMS = np.arange(3, 12, 1)

        for dim in DIMS:
            self.debug and print("DIM",dim)

            matrix = np.array([history[0:dim]])
            for i in np.arange(1, len_history-dim+1, 1):
                matrix = np.append(matrix, [history[i:i+dim]], axis=0)

            dists = np.zeros((matrix.shape[0]-1, matrix.shape[0]-1))
            # Calculate distances matrix, get dmax and d min
            for i in range(0,matrix.shape[0]-1):
                for j in range(0,i+1):
                    dists[i][j] = np.linalg.norm(matrix[i+1]-matrix[j])

            self.debug and print("dists",dists)

            dmin = np.log10(np.min(dists[dists>0]))
            dmax = np.log10(np.max(dists))*3
            delta = (dmax-dmin)/50
            # delta = (dmax-dmin)/50 #UNCOMENT
            # epsilon = np.arange(dmin, dmax+delta/10, delta) #UNCOMENT
            Cd = []

            if len(epsilonl) ==0: #DLELTE
                epsilonl.append( np.arange(dmin, dmax+delta/10, delta) ) #DLELTE

            epsilon = epsilonl[0] #DELETE

            for d in epsilon:
                Cd = np.append(Cd,np.sum(dists<=pow(10,d)) - np.sum(dists==0))

            self.debug and print("Cd_pew",Cd)
            Cd = Cd/(matrix.shape[0]*(matrix.shape[0]-1)/2)
            self.debug and print("Cd",Cd)
            Crl.append(np.log10(Cd))
            # epsilonl.append(epsilon) #UNCOMENT
            epmax=max(epmax,max(epsilon))
            epmin=min(epmin,min(epsilon))

        self.debug and print("Crl", Crl)

        subplot(3,1,1)
        for i in range(0, len(Crl)):
            plt.plot(np.asarray(epsilonl[0]), Crl[i])
            # plt.plot(np.asarray(epsilonl[i]), Crl[i])#UNCOMENT


        plt.ylabel('C(Epsilon)')
        plt.xlabel('Epsilon')
        # plt.xticks(epsilonl)
        subplot(3,1,2)
        self.debug and print("min",Crl[0], epsilonl[0])
        self.debug and print("max", Crl[len(Crl)-1],  epsilonl[0])
        infinites = sum(np.isinf(Crl[len(Crl)-1]))
        if (infinites>20):
            print("Number of inifites high, breaking by:", infinites)
            return
        self.debug and print("infinites", infinites)
        overture = Crl[0]-Crl[len(Crl)-1]
        plt.plot(np.asarray(epsilonl[0]), overture)
        plt.ylabel('Range')
        plt.xlabel('Epsilon')

        subplot(3,1,3)
        overture_diff = np.diff(overture)
        epsilon_diff = np.asarray(epsilonl[0][1:len(epsilonl[0])])
        plt.plot(epsilon_diff, overture_diff)
        plt.ylabel('Range diff')
        plt.xlabel('Epsilon')

        self.debug and print("overture_diff: ", overture_diff)
        indexes=(overture_diff > -0.05) & (overture[1:len(epsilonl[0])] > 0.1)

        self.debug and print("indexes0: ", indexes)
        # Remove the first points and individual
        single_count=0
        for i in range(0, len(indexes)-1):
            if indexes[i]:
                single_count += 1
            else:
                single_count = 0

            if i<10 or single_count <= 3:
                indexes[i] = False

        self.debug and print("indexes: ", indexes)
        self.debug and print("overture_diff[indexes]: ", overture_diff[indexes])
        self.debug and print("epsilon_diff[indexes]: ", epsilon_diff[indexes])
        plt.scatter(epsilon_diff[indexes], overture_diff[indexes], color='red')

        print("RESULT? ", sum(indexes)>0, sum(indexes))

        subplot(3,1,1)
        self.debug and print("Crl[i]: ", Crl[0])
        self.debug and print("epsilonl indexes: ", epsilonl[0][1:len(epsilonl[0])][indexes])
        plt.scatter(epsilonl[0][1:len(epsilonl[0])][indexes], Crl[0][1:len(epsilonl[0])][indexes], color='red')

        plt.show()
