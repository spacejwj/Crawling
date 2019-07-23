import pymysql


# db = pymysql.connect(host='127.0.0.1', port = 3306, user = 'jjwj', passwd = '1234', db = 'Crawling', charset = 'utf8')
# cursor = db.cursor()

class DBStorage:

    _instance = None

    _connection = None

    @classmethod
    def _getInstance(cls):
        return cls._instance

    @classmethod
    def instance(cls, *args, **kwargs):
        cls._instance = cls(*args, **kwargs)
        cls.instance = cls._getInstance
        return cls._instance

    def __init__(self):
        self._connection = pymysql.connect(host='127.0.0.1', port = 3306, user = 'jjwj', passwd = '1234', db = 'Crawling', charset = 'utf8')

    def _getDataName(self, data):
        return data.__class__.__name__

    def _getDataFieldName(self, data):
        return list(data.__dict__.keys())

    def _getDataFieldValue(self, data):
        return list(data.__dict__.values())

    def Count(self, tableName):
        sql = "SELECT COUNT(*) cnt from %s" % tableName
        cursor = self._executeSql(sql)
        return cursor.fetchone()[0]

    def Insert(self, data):
        sql = "INSERT INTO %s VALUES (%s)" % (self._getDataName(data), self._parse(data))
        print(sql)
        self._executeSql(sql)

    def IsContainKey(self, data):

        condition = "%s.%s = %d" % (self._getDataName(data), "Index", data.Index)
        sql = "SELECT COUNT(*) cnt FROM %s WHERE %s" % ( self._getDataName(data), condition)
        print(sql)
        cursor = self._executeSql(sql)
        return cursor.fetchone()[0] != 0

    def IsContain(self, data):

        if self.IsContainKey(data):
            return True;

        names = self._getDataFieldName(data)
        values = self._getDataFieldValue(data)

        condition = ""
        for i in range(1, len(names)):
            if i < len(names) -1 :
                condition = condition + " %s = \'%s\' AND " % (names[i], str(values[i]).replace("'", "\\'"))
            else:
                condition = condition + " %s = \'%s\'" % (names[i], str(values[i]).replace("'", "\\'"))

        sql = "SELECT COUNT(*) cnt FROM %s WHERE %s" % (self._getDataName(data), condition)
        #print(sql)
        cursor = self._executeSql(sql)
        return cursor.fetchone()[0] != 0

    def IsContainByParam(self, data, key, matchingValue):
        sql = "SELECT COUNT(*) cnt FROM %s WHERE %s.%s = \'%s\'" %(self._getDataName(data), self._getDataName(data), key, matchingValue)
        print(sql)
        cursor = self._executeSql(sql)
        return cursor.fetchone()[0] != 0

    def GetTableData(self, data, key, matchingValue, getKey):
        sql = "SELECT %s FROM %s WHERE %s.%s = \'%s\'" % (getKey, self._getDataName(data), self._getDataName(data), key, matchingValue)
        print(sql)
        cursor = self._executeSql(sql)
        return cursor.fetchone()[0]

    def UpdateTableData(self, data, key, matchingValue, updateKey, updateValue):
        sql = "UPDATE %s SET %s = \'%s\' WHERE %s = \'%s\'" %(self._getDataName(data), updateKey, str(updateValue).replace("'", "\\'"), key, str(matchingValue).replace("'", "\\'"))
        print(sql)
        self._executeSql(sql)

    def _executeSql(self, sql):
        try:
            self._connection.connect()
            cursor = self._connection.cursor()
            cursor.execute(sql)
            self._connection.commit()
        finally:
            self._connection.close()
        return cursor

    def _parse(self, data):
        values = self._getDataFieldValue(data)
        result = ""
        for i in range(0, len(values)):
            each = values[i]
            if i < len(values) -1 :
                result = result + "\'%s\'" % str(each).replace("'", "\\'") + ","
            else :
                result = result + "\'%s\'" % str(each).replace("'", "\\'")

        return result




# class A:
#     abc = ""
#     bc = 234
#
#     def __init__(self):
#         self.abc = "adasf"
#         self.bc = 324
#
#
# class B:
#     asfa = ""
#     gasd = 234
#
#     def __init__(self):
#         self.asfa = "adasf"
#         self.gasd = 324
#
#
# def insert(instant):
#     print(instant.__class__.__name__)
#     print(instant.__dict__.keys())
#
#
# instance = A()
#
# DBStorage.instance().Insert(instance)
#
# instance = B()
# insert(instance)
# for each in instance.__class__:
#     print(each)
