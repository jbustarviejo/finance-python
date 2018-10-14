from analysis.CompanyAnalysisSVR import *
from analysis.CompanyAnalysisSVC import *
from analysis.CompanyAnalysisSVM import *
import numpy as np
from database.dbGet import *
from database.dbInsert import *
import Settings
import os

class Analize:

    #Analyzes companies list array in database
    def analizeSVRAndSVCCompanies(self, currency = None):
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
            if currency is True:
                company = DbGet().getCompanyToOptPendingSVM();
                recover = True
            else:
                company = DbGet().getCompanyToOptSVM(currency);
                recover = False

            # optParamsSVR(company, recover)
            # optParamsSVRR(company, recover)
            # optParamsSVC(company, recover)
            optParamsSVCR(company, recover)
            # if currency is True:
            #     exit();

    #Analyzes companies list array in database
    def analizeSVRAndSVCCompaniesWithQ(self, currency = None):
        imTheFather = True
        children = []

        for i in range(Settings.numberOfAnalizeThreads): #Run multiple threads
            child = os.fork()
            if child:
                children.append(child)
            else:
                imTheFather = False
                self.analizeSVRAndSVCCompaniesProcessWithQ(currency)
                os._exit(0)
                break

        #Father must wait to all children before continue
        for childP in children:
            os.waitpid(childP, 0)

    def analizeSVRAndSVCCompaniesProcessWithQ(self, currency):
        while(True):
            if currency is True:
                company = DbGet().getCompanyToOptPendingSVMWithQ();
                recover = True
            else:
                company = DbGet().getCompanyToOptSVMWithQ(currency);
                recover = False

            # optParamsSVR(company, recover)
            # optParamsSVRR(company, recover)
            # optParamsSVC(company, recover)
            optParamsSVCRWithQ(company, recover)
            # if currency is True:
            #     exit();

    #Analyzes companies list array in database
    def analizeSVCCompanies(self, year, min_month, max_month):
        imTheFather = True
        children = []

        for i in range(Settings.numberOfAnalizeThreads): #Run multiple threads
            child = os.fork()
            if child:
                children.append(child)
            else:
                imTheFather = False
                self.analizeSVCCompaniesProcess(year, min_month, max_month)
                os._exit(0)
                break

        #Father must wait to all children before continue
        for childP in children:
            os.waitpid(childP, 0)

    def analizeSVCCompaniesProcess(self, year, min_month, max_month):
        while(True):
            company = DbGet().getCompanyToOptSVCWithMaxAndMin(year, min_month, max_month);

            if company == False:
                print("No more companies left")
                exit()

            optParamsSVCR2(company[0], company[1], year, min_month, max_month)

    #Analyzes companies list array in database
    def analizeSVMCompanies(self):
        imTheFather = True
        children = []

        for i in range(Settings.numberOfAnalizeThreads): #Run multiple threads
            child = os.fork()
            if child:
                children.append(child)
            else:
                imTheFather = False
                self.analizeSVMCompaniesProcess()
                os._exit(0)
                break

        #Father must wait to all children before continue
        for childP in children:
            os.waitpid(childP, 0)

    def analizeSVMCompaniesProcess(self):
        while(True):
            company = DbGet().getCompanyToOptSVM();

            if company == False:
                print("No more companies left")
                exit()

            optParamsSVM(company[0], withR=False, svc=False)
            optParamsSVM(company[0], withR=True, svc=False)
            optParamsSVM(company[0], withR=True, svc=True)
