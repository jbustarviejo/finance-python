from django.contrib import admin
from django.contrib.auth.models import Group, User
admin.site.unregister(Group)
admin.site.unregister(User)

from .sector import SectorAdmin
from .industry import IndustryAdmin
