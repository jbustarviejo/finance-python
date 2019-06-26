import os
import numpy as np
import operator
from sklearn.svm import SVC
from pyentrp import entropy

from django.utils import timezone
from django.db import transaction
from django.db.models import Q
from django.core.management.base import BaseCommand

from config import settings
from scrap.models import Analisys, Company

class Command(BaseCommand):
    help = "Scrap sectors data from FT.com"

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
                    if(self.analize_company_entropy()):
                        os._exit(0)
                        break

        #Father must wait to all children before continue
        for childP in children:
            os.waitpid(childP, 0)
            print("Finished! 🏁")

    #Get companies list array
    @transaction.non_atomic_requests
    def analize_company_entropy(self):
        company_analysis = Analisys.objects.filter(permutation_entropy__isnull=True).first()
        if not company_analysis:
            print("No company to analyze")
            return True
        data = company_analysis.getHistoryForEntropy()
        data = [s['open'] for s in data] #Transform tuples to number array

        # print("Processing entropy for company "+str(company_analysis.company))

        permutation_entropy = {
            'p2': entropy.permutation_entropy(data, 2),
            'p3': entropy.permutation_entropy(data, 3),
            'p4': entropy.permutation_entropy(data, 4),
            'p5': entropy.permutation_entropy(data, 5),
            'p6': entropy.permutation_entropy(data, 6),
            'p7': entropy.permutation_entropy(data, 7),
            'p8': entropy.permutation_entropy(data, 8),
            'p9': entropy.permutation_entropy(data, 9),
            'p10': entropy.permutation_entropy(data, 10),
            'p15': entropy.permutation_entropy(data, 15),
            'p30': entropy.permutation_entropy(data, 30),
            'p61': entropy.permutation_entropy(data, 61),
            'p122': entropy.permutation_entropy(data, 122),
            'p244': entropy.permutation_entropy(data, 244)
        }

        company_analysis.permutation_entropy = permutation_entropy
        company_analysis.save()
