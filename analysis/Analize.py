from analysis.CompanyAnalysisSVR import *
from analysis.CompanyAnalysisSVC import *
import numpy as np
from database.dbGet import *
from database.dbInsert import *
import Settings
import os

class Analize:

    #Analyzes companies list array in database
    def analizeSVRAndSVCCompanies(self, currency):
        imTheFather = True
        children = []

        for i in range(Settings.numberOfAnalizeThreads): #Run multiple threads
            child = os.fork()
            if child:
                children.append(child)
            else:
                imTheFather = False
                self.analizeSVRAndSVCCompaniesProcess(currency)
                os._exit(0)
                break

        #Father must wait to all children before continue
        for childP in children:
            os.waitpid(childP, 0)


    def analizeSVRAndSVCCompaniesProcess(self, currency):
        while(True):
            company = DbGet().getCompanyToOptSVM(currency);

            optParamsSVR(company)

            optParamsSVRR(company)

            optParamsSVC(company)

            optParamsSVCR(company)
