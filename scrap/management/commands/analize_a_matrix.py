import os
import numpy as np
import operator
import random
import math

from sklearn.svm import SVR
from scrap.models import Analisys, Company, Sector, Industry

from django.utils import timezone
from django.db import transaction
from django.db.models import Q
from django.core.management.base import BaseCommand

from config.settings import local as settings

class Command(BaseCommand):
    help = "Analize the A matrix"
    debug = True

    def handle(self, *args, **kwargs):
        industry1 = Industry.objects.filter(slug='mobile-telecommunications').first()
        industry2 = Industry.objects.filter(slug='fixed-line-telecommunications').first()
        industry3 = Industry.objects.filter(slug='electricity').first()
        industry4 = Industry.objects.filter(slug='gas-water-and-multi-utilities').first()

        comps1 = industry1.companies.filter(~Q(history=[])).all()[:4]
        print('mobile-telecommunications', comps1)
        comps2 = industry2.companies.filter(~Q(history=[])).all()[:3]
        print('fixed-line-telecommunications', comps2)
        comps3 = industry3.companies.filter(~Q(history=[])).all()[:5]
        print('electricity', comps3)
        comps4 = industry4.companies.filter(~Q(history=[])).all()[:7]
        print('gas-water-and-multi-utilities', comps4)

        x1=[]
        for comp in comps1:
            x1.append(comp.getHistoryOpen(1)[0])
        x2=[]
        for comp in comps2:
            x2.append(comp.getHistoryOpen(1)[0])
        x3=[]
        for comp in comps3:
            x3.append(comp.getHistoryOpen(1)[0])
        x4=[]
        for comp in comps4:
            x4.append(comp.getHistoryOpen(1)[0])
        print('mobile-telecommunications', x1)
        print('fixed-line-telecommunications', x2)
        print('electricity', x3)
        print('gas-water-and-multi-utilities', x4)

        X=x1 +x2 + x3 + x4

        reductionFactor = 2

        c1l = math.ceil(len(comps1)/reductionFactor)
        c2l = math.ceil(len(comps2)/reductionFactor)
        c3l = math.ceil(len(comps3)/reductionFactor)
        c4l = math.ceil(len(comps4)/reductionFactor)

        A=[]
        X=np.array(x1+x2+x3+x4)
        offset=0

        for i in range(c1l):
            final_zeros = np.zeros(len(X)-len(comps1))
            randomElems = np.random.rand(1, len(comps1))[0]
            randomMatrix = np.concatenate([randomElems, final_zeros])
            A.append(randomMatrix)

        offset+=len(comps1)
        for i in range(c2l):
            init_zeros = np.zeros(offset)
            final_zeros = np.zeros(len(X)-len(comps2)-offset)
            randomElems = np.random.rand(1, len(comps2))[0]
            randomMatrix = np.concatenate([init_zeros, randomElems, final_zeros])
            A.append(randomMatrix)

        offset+=len(comps2)
        for i in range(c3l):
            init_zeros = np.zeros(offset)
            final_zeros = np.zeros(len(X)-len(comps3)-offset)
            randomElems = np.random.rand(1, len(comps3))[0]
            randomMatrix = np.concatenate([init_zeros, randomElems, final_zeros])
            A.append(randomMatrix)

        offset+=len(comps3)
        for i in range(c2l):
            init_zeros = np.zeros(offset)
            final_zeros = np.zeros(len(X)-len(comps4)-offset)
            randomElems = np.random.rand(1, len(comps4))[0]
            randomMatrix = np.concatenate([init_zeros, randomElems, final_zeros])
            A.append(randomMatrix)

        A=np.array(A)
        print('----Result----')
        print('A',A)
        print('X',X)
        print('Y',A.dot(X))
        return
