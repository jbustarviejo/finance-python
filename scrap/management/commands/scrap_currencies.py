import requests
from lxml import html

from django.core.management.base import BaseCommand

from scrap.models import Currency

class Command(BaseCommand):
    help = "Scrap currencies list from FT.com"

    def handle(self, *args, **kwargs):
        #Get currencies array
        page = requests.get('https://markets.ft.com/data/currencies')
        tree = html.fromstring(page.content)

        currencies = tree.xpath("//select[@class='o-forms__select mod-ui-form__select--event']/option")

        currencyList = []
        for curr in currencies:
            currency = str(curr.text)

            if "(" not in currency: continue
            symbolStart = currency.index("(")
            symbolEnd = currency.index(")")
            currency_name= currency[0:(symbolStart-1)]
            currency_symbol = currency[(symbolStart+1):symbolEnd]

            currencyList.append(curr)
            currency_model, created = Currency.objects.get_or_create(symbol=currency_symbol)
            currency_model.symbol = currency_symbol
            currency_model.name = currency_name

            currency_model.save()

        print("Finished! 🏁")
