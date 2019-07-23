import enum
import re
from multiprocessing import Pool

from bs4 import BeautifulSoup
from dateutil.parser import parse

from Helper import DBStorage
from Helper import httpWeb


class NewsData:
    Index = 0
    category = ""
    title = ""
    dateTime = ""
    article = ""

    def __init__(self, index = 0, category = "", title = "", time = "", article = ""):
        self.Index = index
        self.category = category
        self.title = title
        self.dateTime = time
        self.article = article



class DaumNewsCrawling:
    _CommonUrl = "https://media.daum.net/breakingnews"
    _urls = {}
    _actions = []
    _index = 0

    # _indexValue = None
    class Category(enum.Enum):
        Sports = 0
        Digital = 1
        Economic = 2
        Society = 3
        Politics = 4
        Foreign = 5
        Culture = 6
        Entertain = 7

    class CallDelegate:

        callback = None
        category = None
        index = 0


        def __init__(self, callback, category=None, index = 0):
            self.category = category
            self.callback = callback
            self.index = index

        def __call__(self, data):
            self.callback(data, self.category, self.index)


    def __init__(self, firstindex):
        self._index = firstindex
        # self._indexValue = Value('i', firstindex)
        self._urls[self.Category.Economic] = self._CommonUrl + "/economic"
        self._urls[self.Category.Society] = self._CommonUrl + "/society"
        self._urls[self.Category.Politics] = self._CommonUrl + "/politics"
        self._urls[self.Category.Foreign] = self._CommonUrl + "/foreign"
        self._urls[self.Category.Culture] = self._CommonUrl + "/culture"
        self._urls[self.Category.Entertain] = self._CommonUrl + "/entertain"
        self._urls[self.Category.Digital] = self._CommonUrl + "/digital"
        self._urls[self.Category.Sports] = self._CommonUrl + "/sports"


    def execute(self):
        for name in self.Category:
             _httpWeb = httpWeb.HttpWeb(self._urls[name], lambda x : self.on_success(x, name), lambda x : self.on_failed(x, name))
             _httpWeb.execute()


        pool = Pool(processes=4)
        pool.map(self._poolExecute, self._actions)

    def _poolExecute(self, action):
        action()

    def on_success(self, data, category):
        print("success %s" % category)

        soup = BeautifulSoup(data, "html.parser")
        newsNodes = soup.find("ul", {"class", "list_news2 list_allnews"}).find_all("strong", {"class", "tit_thumb"})

        for newsNode in newsNodes:
            info = newsNode.find("a")
            url = info["href"]

            # tl = threading.Thread(target = httpWeb.HttpWeb(url,  lambda x : self.on_success_article(x, category), lambda x : self.on_failed_article(x, category)).execute)
            # tl.daemon = True
            # tl.start()

            #httpWeb.HttpWeb(url, self.CallDelegate(self.on_success_article, category), self.CallDelegate(self.on_failed_article, category)).execute()

            self._actions.append(httpWeb.HttpWeb(url, self.CallDelegate(self.on_success_article, category, self._index), self.CallDelegate(self.on_failed_article, category)).execute)
            self._index += 1


    def on_failed(self, data, category):
        print("failed %s" % category)


    def on_success_article(self, data, category, index):
        print("success_article %s" % category.name)
        soup = BeautifulSoup(data, "html.parser")
        head = soup.find("div", {"class", "head_view"})

        title = head.find("h3").text

        infos = head.find_all("span", {"class", "txt_info"})

        if len(infos) > 1:
            date = infos[1].text
        else:
            date = infos[0].text
        hangul = re.compile("[ㄱ-ㅎ가-힣]")
        date = re.sub(hangul, "", date)

        datetypedate = parse(date)

        articleNodes = soup.find("div", {"class", "article_view"}).find("section").find_all("p")

        article = ""

        for articleNode in articleNodes:
            article = article + articleNode.text

        dateStr = datetypedate.strftime("%Y-%m-%d %H:%M:%S")

        newsData = NewsData(index, category.name, title, dateStr, article)

        if DBStorage.DBStorage.instance().IsContain(newsData):
            return

        DBStorage.DBStorage.instance().Insert(newsData)



       # print("%s %s %s" % (title, dateStr, article))


    def on_failed_article(self, data, category, index = 0):
        print("failed_article %s" % category)

    




