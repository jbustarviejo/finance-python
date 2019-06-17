from django.contrib import admin
from django.contrib.auth.models import Group, User
admin.site.unregister(Group)
admin.site.unregister(User)

from .sector_admin import SectorAdmin
from .industry_admin import IndustryAdmin
from .company_admin import CompanyAdmin
from .currency_admin import CurrencyAdmin
from .analisys_admin import AnalisysAdmin
