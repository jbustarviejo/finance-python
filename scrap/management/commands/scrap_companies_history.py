import os
import json
import requests
import datetime
from lxml import html

from django.utils import timezone
from django.db.models import Q, Count
from django.db import transaction
from django.core.management.base import BaseCommand

from config.settings import local as settings
from scrap.models import Company

class Command(BaseCommand):
    help = "Scrap companies history data from FT.com"

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
                    if(self.scrapCompaniesHistory()):
                        os._exit(0)
                        break

        #Father must wait to all children before continue
        for childP in children:
            os.waitpid(childP, 0)
            print("Finished! 🏁")

    #Get companies list array
    @transaction.non_atomic_requests
    def scrapCompaniesHistory(self):
        time_threshold = timezone.now() - timezone.timedelta(hours=24)
        company = Company.objects.filter(Q(history_updated_at__isnull=True) | Q(history_updated_at__lt=time_threshold) ).order_by('?').first()
        if not company:
            return True

        print("->Scrapping history from: %s" % (company.name),)
        try:
            page = requests.get(
                company.history_scraping_link(),
                data=json.dumps(company.history_payload()),
                headers=company.history_headers()
            )
            parsedJson=json.loads(page.content)

            company.history_updated_at=timezone.now()

            if(not parsedJson or not parsedJson["Elements"] or not parsedJson["Elements"][0]["ComponentSeries"][0]["Values"]):
                company.history = []
                company.save()
                return False

            history = []

            dates = parsedJson["Dates"]
            currency = parsedJson["Elements"][0]["Currency"]

            openPrice = parsedJson["Elements"][0]["ComponentSeries"][0]["Values"]
            highPrice = parsedJson["Elements"][0]["ComponentSeries"][1]["Values"]
            lowPrice = parsedJson["Elements"][0]["ComponentSeries"][2]["Values"]
            closePrice = parsedJson["Elements"][0]["ComponentSeries"][3]["Values"]

            volume = parsedJson["Elements"][1]["ComponentSeries"][0]["Values"]

            for i in range(len(dates)):
                historyValues = {}

                historyValues["date"] = datetime.datetime.strptime(dates[i], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d')

                historyValues["open"] = openPrice[i]
                historyValues["high"] = highPrice[i]
                historyValues["low"] = lowPrice[i]
                historyValues["close"] = closePrice[i]

                historyValues["volume"] = volume[i]
                history.append(historyValues)

            company.history = history
            company.currency = currency
            company.save()

            print("Scraped history from %s" % (company.name))

        except:
            print('------------------ERROR--------------------')
            raise
            exit()
