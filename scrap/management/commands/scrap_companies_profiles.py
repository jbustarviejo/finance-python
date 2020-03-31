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
    help = "Scrap companies profiles (such about, web, etc.) data from FT.com"

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
        company = Company.objects.filter(Q(profile_updated_at__isnull=True) & Q(incorporated__isnull=True) ).order_by('?').first()
        if not company:
            return True

        print("->Scrapping company profile: %s" % (company.name),)
        self.scrapCompanyProfile(company)
        print("Scraped company profile %s" % (company.name))

    #iterate over company
    @transaction.non_atomic_requests
    def scrapCompanyProfile(self, company):
        page = requests.get(company.profile_scraping_link())
        tree = html.fromstring(page.content)

        description = tree.xpath("//p[@class='mod-tearsheet-profile-description mod-tearsheet-profile-section']")
        if description:
            description_text=description[0].text
            description_extra=description[0].findall("span/span")
            for description_extra_content in description_extra:
                description_text+=description_extra_content.text
            company.description = description_text

        location = tree.xpath("//address//span")
        if location:
            address = ''
            for line in location:
                address+=line.text+", "
            company.location = address[:-2]

        website = tree.xpath("//li[@class='mod-tearsheet-profile__info--stacked']//a[@class='mod-ui-link']/text()")
        if website and website[0]:
            company.website = website[0]

        extra_info = tree.xpath("//ul[@class='mod-tearsheet-profile-stats mod-tearsheet-profile-section mod-tearsheet-profile__extra__content']//li")
        if extra_info:
            revenue = extra_info[0].findall("span")
            if revenue:
                company.revenue = revenue[1].find("span").text

            net_income = extra_info[1].findall("span")
            if net_income:
                company.net_income = net_income[1].find("span").text

            incorporated = extra_info[2].findall("span")
            if incorporated:
                company.incorporated = incorporated[1].text

            employees = extra_info[3].findall("span")
            if employees:
                company.employees = employees[1].text

        company.profile_updated_at=timezone.now()
        company.save()
