import os
import json
import requests
import datetime
from lxml import html

from django.utils import timezone
from django.db.models import Q, Count
from django.db import transaction
from django.core.management.base import BaseCommand

from config import settings
from scrap.models import Currency

class Command(BaseCommand):
    help = "Scrap currencies history data from FT.com"

    @transaction.non_atomic_requests
    def handle(self, *args, **kwargs):
        while(True):
            if(self.scrapCurrencyHistory()):
                break

        print("Finished! 🏁")

    #Get companies list array
    @transaction.non_atomic_requests
    def scrapCurrencyHistory(self):
        time_threshold = timezone.now() - timezone.timedelta(hours=24)
        currency = Currency.objects.filter(Q(history_updated_at__isnull=True) | Q(history_updated_at__lt=time_threshold) ).order_by('?').first()
        if not currency:
            return True
            
        print("->Scrapping currency history from: %s" % (currency.name),)
        currency.xid_to_usd and self.scrapCurrencyHistoryByXid(currency, currency.xid_to_usd)
        currency.xid_from_usd and self.scrapCurrencyHistoryByXid(currency, currency.xid_from_usd)

    #Get companies list array
    @transaction.non_atomic_requests
    def scrapCurrencyHistoryByXid(self, currency, xid):
        try:
            page = requests.get(
                currency.history_scraping_link(),
                data=json.dumps(currency.history_payload(xid)),
                headers=currency.history_headers()
            )
            parsedJson=json.loads(page.content)

            currency.history_updated_at=timezone.now()

            if(not parsedJson or not parsedJson["Elements"] or not parsedJson["Elements"][0]["ComponentSeries"][0]["Values"]):
                currency.history = []
                currency.save()
                return False

            history = []

            dates = parsedJson["Dates"]

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

            if currency.xid_to_usd == xid:
                currency.history_to_usd = history
            else:
                currency.history_from_usd = history

            currency.history_updated_at=timezone.now()
            currency.save()

            print("Scraped currency history from %s" % (currency.name))

        except:
            print('------------------ERROR--------------------')
            raise
            exit()
