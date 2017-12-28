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
            company = [10088] #DbGet().getCompanyToOptSVR(currency);

            #SVR and SVRR
            optParams = optParamsSVR(company)
            if not optParams or optParams is None or not optParams["min"] or not optParams["max"]:
                continue
            DbInsert().saveOptSVR(company[0], optParams["max"], optParams["min"])
            print ("Company: "+str(company)+" M:"+str(optParams["max"])+"% m:"+str(optParams["min"])+"%")

            optParams = optParamsSVRR(company)
            if not optParams or optParams is None or not optParams["min"] or not optParams["max"]:
                continue
            DbInsert().saveOptSVRR(company[0], optParams["max"], optParams["min"])
            print ("Company: "+str(company)+" M:"+str(optParams["max"])+"% m:"+str(optParams["min"])+"%")

            #SVC and SVCR
            optParams = optParamsSVC(company)
            if not optParams or optParams is None or not optParams["min"] or not optParams["max"]:
                continue
            DbInsert().saveOptSVC(company[0], optParams["max"], optParams["min"])
            print ("Company: "+str(company)+" M:"+str(optParams["max"])+"% m:"+str(optParams["min"])+"%")

            optParams = optParamsSVCR(company)
            if not optParams or optParams is None or not optParams["min"] or not optParams["max"]:
                continue
            DbInsert().saveOptSVCR(company[0], optParams["max"], optParams["min"])
            print ("Company: "+str(company)+" M:"+str(optParams["max"])+"% m:"+str(optParams["min"])+"%")
