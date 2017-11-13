from analysis.CompanyAnalysisSVR import *
import numpy as np
from database.DbGet import *
from database.DbInsert import *
import Settings
import os

class Analize:

    #Save companies list array in database
    def analizeSVRCompanies(self):
        imTheFather = True
        children = []

        for i in range(Settings.numberOfAnalizeThreads): #Run multiple threads
            child = os.fork()
            if child:
                children.append(child)
            else:
                imTheFather = False
                self.analizeSVRAndSVRRCompaniesProcess()
                os._exit(0)
                break

        #Father must wait to all children before continue
        for childP in children:
            os.waitpid(childP, 0)


    def analizeSVRAndSVRRCompaniesProcess(self):
        while(True):
            company = DbGet().getCompanyToOptSVR();
            optParams = optParamsSVR(company)
            if not optParams or optParams is None or not optParams["min"] or not optParams["max"]:
                continue
            DbInsert().saveOptSVR(company[0], optParams["max"], optParams["min"])
            print "Company: "+str(company)+" M:"+str(optParams["max"])+"% m:"+str(optParams["min"])+"%"

            optParams = optParamsSVRR(company)
            if not optParams or optParams is None or not optParams["min"] or not optParams["max"]:
                continue
            DbInsert().saveOptSVRR(company[0], optParams["max"], optParams["min"])
            print "Company: "+str(company)+" M:"+str(optParams["max"])+"% m:"+str(optParams["min"])+"%"
