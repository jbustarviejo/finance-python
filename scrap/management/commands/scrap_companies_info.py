import os
import json
import requests
from lxml import html

from django.utils import timezone
from django.db.models import Q, Count
from django.db import transaction
from django.core.management.base import BaseCommand

from config.settings import local as settings
from scrap.models import Company

class Command(BaseCommand):
    help = "Scrap companies info (such xid) data from FT.com"

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
                    if(self.scrapCompaniesInfo()):
                        os._exit(0)
                        break

        #Father must wait to all children before continue
        for childP in children:
            os.waitpid(childP, 0)
            print("Finished! 🏁")

    #Get companies list array
    @transaction.non_atomic_requests
    def scrapCompaniesInfo(self):
        time_threshold = timezone.now() - timezone.timedelta(hours=24)
        company = Company.objects.filter(Q(updated_at__isnull=True) | Q(updated_at__lt=time_threshold) ).order_by('?').first()
        if not company:
            return True

        print("->Scrapping company: %s" % (company.name),)
        company.updated_at=timezone.now()
        company.save()

        self.scrapCompanyXidAndCurrency(company)

        print("Scraped company %s" % (company.name))

    #iterate over company
    @transaction.non_atomic_requests
    def scrapCompanyXidAndCurrency(self, company):
        page = requests.get(company.info_scraping_link)
        tree = html.fromstring(page.content)

        matchingElement = tree.xpath("//section[@class='mod-tearsheet-add-to-portfolio']")
        if (not matchingElement or len(matchingElement)==0):
            return False
        jsonScript = json.loads(matchingElement[0].attrib['data-mod-config'])

        xid = jsonScript["xid"]
        currency = jsonScript["currency"]
        if (not xid or not currency):
            return False

        company.xid = xid
        company.currency = currency

        company.save()
