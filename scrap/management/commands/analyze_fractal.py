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
    debug = True

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
        if self.debug:
            company_analysis = Analisys.objects.get(company__id=2653)
            #6: 0.7049180327868853
            # {1: 0.5327868852459017, 2: 0.6639344262295082, 3: 0.6680327868852459, 4: 0.6434426229508197, 5: 0.6680327868852459, 6: 0.7049180327868853, 7: 0.6967213114754098, 8: 0.6926229508196722, 9: 0.7090163934426229, 10: 0.6885245901639344, 11: 0.6926229508196722, 12: 0.6844262295081968, 13: 0.6885245901639344, 14: 0.6885245901639344}

            # company_analysis = Analisys.objects.get(company__id=7492)
            #8: 0.7254098360655737
            # {1: 0.48360655737704916, 2: 0.7090163934426229, 3: 0.7336065573770492, 4: 0.7049180327868853, 5: 0.7049180327868853, 6: 0.7131147540983607, 7: 0.7131147540983607, 8: 0.7254098360655737, 9: 0.7090163934426229, 10: 0.7295081967213115, 11: 0.7131147540983607, 12: 0.7213114754098361, 13: 0.7131147540983607, 14: 0.7049180327868853}

            # company_analysis = Analisys.objects.get(company__id=28906)
            # 7: 0.7213114754098361
            # {1: 0.5204918032786885, 2: 0.7131147540983607, 3: 0.7049180327868853, 4: 0.7049180327868853, 5: 0.7131147540983607, 6: 0.7131147540983607, 7: 0.7213114754098361, 8: 0.7172131147540983, 9: 0.7172131147540983, 10: 0.7172131147540983, 11: 0.7090163934426229, 12: 0.7008196721311475, 13: 0.7131147540983607, 14: 0.7049180327868853}

            # company_analysis = Analisys.objects.get(company__id=25449)
            # 6: 0.7008196721311475
            # {1: 0.48770491803278687, 2: 0.6680327868852459, 3: 0.6639344262295082, 4: 0.6721311475409836, 5: 0.6844262295081968, 6: 0.7008196721311475, 7: 0.680327868852459, 8: 0.6967213114754098, 9: 0.6967213114754098, 10: 0.6844262295081968, 11: 0.6926229508196722, 12: 0.7131147540983607, 13: 0.7131147540983607, 14: 0.7172131147540983}

            # company_analysis = Analisys.objects.get(company__id=17305)
            # 5: 0.7581967213114754
            # {1: 0.5532786885245902, 2: 0.6680327868852459, 3: 0.6926229508196722, 4: 0.7459016393442623, 5: 0.7581967213114754, 6: 0.7336065573770492, 7: 0.7418032786885246, 8: 0.7213114754098361, 9: 0.7254098360655737, 10: 0.7213114754098361, 11: 0.7131147540983607, 12: 0.7049180327868853, 13: 0.7090163934426229, 14: 0.7172131147540983}


            # company_analysis = Analisys.objects.filter(Q(fractal_points__isnull=True) & Q(rate__gt=0) ).order_by('?').first()
        else:
            company_analysis = Analisys.objects.filter(Q(fractal_points__isnull=True) & Q(rate__gt=0) ).order_by('?').first()

        if not company_analysis:
            return True

        company_analysis.fractal_points = self.analysis(company_analysis.company)
        company_analysis.save()

    def analysis(self, company):
        # Get history
        data_length=252
        history=company.getHistoryOpen(data_length)
        # print("history", history)

        # Initialize variables
        len_history = len(history)
        print("Analysis of " + company.name + " (id: " + str(company.id) + ")")
        self.debug and print("len_history", len_history)

        if len_history == 0:
            print('Company without enough history:', len_history)
            return -1

        epmin=1e6
        epmax=-1
        epsilonl=[]
        Crl = []

        max_dim = 12
        min_dim = 3
        DIMS = np.arange(min_dim, max_dim, 1)
        index_dim_median = round(len(DIMS)/2)

        for dim in DIMS:
            print("-> DIM",dim)

            matrix = np.array([history[0:dim]])
            for i in np.arange(1, len_history-dim+1, 1):
                matrix = np.append(matrix, [history[i:i+dim]], axis=0)

            dists = np.zeros((matrix.shape[0]-1, matrix.shape[0]-1))
            # Calculate distances matrix, get dmax and d min
            for i in range(0,matrix.shape[0]-1):
                for j in range(0,i+1):
                    dists[i][j] = np.linalg.norm(matrix[i+1]-matrix[j])

            # self.debug and print("dists",dists)

            dmin = np.log10(np.min(dists[dists>0]))
            dmax = np.log10(np.max(dists))*3
            delta = (dmax-dmin)/50
            # epsilon = np.arange(dmin, dmax+delta/10, delta) #UNCOMENT
            Cd = []

            if len(epsilonl) ==0: #DLELTE
                epsilonl.append( np.arange(dmin, dmax+delta/10, delta) ) #DLELTE

            epsilon = epsilonl[0] #DELETE

            for d in epsilon:
                Cd = np.append(Cd,np.sum(dists<=pow(10,d)) - np.sum(dists==0))

            # self.debug and print("Cd_pew",Cd)
            Cd = Cd/(matrix.shape[0]*(matrix.shape[0]-1)/2)
            # self.debug and print("Cd",Cd)
            Crl.append(np.log10(Cd))
            # epsilonl.append(epsilon) #UNCOMENT
            epmax=max(epmax,max(epsilon))
            epmin=min(epmin,min(epsilon))

        self.debug and print("Crl", Crl)

        if self.debug:
            subplot(4,1,1)
        for i in range(0, len(Crl)):
            if self.debug:
                plt.plot(np.asarray(epsilonl[0]), Crl[i])
            # plt.plot(np.asarray(epsilonl[i]), Crl[i])#UNCOMENT


        if self.debug:
            plt.ylabel('log(C(Ɛ))')
            plt.xlabel('log(Ɛ)')
        # plt.xticks(epsilonl)
        if self.debug:
            subplot(4,1,2)
        self.debug and print("min",Crl[0], epsilonl[0])
        self.debug and print("max", Crl[len(Crl)-1],  epsilonl[0])
        infinites = sum(np.isinf(Crl[len(Crl)-1]))
        # UNCOMENT
        # if (infinites>20):
        #     print("Number of inifites high, breaking by:", infinites)
        #     return -2
        self.debug and print("infinites", infinites)
        overture = Crl[0]-Crl[len(Crl)-1]
        if self.debug:
            plt.plot(np.asarray(epsilonl[0]), overture)
            plt.ylabel('Amplitude')
            plt.xlabel('Ɛ')
            subplot(4,1,3)
        overture_diff = np.diff(overture)
        epsilon_diff = np.asarray(epsilonl[0][1:len(epsilonl[0])])
        if self.debug:
            plt.plot(epsilon_diff, overture_diff)
            plt.ylabel('δAmplitude')
            plt.xlabel('Ɛ')

        self.debug and print("overture_diff: ", overture_diff)
        self.debug and print("Crl[0]: ", Crl[0][1:len(Crl[0])])
        self.debug and print("Crl[0]<-0.5: ", Crl[0][1:len(Crl[0])]<-0.5)
        # indexes=(overture_diff > -0.2) & (overture[1:len(epsilonl[0])] > 0.5)
        indexes=(Crl[0][1:len(Crl[0])] < -0.5) & (overture_diff > -0.2)

        self.debug and print("indexes0: ", indexes)
        # Remove the first points and individual
        single_count=0
        for i in range(0, len(indexes)-1):
            if indexes[i]:
                single_count += 1
            else:
                single_count = 0

            # if i<10 or single_count <= 3:
            #     indexes[i] = False

        init_index=0
        end_index=0
        m_points=0
        if sum(indexes)>1:
            # We have enough data
            print("MIRA los indexes", indexes)
            for i in range(0, len(indexes)-1):
                if indexes[i] and not init_index:
                    init_index = i
                elif not indexes[i] and init_index and i > init_index+1:
                    end_index = i-1
                    break;

            if self.debug:
                print("init_index: ", init_index, ". end_index:", end_index)
                x1=epsilonl[0][1:len(epsilonl[0])][init_index]
                y1=Crl[index_dim_median][1:len(epsilonl[0])][init_index]
                x2=epsilonl[0][1:len(epsilonl[0])][end_index]
                y2=Crl[index_dim_median][1:len(epsilonl[0])][end_index]
                print("p1", x1, y1)
                print("p2", x2, y2)
                m_points=(y2-y1)/(x2-x1)
                print("==> m:", m_points)

        if self.debug:
            print("indexes: ", indexes)
            print("overture_diff[indexes]: ", overture_diff[indexes])
            print("epsilon_diff[indexes]: ", epsilon_diff[indexes])
            plt.scatter(epsilon_diff[indexes], overture_diff[indexes], color='red')

        print("RESULT? ", sum(indexes)>0, sum(indexes))

        for j in range(len(Crl)):
            slopes=[]
            for i in range(len(epsilonl[0])-2):
                x1=epsilonl[0][1:len(epsilonl[0])][i]
                y1=Crl[j][1:len(epsilonl[0])][i]
                x2=epsilonl[0][1:len(epsilonl[0])][i+1]
                y2=Crl[j][1:len(epsilonl[0])][i+1]
                print("p1", x1, y1)
                print("p2", x2, y2)
                slopes.append((y2-y1)/(x2-x1))
                print("==> m:", m_points)

            subplot(4,1,4)
            plt.plot(epsilonl[0][1:len(epsilonl[0])][1:len(epsilonl[0])-1], slopes)
            plt.ylabel('Slope')
            plt.xlabel('Ɛ')

        if self.debug:
            subplot(4,1,1)
        self.debug and print("Crl[i]: ", Crl[0])
        self.debug and print("epsilonl indexes: ", epsilonl[0][1:len(epsilonl[0])][indexes])
        if self.debug:
            plt.scatter(epsilonl[0][1:len(epsilonl[0])][indexes], Crl[index_dim_median][1:len(epsilonl[0])][indexes], color='red')

        if self.debug:
            subplot(4,1,1)
            plt.title('CiD: '+str(company.id)+' d_len='+str(data_length)+' m='+str(m_points))
            plt.show()
            exit()

        return sum(indexes)
