import DBStorage
import DaumNewsCrawling
import DaumFinacingCrawling
from multiprocessing import Pool
import time
from konlpy.tag import  Kkma
from konlpy.utils import pprint
from konlpy.tag import  Okt
from konlpy.tag import Mecab
from konlpy.tag import Hannanum
from konlpy.tag import Komoran

# newsData = DaumNewsCrawling.NewsData(133, "Sprots", "KIA 이범호 '안타'", "2018-10-09", "")
#
rowCnt = DBStorage.DBStorage.instance().Count(DaumNewsCrawling.NewsData.__name__)
# print(rowCnt)


#DBStorage.DBStorage.instance().Insert(newsData)

#daumNews = DaumNewsCrawling.DaumNewsCrawling(rowCnt)
#daumNews.execute()

#daumFinancing = DaumFinacingCrawling.DaumFinacingCrawling()
#daumFinancing.execute()


testArticle = DBStorage.DBStorage.instance().GetTableData(DaumNewsCrawling.NewsData(), "Index", 1165, "article");

kkma = Kkma()
print(kkma.nouns(testArticle))

okt = Okt()
print(okt.nouns((testArticle)))

mecab = Mecab()
print(mecab.nouns(testArticle))

hannanum = Hannanum()
print(hannanum.nouns(testArticle))

komoran = Komoran()
print(komoran.nouns(testArticle))

# class TestMPProcess:
#
#     _max = 0
#     _onSucess = None
#     def __init__(self, n, onsucess):
#         self._max = n
#         self._onSucess = onsucess
#
#     def execute(self):
#         result = self.testProcess(self._max, lambda x:self.testCallBack(x, 10))
#         self._onSucess(result)
#
#     def testProcess(self, n, callback):
#
#         result = 0
#         for i in range(0,n) :
#             result = result + i
#
#         #print(result)
#         callback(n)
#         return result
#
#     def testCallBack(self, x, y):
#         return x + y
#
# class TestMP:
#
#     actions = []
#
#     def execute(self):
#         params = [100000, 2000000, 3000000, 4000000]
#
#         for i in params:
#             self.actions.append(TestMPProcess(i, self.onSuccess).execute)
#
#         self.Process()
#         self.multiProcess()
#
#     def Process(self):
#         print("normalProcess")
#         start_time = time.time()
#
#         for action in self.actions:
#             action()
#
#         print("----%s----" % (time.time() - start_time))
#
#
#     def multiProcess(self):
#         print("multiProcess")
#
#         start_time = time.time()
#
#
#         pool = Pool(processes=4)
#         pool.map(self.temp, self.actions)
#
#         print("----%s----" % (time.time() - start_time))
#
#     def temp(self, action):
#         action()
#
#     def onSuccess(self, result):
#         print(result)
#
#     def testProcess(self, n):
#
#         result = 0
#         for i in range(0,n) :
#             result = result + i
#
#         print(result)
#         return result
#
#
# mp = TestMP()
# mp.execute()



