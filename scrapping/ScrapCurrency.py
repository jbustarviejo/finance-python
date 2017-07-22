from lxml import html
import requests
from database.DbGet import *
import Settings
import json
import datetime
from database.DbInsert import *

class ScrapCurrency:
    """Scrap currency from companies from FT.com"""

    #Get currencies list array
    def scrapCurrencyList(self):
        page = requests.get(Settings.currencySymbolListUrl)
        tree = html.fromstring(page.content)

        select = tree.xpath("//select[@class='o-forms-select']")[0]
        currencies = select.xpath("//option/text()");
        # //currencies = currencies[1:len(currencies)]

        currencyList = []
        for currency in currencies:
            curr = {}

            if "(" not in currency: continue
            symbolStart = currency.index("(")
            symbolEnd = currency.index(")")
            curr["name"] = currency[0:(symbolStart-1)]
            curr["symbol"] = currency[(symbolStart+1):symbolEnd]

            currencyList.append(curr)

        DbInsert().saveCurrencies(currencyList)
