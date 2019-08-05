import datetime
import enum
from multiprocessing import Pool

from bs4 import BeautifulSoup

from Helper import DBStorage
from Helper import httpWeb


class FinanceData:
    privateKey = ""
    code = ""
    name = ""
    priceList = ""
    isBadPublic = False
    tradeList = ""
    category = ""
    kind = ""
    dateTime = ""
    timeList = ""

    def __init__(self, privateKey, code, name, price, isBadPublic, trade, category, kind, dateTime, time):
        self.privateKey = privateKey
        self.code = code
        self.name = name
        self.priceList = price
        self.isBadPublic = isBadPublic
        self.tradeList = trade
        self.category = category
        self.kind = kind
        self.dateTime = dateTime
        self.timeList = time


class DaumFinacingCrawling:
    _CommonUrl = "https://www.sedaily.com/Stock/Quote"
    _BaseUrl = "https://www.sedaily.com/Stock/"
    _urls = {}
    _codeNames = []

    _actions = []

    class Category(enum.Enum):
       Kospi = 0
       Kosdaq =1

    class CallDelegate:

        callback = None
        price = 0
        title = ""
        code = ""
        category = None
        kind = ""

        def __init__(self, callback, category = None, title = "", code = "",  price = 0,  kind = ""):
            self.price = price
            self.category = category
            self.title = title
            self.code = code
            self.kind = kind
            self.callback =callback

        def __call__(self, data):
            self.callback(data,self.category, self.title, self.code, self.price, self.kind)


    def __init__(self):
        self._urls[self.Category.Kospi] = self._CommonUrl + "?type=1"
        self._urls[self.Category.Kosdaq] = self._CommonUrl + "?type=2"

    def execute(self):
        for name in self.Category:
            _httpWeb = httpWeb.HttpWeb(self._urls[name], lambda x: self.on_success(x, name),
                                       lambda x: self.on_failed(x, name))
            _httpWeb.execute()

        pool = Pool(processes=4)
        pool.map(self._poolExecute, self._actions)

    def _poolExecute(self, action):
        action()

    def on_success(self, data, category):
        print("success %s" % category)
        soup = BeautifulSoup(data, "html.parser")

        financeCategory = soup.find_all("div", {"class", "table"})
        #financeNodes = soup.find_all("table", {"class", "gTable clr"})


        for financeCategoryNode in financeCategory:
            titleNode =  financeCategoryNode.find_all("dl", {"class", "thead"})
            kindValue = titleNode[0].find("a")
            kind = kindValue.text

            stockNodes = financeCategoryNode.find_all("dl", {"class", "tbody"})
            for stockNode in stockNodes:
                title = stockNode.find("dt").find("a").text
                infoNode = stockNode.find("dd")
                code = infoNode["id"].split('_')[2]
                price = infoNode.find_all("span")[0].text
                link = self._BaseUrl + code
                self.SetDB(category, title, code, price, kind)
                #self._actions.append(
                #   httpWeb.HttpWeb(link, self.CallDelegate(self.on_success_item, category, title, code, price, kind),
                #                    self.CallDelegate(self.on_failed_item, title, code, category, price, kind)).execute)



    ''' 
        i = 0
        for financeNode in financeNodes:

            kind = financeCategory[i].text.split('|')[0]
            trs = financeNode.find_all("tr")
            i = i + 1

            for j in range(0, len(trs)):
                if j == 0:
                    continue

                tr = trs[j]

                tds = tr.find_all("td")
                if len(tds) < 3:
                    continue

                for k in range(0, len(tds), 3):
                    if tds[k].find("a") is None:
                        continue

                    name = tds[k].find("a").text
                    if name in self._codeNames:
                        continue
                    else:
                        self._codeNames.append(name)

                    link = self._baseUrl + tds[k].find("a")["href"]
                    price = tds[k + 1].text.replace(",", "")

                    #print("%s %s %s" % (name, link, price))

                    self._actions.append( httpWeb.HttpWeb(link,  self.CallDelegate(self.on_success_item, category, price, kind), self.CallDelegate(self.on_failed_item, category, price, kind)).execute)

                    #httpWeb.HttpWeb(link,  self.CallDelegate(self.on_success_item, category, price, kind), self.CallDelegate(self.on_failed_item, category, price, kind)).execute()
    '''

    def on_failed(self, data, category, price = 0, kind = ""):
        print("failed %s" % category)

    def SetDB(self, category, title, code, price, kind):
        dateStr = datetime.datetime.now().strftime("%Y-%m-%d")
        timeStr = datetime.datetime.now().strftime("%H:%M:%S")
        privateKey = code + "_" + dateStr

        dataObj = FinanceData(privateKey, code, title, price, 0, 0, category.name, kind, dateStr, timeStr)

        isContain =  DBStorage.DBStorage.instance().IsContainByParam(dataObj, "privateKey", privateKey)
        if isContain:
            priceList = DBStorage.DBStorage.instance().GetTableData(dataObj, "privateKey", privateKey, "priceList")
            priceList = priceList + "," + price
            DBStorage.DBStorage.instance().UpdateTableData(dataObj, "privateKey", privateKey, "priceList", priceList)

            tradeList = DBStorage.DBStorage.instance().GetTableData(dataObj, "privateKey", privateKey, "tradeList")
            tradeList = tradeList + "," + trade
            DBStorage.DBStorage.instance().UpdateTableData(dataObj, "privateKey", privateKey, "tradeList", tradeList)

            timeList = DBStorage.DBStorage.instance().GetTableData(dataObj, "privateKey", privateKey, "timeList")
            timeList = timeList + "," + timeStr
            DBStorage.DBStorage.instance().UpdateTableData(dataObj, "privateKey", privateKey, "timeList", timeList)

        else:
            DBStorage.DBStorage.instance().Insert(dataObj)

    def on_success_item(self, data, category, title, code, price, kind):
        #print("successItem %s" % category)

        soup = BeautifulSoup(data, "html.parser")

        '''
        #itemNode = soup.find("div", {"class", "topInfo"})
        itemNode = soup.find("div", id = "topWrap")

        name = itemNode.find("h2").text
        code = itemNode.find("span", {"class", "stockCode"}).text
        trade = itemNode.find("span", {"class", "num_trade"}).text.replace(",", "")

        isBadPublic = 0
        
        
        

        if itemNode.find("a", {"class", "badPublic"}) is not None:
            isBadPublic = 1
        '''

        itemNode = soup.find("div", {"class", "text_chart_top"})
        trade = itemNode.find("dl").find("dd").text
        isBadPublic = 0


        dateStr = datetime.datetime.now().strftime("%Y-%m-%d")
        timeStr = datetime.datetime.now().strftime("%H:%M:%S")
        privateKey = code + "_" + dateStr

        dataObj = FinanceData(privateKey, code, title, price, isBadPublic, trade, category.name, kind, dateStr, timeStr)

        isContain =  DBStorage.DBStorage.instance().IsContainByParam(dataObj, "privateKey", privateKey)
        if isContain:
            priceList = DBStorage.DBStorage.instance().GetTableData(dataObj, "privateKey", privateKey, "priceList")
            priceList = priceList + "," + price
            DBStorage.DBStorage.instance().UpdateTableData(dataObj, "privateKey", privateKey, "priceList", priceList)

            tradeList = DBStorage.DBStorage.instance().GetTableData(dataObj, "privateKey", privateKey, "tradeList")
            tradeList = tradeList + "," + trade
            DBStorage.DBStorage.instance().UpdateTableData(dataObj, "privateKey", privateKey, "tradeList", tradeList)

            timeList = DBStorage.DBStorage.instance().GetTableData(dataObj, "privateKey", privateKey, "timeList")
            timeList = timeList + "," + timeStr
            DBStorage.DBStorage.instance().UpdateTableData(dataObj, "privateKey", privateKey, "timeList", timeList)

        else:
            DBStorage.DBStorage.instance().Insert(dataObj)

        print("%s %s %s %s %s" % (title, code, price, trade, isBadPublic))



    def on_failed_item(self, data, category, title, code, price, kind):
        print("failedItem %s" % category)