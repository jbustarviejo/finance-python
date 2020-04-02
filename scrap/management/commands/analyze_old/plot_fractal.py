import os
import numpy as np
import operator
import nolds
import matplotlib
import matplotlib.pyplot as plt; plt.rcdefaults()
from pylab import *

from sklearn.svm import SVR
from scrap.models import Analisys, Company

from django.utils import timezone
from django.db import transaction
from django.db.models import Q, Count, Avg
from django.core.management.base import BaseCommand

from config.settings import local as settings

class Command(BaseCommand):
    help = "Analize company SVM data from FT.com. analize_fractal"
    debug = False

    @transaction.non_atomic_requests
    def handle(self, *args, **kwargs):
        nbars=6
        bars = np.arange(0.5, 1.01, 1/(nbars*2))
        barLabels = []
        Y=[]
        for i in range(len(bars)-1):
            Y.append(Analisys.objects.filter(Q(rate__gt=bars[i]) & Q(rate__lte=bars[i+1]) & Q(fractal_points__gte=0)).aggregate(Avg('fractal_points'))['fractal_points__avg'] or 0 )
            barLabels.append(str(round(bars[i],2))+'-'+str(round(bars[i+1],2)))
        y_pos=np.arange(len(bars)-1)
        plt.bar(y_pos, Y, align='center', alpha=0.5)
        plt.xticks(y_pos, barLabels)
        plt.xlabel('Rate')
        plt.ylabel('Avg(fractal points)')
        print('bars', bars)
        print('Y', Y)
        plt.show()
