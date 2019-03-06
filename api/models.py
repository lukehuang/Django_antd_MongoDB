import mongoengine

# Create your models here.


class Account(mongoengine.Document):
    username = mongoengine.StringField(max_length=16)
    password = mongoengine.StringField(max_length=200)


class CurrentUserInfo(mongoengine.Document):
    avatar = mongoengine.StringField()
    name = mongoengine.StringField(max_length=16)
    notifyCount = mongoengine.IntField()
    userid = mongoengine.StringField(max_length=32)
    username = mongoengine.StringField()

class CurrentUser(mongoengine.Document):
    currentUserName = mongoengine.StringField()


class VisitData(mongoengine.Document):
    index = mongoengine.IntField()
    x = mongoengine.StringField()
    y = mongoengine.IntField()

class VisitData2(mongoengine.Document):
    index = mongoengine.IntField()
    x = mongoengine.StringField()
    y = mongoengine.IntField()

class SalesData(mongoengine.Document):
    index = mongoengine.IntField()
    x = mongoengine.IntField()
    y = mongoengine.IntField()

class SearchData(mongoengine.Document):
    index = mongoengine.IntField()
    keyword = mongoengine.StringField()
    count = mongoengine.IntField()
    rangeData = mongoengine.IntField()
    status = mongoengine.IntField()

class SalesTypeData(mongoengine.Document):
    index = mongoengine.IntField()
    x = mongoengine.StringField()
    y = mongoengine.IntField()

class SalesTypeDataOnline(mongoengine.Document):
    index = mongoengine.IntField()
    x = mongoengine.StringField()
    y = mongoengine.IntField()

class SalesTypeDataOffline(mongoengine.Document):
    index = mongoengine.IntField()
    x = mongoengine.StringField()
    y = mongoengine.IntField()

class OfflineData(mongoengine.Document):
    index = mongoengine.IntField()
    name = mongoengine.StringField()
    cvr = mongoengine.FloatField()

class OfflineChartData(mongoengine.Document):
    index = mongoengine.IntField()
    x  = mongoengine.IntField()
    y1 = mongoengine.IntField()
    y2 = mongoengine.IntField()

class OfflineChartDataList(mongoengine.Document):
    index = mongoengine.IntField()
    data = mongoengine.ListField()

class RadarData(mongoengine.Document):
    index = mongoengine.IntField()
    name  = mongoengine.StringField()
    label = mongoengine.StringField()
    value = mongoengine.IntField()