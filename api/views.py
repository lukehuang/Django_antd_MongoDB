from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import View
import json
import datetime
import random
import time
from werkzeug.security import check_password_hash,generate_password_hash
from .models import Account,CurrentUserInfo,VisitData,VisitData2,\
    SalesData,SearchData,SalesTypeData,SalesTypeDataOnline,SalesTypeDataOffline,\
    OfflineData,OfflineChartData,RadarData,CurrentUser,OfflineChartDataList

# Create your views here.


class Login(View):
    def post(self,request):
        print("--------------------login----------------------------")
        res_data = {
            "status":"error",
            "type":"account",
            "currentAuthority":"guest"
        }

        post_data = json.loads(request.body.decode("utf-8"))
        cookiesTest = request.COOKIES
        print(cookiesTest)
        modifyResult = CurrentUser.objects.modify(currentUserName = "")
        queryUsername = Account.objects.filter(username=post_data["userName"])
        if queryUsername:
            temp = queryUsername[0]

            # if (temp.password == post_data["password"]):
            if (check_password_hash(temp.password,post_data["password"])):
                res_data["status"] = 'ok'
                res_data["type"] = post_data["type"]
                res_data["currentAuthority"] = 'user'
                modifyResult = CurrentUser.objects.modify(currentUserName = post_data["userName"])
                print(modifyResult.currentUserName)
        data = json.dumps(res_data).encode()
        
        return HttpResponse(data)

class RegisterClass(View):
    def post(self,request):
        print("--------------------register------------------------------")
        res_data = {
            "status": "error",
            "currentAuthority": "guest",
        }
        post_data = json.loads(request.body.decode("utf-8"))
        queryUsername = Account.objects.filter(username=post_data["userName"])
        if not queryUsername:
            password = generate_password_hash(post_data["password"])
            registerResult = Account.objects.create(username = post_data["userName"],password = password)
            if registerResult:
                userCount = Account.objects.count()
                userInfo = CurrentUserInfo.objects.create(
                    avatar='https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png',
                    name = "UserName",
                    userid = str(userCount),
                    notifyCount=1,
                    username = post_data["userName"])
                if userInfo:
                    res_data["status"] = "ok"
                    res_data["currentAuthority"] = "user"
        data = json.dumps(res_data).encode()
        return HttpResponse(data)

class CurrentUserClass(View):
    def get(self,request):
        print("--------------------currentUser------------------------------")
        res_data ={
            'avatar'        : '',
            'name'          : '',
            'notifyCount'   : 0,
            'userid'        : "",
        }
        currentUserName = ''
        currentUserNameList = CurrentUser.objects.filter()
        if(currentUserNameList[0]):
            currentUserName = currentUserNameList[0].currentUserName
        try:
            queryUsername = Account.objects.filter(username=currentUserName)
            if queryUsername[0]:
                thisUser = CurrentUserInfo.objects.filter(username=queryUsername[0].username)
                if thisUser:
                    temp = thisUser[0]
                    res_data["avatar"] = temp.avatar
                    res_data["name"] = temp.name
                    res_data["notifyCount"] = temp.notifyCount
                    res_data["userid"] = temp.userid
            data = json.dumps(res_data).encode()
            return HttpResponse(data)
        except IndexError:
            print("===========IndexError=============")
            return HttpResponseRedirect('/user')


class FakeChartDataClass(View):
    def get(self,request):
        print("--------------------fakeChartData------------------------------")
        fakeData = self.getFakeChartData()
        data = json.dumps(fakeData).encode()
        return HttpResponse(data)


    def getVisitData(self):
        resultData = []
        for i in range(17):
            today = datetime.datetime.now()
            delta = datetime.timedelta(days=(16 - i))
            temp = today - delta
            date = temp.__format__('%Y-%m-%d')
            data = (int(random.random() * 10 + 5))
            tempData = VisitData.objects(index=i).modify(x=date, y=data)
            tempData.save()
            result = VisitData.objects.filter(index=i)
            resultData.append({
                "x": result[0].x,
                "y": result[0].y
            })
        return resultData

    def getVisitData2(self):
        resultData = []

        for i in range(7):
            today = datetime.datetime.now()
            delta = datetime.timedelta(days=(7 - i))
            temp = today - delta
            date = temp.__format__('%Y-%m-%d')
            data = (int(random.random() * 10 + 5))
            tempData = VisitData2.objects(index=i).modify(x=date, y=data)
            tempData.save()
            result = VisitData2.objects.filter(index=i)
            resultData.append({
                "x": result[0].x,
                "y": result[0].y,
            })
        return resultData

    def getSalesData(self):
        resultData = []
        for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
            temp = (int(random.random() * 1000) + 200)
            tempData = SalesData.objects(index=i).modify(x=i, y=temp)
            tempData.save()
            result = SalesData.objects.filter(index=i)
            resultData.append({
                "x": (str(result[0].x) + "月"),
                "y": result[0].y
            })
        return resultData

    def getSearchData(self):
        resultData = []
        for i in range(50):
            indexNum = i + 1
            keywordData = ('搜索关键词-' + str(indexNum))
            countData = (int(random.random() * 1000))
            rangeData = (int(random.random() * 100))
            statusData = (int(random.random() * 100) % 2)
            tempData = SearchData.objects(index=indexNum).modify(keyword=keywordData, count=countData, rangeData=rangeData,
                                                                 status=statusData)
            tempData.save()
            result = SearchData.objects.filter(index=indexNum)
            resultData.append({
                "index": result[0].index,
                "keyword": result[0].keyword,
                "count": result[0].count,
                "range": result[0].rangeData,
                "status": result[0].status
            })
        return resultData

    def getSalesTypeData(self,onlineData,offlineData):
        resultData = []
        salesTypeDataBase = SalesTypeData.objects.filter()
        rangNum = len(salesTypeDataBase)
        for i in range(rangNum):
            data = onlineData[i]["y"] + offlineData[i]["y"]
            tempData = SalesTypeData.objects(index=i).modify(y=data)
            tempData.save()
            result = SalesTypeData.objects.filter(index=i)
            resultData.append({
                "x": result[0].x,
                "y": result[0].y,
            })
        return resultData

    def getSalesTypeDataOnline(self):
        resultData = []
        salesTypeDataOnlineBase = SalesTypeDataOnline.objects.filter()
        rangNum = len(salesTypeDataOnlineBase)
        for i in range(rangNum):
            data = (int(random.random() * 5000))
            tempData = SalesTypeDataOnline.objects(index=i).modify(y=data)
            tempData.save()
            result = SalesTypeDataOnline.objects.filter(index=i)
            resultData.append({
                "x": result[0].x,
                "y": result[0].y,
            })
        return resultData

    def getSalesTypeDataOffline(self):
        resultData = []
        salesTypeDataOfflineBase = SalesTypeDataOffline.objects.filter()
        rangNum = len(salesTypeDataOfflineBase)
        for i in range(rangNum):
            data = (int(random.random() * 5000))
            tempData = SalesTypeDataOffline.objects(index=i).modify(y=data)
            tempData.save()
            result = SalesTypeDataOffline.objects.filter(index=i)
            resultData.append({
                "x": result[0].x,
                "y": result[0].y,
            })
        return resultData

    def getOfflineData(self,chartData):
        resultData = []
        for i in range(10):
            temp = chartData[i]
            y1Sum = 0
            y2Sum = 0
            for j in temp:
                y1Sum += j["y1"]
                y2Sum += j["y2"]

            cvrData = float('%.2f' % (y2Sum/y1Sum))
            nameData = ("门店" + str(i))
            tempData = OfflineData.objects(index=i).modify(name=nameData, cvr=cvrData)
            tempData.save()
            result = OfflineData.objects.filter(index=i)
            resultData.append({
                "index":i,
                "name": result[0].name,
                "cvr": result[0].cvr,
            })
        return resultData

    def getOfflineChartData(self):
        resultData = []
        for i in range(10):
            tempList = []
            for j in range(20):
                t = time.time()
                xData = (int(round(t * 1000)) - (1000 * 60 * 30 * (20 - j)))
                y1Data = (int(random.random() * 100) + 10)
                y2Data = (int(random.random() * y1Data) + 10)
                tempList.append({
                    'index': j,
                    'x' : xData,
                    'y1': y1Data,
                    'y2': y2Data,
                })
            tempData = OfflineChartDataList.objects(index=i).modify(data = tempList)
            tempData.save()
            result = OfflineChartDataList.objects.filter(index = i)
            if result:
                resultData.append(result[0].data)
        return resultData

    def getRadarData(self):
        radarTitleMap = {
            'ref': '引用',
            'koubei': '口碑',
            'output': '产量',
            'contribute': '贡献',
            'hot': '热度',
        }
        radarName = ['个人','团队','部门']
        radarData = []
        indexNum = 0
        for nameData in radarName:
            radarOriginalData = {}
            radarOriginalData["ref"] = (int(random.random() * 10 + 1))
            radarOriginalData["koubei"] = (int(random.random() * 10 + 1))
            radarOriginalData["output"] = (int(random.random() * 10 + 1))
            radarOriginalData["contribute"] = (int(random.random() * 10 + 1))
            radarOriginalData["hot"] = (int(random.random() * 10 + 1))

            for key in radarTitleMap:
                labelData = radarTitleMap[key]
                valueData = radarOriginalData[key]
                tempData = RadarData.objects(index = indexNum).modify(name = nameData,label = labelData,value =valueData )
                tempData.save()
                result = RadarData.objects.filter(index=indexNum)
                radarData.append({
                    "name"  : result[0].name,
                    "label" : result[0].label,
                    "value" : result[0].value,
                })
                indexNum += 1
            del(radarOriginalData)
        return radarData



    def getFakeChartData(self):

        visitData           =   self.getVisitData()
        visitData2          =   self.getVisitData2()
        salesData           =   self.getSalesData()
        searchData          =   self.getSearchData()
        salesTypeDataOnline =   self.getSalesTypeDataOnline()
        salesTypeDataOffline=   self.getSalesTypeDataOffline()
        salesTypeData       =   self.getSalesTypeData(salesTypeDataOnline,salesTypeDataOffline)
        offlineChartData    =   self.getOfflineChartData()
        offlineData         =   self.getOfflineData(offlineChartData)
        radarData           =   self.getRadarData()

        date =  {
            "visitData"             : visitData,
            "visitData2"            : visitData2,
            "salesData"             : salesData,
            "searchData"            : searchData,
            "offlineData"           : offlineData,
            "offlineChartData"      : offlineChartData,
            "salesTypeData"         : salesTypeData,
            "salesTypeDataOnline"   : salesTypeDataOnline,
            "salesTypeDataOffline"  : salesTypeDataOffline,
            "radarData"             : radarData,
        }
        return date


class TagsClass(View):
    def get(self,request):
        print("--------------------tags------------------------------")
        city = ["上海","北京","北京市","朝阳","朝阳区","海淀","元谋","南充","且末","荔波","佛山","庆阳","保山",
                "二连浩特","丽江","北京","锦州","塔城","大庆","西安","芷江","西宁","喀什","三亚","恩施","三女河",
                "连云港","长春","牡丹江","伊春","山海关","鸡西","昭通","达州","海淀","宜宾","运城","安阳","酒泉",
                "通辽","济宁","重庆","延吉","黑河","无锡","榆林","九江","兴城","乌海","邢台","阿克苏","厦门","晋江",
                "黎平","昆明","深圳","宁波","文山","临沂","伊宁","大理","揭阳","邯郸","南阳","大同","腾冲","银川",
                "呼和浩特","合肥","乌兰浩特","襄樊","柳州","南宁","长海","蓬莱","缨芬河","满洲里","成都","安顺","珠海",
                "库尔勒","通化","兴宁","长沙","依兰","西双版纳","温州","万县","延安","上海","安康","潍坊","广汉",
                "武汉","佳木斯","博尔塔拉","长治","湛江","哈尔滨","思茅","富蕴","鞍山","兴义","鄂尔多斯","天津",
                "常德","杭州","朝阳","拉萨","长白山","烟台","福州","梁平","泸州","芒市","临沧","安庆","保安营",
                "济南","蚌埠","石家庄","南昌","张家界","吉林","吉安","海拉尔","遵义","朝阳区","铜仁","南通","广州",
                "太原","阜阳","齐齐哈尔","大连","景德镇","徐州","贵阳","苏州","东营","常州","丹东","梧州","永州",
                "衢州","黄山","惠州","新源","阿尔山","百色","兰州","荆州","梅州","和田","扬州","海口","林芝","青岛",
                "哈密","库车","洛阳","嘉峪关","沈阳","绵阳","克拉玛依","玉树","西昌","汉中","赣州","威海","迪庆",
                "盐城","武夷山","阿勒泰","乌鲁木齐","庐山","秦皇岛","格尔木","衡阳","桂林","义乌","连城","井冈山",
                "宜昌","昌都","赤峰","九寨沟","锡林浩特","黄岩","敦煌","南京","舟山","郑州","北海","淮安","固原",
                "包头","广元","康定","万县","三亚","三女河","上海","且末","东营","临沂","临沧","丹东","丽江","义乌",
                "乌兰浩特","乌海","乌鲁木齐","九寨沟","九江","二连浩特","井冈山","伊宁","伊春","佛山","佳木斯","依兰",
                "保安营","保山","元谋","克拉玛依","兰州","兴义","兴城","兴宁","包头","北京","北海","南京","南充",
                "南宁","南昌","南通","南阳","博尔塔拉","厦门","合肥","吉安","吉林","呼和浩特","和田","哈密","哈尔滨",
                "喀什","嘉峪关","固原","塔城","大同","大庆","大理","大连","天津","太原","威海","宁波","安庆","安康",
                "安阳","安顺","宜宾","宜昌","富蕴","山海关","常州","常德","广元","广州","广汉","庆阳","庐山","库尔勒",
                "库车","康定","延吉","延安","张家界","徐州","思茅","恩施","惠州","成都","扬州","拉萨","揭阳","敦煌",
                "文山","新源","无锡","昆明","昌都","昭通","晋江","景德镇","朝阳","杭州","林芝","柳州","格尔木","桂林",
                "梁平","梅州","梧州","榆林","武夷山","武汉","永州","汉中","沈阳","泸州","洛阳","济南","济宁","海口",
                "海拉尔","淮安","深圳","温州","湛江","满洲里","潍坊","烟台","牡丹江","玉树","珠海","百色","盐城",
                "石家庄","福州","秦皇岛","绵阳","缨芬河","腾冲","舟山","芒市","芷江","苏州","荆州","荔波","蓬莱",
                "蚌埠","衡阳","衢州","襄樊","西双版纳","西宁","西安","西昌","贵阳","赣州","赤峰","达州","运城",
                "连云港","连城","迪庆","通化","通辽","遵义","邢台","邯郸","郑州","鄂尔多斯","酒泉","重庆","铜仁",
                "银川","锡林浩特","锦州","长春","长沙","长治","长海","长白山","阜阳","阿克苏","阿勒泰","阿尔山",
                "青岛","鞍山","鸡西","黄山","黄岩","黎平","黑河","齐齐哈尔"]
        tempList = []
        todayTotal = (int(random.random()* 1000000000))
        for i in range(100):
            num1 = (int(random.random() * len(city)))
            num2 = (int(random.random() * 1000))
            num3 = (int(random.random() * 100) % 3)
            tempList.append({
                "name" : city[num1],
                "value" : num2,
                "type" : num3,
            })

        res_data ={
            "list" : tempList,
            "todayTotal" : todayTotal,
        }
        data = json.dumps(res_data).encode()
        return HttpResponse(data)
