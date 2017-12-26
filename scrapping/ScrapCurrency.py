from lxml import html, etree
import requests
from database.dbGet import *
import Settings
import json
import datetime
from database.dbInsert import *

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
                print ("->Scrapping currency change xid " + symbol + "/USD:",)
                link = Settings.crossRateUrl + "?s=" + currency[2] + "USD"
            else:
                print ("->Scrapping currency change xid USD/"+symbol+":",)
                link = Settings.crossRateUrl + "?s=USD" + currency[2]

            page = requests.get(link)
            tree = html.fromstring(page.content)

            matchingElement = tree.xpath("//section[@class='mod-tearsheet-add-to-watchlist']")

            if (not matchingElement or len(matchingElement)==0):
                print ("-")
                if toUSD:
                    DbInsert().updateCurrencyXidToUSD(currency[0], 0)
                else:
                    DbInsert().updateCurrencyXidFromUSD(currency[0], 0)
                continue
            jsonScript = json.loads(matchingElement[0].attrib['data-mod-config'])

            xid = jsonScript["xid"]
            if (not xid):
                print ("-")
                if toUSD:
                    DbInsert().updateCurrencyXidToUSD(currency[0], 0)
                else:
                    DbInsert().updateCurrencyXidFromUSD(currency[0], 0)
                continue

            print (xid)

            if toUSD:
                DbInsert().updateCurrencyXidToUSD(currency[0], xid)
            else:
                DbInsert().updateCurrencyXidFromUSD(currency[0], xid)

    #Get companies list array
    def scrapCurrencyHistory(self):
        currency = DbGet().getCurrencyToScrap();

        #Return false if not found
        if not currency:
            return False

        currencyId = currency[0]
        currencyName = currency[1]

        print ("->Scrapping currency: " + currencyName,)

        currencyToUSD = True
        if (currency[3] == 0):
            currencyToUSD = False
            currencyXid = currency[4] #currencyXidFromUSD
            print ("from USD",)
        else:
            currencyXid = currency[3] #currencyXidToUSD
            print ("to USD",)

        payload = {"days":Settings.historyDaysToScrap,"dataNormalized":False,"dataPeriod":"Day","dataInterval":1,"endOffsetDays":0,"exchangeOffset":0,"realtime":False,"yFormat":"0.###","timeServiceFormat":"JSON","rulerIntradayStart":26,"rulerIntradayStop":3,"rulerInterdayStart":10957,"rulerInterdayStop":365,"returnDateType":"ISO8601","elements":[{"Label":"d475c065","Type":"price","Symbol":str(currencyXid),"OverlayIndicators":[],"Params":{}},{"Label":"079e5104","Type":"volume","Symbol":str(currencyXid),"OverlayIndicators":[],"Params":{}}]}

        headers = {"Content-Type": "application/json","Content-Length": "999999"}

        page = requests.post(Settings.currencyHistoryUrl, data=json.dumps(payload), headers=headers)
        parsedJson=json.loads(page.content);

        history = []

        if(parsedJson and parsedJson["Elements"] and parsedJson["Elements"][0]["ComponentSeries"][3]["Values"]):

            dates = parsedJson["Dates"]
            closePrice = parsedJson["Elements"][0]["ComponentSeries"][3]["Values"]

            for i in range(len(dates)):
              historyValues = {}

              historyValues["currency_id"] = currencyId
              historyValues["date"] = dates[i]

              if (currencyToUSD is True):
                  historyValues["price"] = closePrice[i]
              else:
                  historyValues["price"] = 1/closePrice[i]

              history.append(historyValues)
            print ("")
        else:
            print ("- No history")

        return history
