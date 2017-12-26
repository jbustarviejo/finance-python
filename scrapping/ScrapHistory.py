from lxml import html
import requests
from database.dbGet import *
import Settings
import json
import datetime
from database.dbInsert import *

class ScrapHistory:
    """Scrap history from companies from FT.com"""

    #Get companies list array
    def scrapHistory(self, currency = None):
        company = DbGet().getCompanyToScrap(currency);
        #Return false if not found
        if not company:
            return False

        companyId = company[0]
        companyName = company[2]
        companySymbol = company[3]
        companyXid = company[4]
        companyCurrency = company[5]

        print ("->Scrapping company: " + companyName,)

        if (not companyXid or not companyCurrency):
            print ("(xid-curr)")
            xidLink = Settings.companyXidUrl + "?s=" + companySymbol
            companyXidAndCurrency = self.scrapCompanyXidAndCurrency(xidLink)
            DbInsert().updateCompanyXidAndCurrency(companyId, companyXidAndCurrency)
        else:
            print ("")

        if (not companyXid or companyXid==0): return True

        slug = companyName.replace("&","%26")

        return self.scrapHistoryValues(companyId, companyXid)

    #iterate over history
    def scrapCompanyXidAndCurrency(self, link):
        page = requests.get(link)
        tree = html.fromstring(page.content)

        industries = []
        matchingElement = tree.xpath("//section[@class='mod-tearsheet-add-to-portfolio']")
        if (not matchingElement or len(matchingElement)==0):
            return False
        jsonScript = json.loads(matchingElement[0].attrib['data-mod-config'])

        xid = jsonScript["xid"]
        currency = jsonScript["currency"]
        if (not xid or not currency):
            return False

        values = {}
        values["xid"] = xid
        values["currency"] = currency

        return values


    #iterate over history
    def scrapHistoryValues(self, companyId, companyXid):
        payload = {"days":Settings.historyDaysToScrap,"dataNormalized":False,"dataPeriod":"Day","dataInterval":1,"endOffsetDays":0,"exchangeOffset":0,"realtime":False,"yFormat":"0.###","timeServiceFormat":"JSON","rulerIntradayStart":26,"rulerIntradayStop":3,"rulerInterdayStart":10957,"rulerInterdayStop":365,"returnDateType":"ISO8601","elements":[{"Label":"d475c065","Type":"price","Symbol":str(companyXid),"OverlayIndicators":[],"Params":{}},{"Label":"079e5104","Type":"volume","Symbol":str(companyXid),"OverlayIndicators":[],"Params":{}}]}

        headers = {"Content-Type": "application/json","Content-Length": "999999"}

        page = requests.post(Settings.companyHistoryUrl, data=json.dumps(payload), headers=headers)
        parsedJson=json.loads(page.content);

        history = []

        if(parsedJson and parsedJson["Elements"] and parsedJson["Elements"][0]["ComponentSeries"][0]["Values"]):

          dates = parsedJson["Dates"]
          currency = parsedJson["Elements"][0]["Currency"]

          openPrice = parsedJson["Elements"][0]["ComponentSeries"][0]["Values"]
          highPrice = parsedJson["Elements"][0]["ComponentSeries"][1]["Values"]
          lowPrice = parsedJson["Elements"][0]["ComponentSeries"][2]["Values"]
          closePrice = parsedJson["Elements"][0]["ComponentSeries"][3]["Values"]

          volume = parsedJson["Elements"][1]["ComponentSeries"][0]["Values"]

          for i in range(len(dates)):
            historyValues = {}
            historyValues["company_id"] = companyId
            historyValues["currency"] = currency

            historyValues["date"] = dates[i]

            historyValues["open"] = openPrice[i]
            historyValues["high"] = highPrice[i]
            historyValues["low"] = lowPrice[i]
            historyValues["close"] = closePrice[i]

            historyValues["volume"] = volume[i]
            history.append(historyValues)

        return history
