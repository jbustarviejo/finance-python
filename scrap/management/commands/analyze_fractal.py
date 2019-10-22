import os
import numpy as np
import operator
import nolds
from sklearn.svm import SVR
from scrap.models import Analisys, Company

from django.utils import timezone
from django.db import transaction
from django.db.models import Q
from django.core.management.base import BaseCommand

from config.settings import local as settings

class Command(BaseCommand):
    help = "Analize company SVM data from FT.com. analize_fractal"
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

        self.analysis(company)

        # company.analysis_updated_at = timezone.now()
        # company.save()
        exit()

    def analysis(self, company):
        # Get history
        history=company.getHistoryOpen(4)

        # Initialize variables
        len_history = len(history)
        dists = [[0 for x in range(len_history)] for y in range(len_history-1)]
        dmin=None
        dmax=None

        # Calculate distances matrix, get dmax and d min
        for i in range(0,len_history-1):
            for j in range(i,len_history):
                dists[i][j] = abs(history[i]-history[j])
                if (dmin is None or dists[i][j] < dmin) and dists[i][j] > 0:
                    dmin = dists[i][j]
                if dmax is None or dists[i][j] > dmax:
                    dmax = dists[i][j]

        print('history: ', history)
        print('dmin: ', dmin)
        print('dmax: ', dmax)
        print('dists: ', dists)

        delta = (dmax-dmin)/10
        print('delta: ', delta)

        c_r = []

        for d in np.arange(dmin, dmax, delta):
            print('->d', d)
            # print('Dists TF', (dists < d))
            print('Dists', (dists < d)*1)
            print('#Vectors', sum(sum((dists < d)*1)))
            c_r_i = sum(sum((dists < d)*1))
            c_r_i = c_r_i / (len_history * (len_history-1) )
            print('C(r,i)', c_r_i)
            c_r.append(c_r_i)

        print('C(r)', c_r)
