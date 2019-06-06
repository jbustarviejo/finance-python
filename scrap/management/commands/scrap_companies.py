import os
import json
import requests
from lxml import html

from django.utils import timezone
from django.db.models import Q, Count
from django.db import transaction
from django.core.management.base import BaseCommand

from config import settings
from scrap.models import Industry, Company

class Command(BaseCommand):
    help = "Scrap companies data from FT.com"

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
                    if(self.scrapCompaniesList()):
                        os._exit(0)
                        break

        #Father must wait to all children before continue
        for childP in children:
            os.waitpid(childP, 0)
            print("Finished! 🏁")

    #Get companies list array
    @transaction.non_atomic_requests
    def scrapCompaniesList(self):
        time_threshold = timezone.now() - timezone.timedelta(hours=24)
        industry = Industry.objects.annotate(total_companies=Count('companies')).filter(Q(updated_at__isnull=True) | Q(updated_at__lt=time_threshold) | Q(total_companies__lte=0) ).order_by('?').first()
        if not industry:
            return True

        print("->Scrapping industry: %s" % (industry.name),)
        industry.updated_at=timezone.now()
        industry.save()

        self.scrapIndustry(industry)

        print("Scraped industry %s" % (industry.name))

    #iterate over industry
    def scrapIndustry(self, industry):
        startRow = 0
        while(True):
            print(".")
            companies_count = self.getPageContent(industry.companies_scraping_link + "&startRow=" + str(startRow), industry)
            if companies_count == 0:
                break;
            startRow += 100

    #Scrap industry link
    def getPageContent(self, link, industry):
        page = requests.get(link)
        parsedJson=json.loads(page.content);
        tree = html.fromstring(parsedJson["html"])

        companies_count = 0
        for matchingElement in tree.xpath("//a"):
            companyLink = matchingElement.attrib['href']
            company, created = Company.objects.get_or_create(
                name=matchingElement.text,
                symbol=companyLink[companyLink.index("?s=")+3:],
                link=companyLink,
                industry=industry
            )
            companies_count+=1
            company.save()
        return companies_count;
