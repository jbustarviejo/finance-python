from lxml import html, etree
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
            if curr["symbol"] == "USD":
                return #ignore USD
            currencyList.append(curr)

        DbInsert().saveCurrencies(currencyList)

    #iterate over currencies xid
    def scrapCurrencyXid(self, toUSD):
        while(True):
            if toUSD:
                currency = DbGet().getCurrencyToScrapXidToUSD();
            else:
                currency = DbGet().getCurrencyToScrapXidFromUSD();
            #Return if not found
            if not currency:
                return

            symbol = currency[2]

            if toUSD:
                print "->Scrapping currency change xid " + symbol + "/USD:",
                link = Settings.crossRateUrl + "?s=" + currency[2] + "USD"
            else:
                print "->Scrapping currency change xid USD/"+symbol+":",
                link = Settings.crossRateUrl + "?s=USD" + currency[2]

            page = requests.get(link)
            tree = html.fromstring(page.content)

            matchingElement = tree.xpath("//section[@class='mod-tearsheet-add-to-watchlist']")

            if (not matchingElement or len(matchingElement)==0):
                print "-"
                if toUSD:
                    DbInsert().updateCurrencyXidToUSD(currency[0], 0)
                else:
                    DbInsert().updateCurrencyXidFromUSD(currency[0], 0)
                continue
            jsonScript = json.loads(matchingElement[0].attrib['data-mod-config'])

            xid = jsonScript["xid"]
            if (not xid):
                print "-"
                if toUSD:
                    DbInsert().updateCurrencyXidToUSD(currency[0], 0)
                else:
                    DbInsert().updateCurrencyXidFromUSD(currency[0], 0)
                continue

            print xid

            if toUSD:
                DbInsert().updateCurrencyXidToUSD(currency[0], xid)
            else:
                DbInsert().updateCurrencyXidFromUSD(currency[0], xid)
