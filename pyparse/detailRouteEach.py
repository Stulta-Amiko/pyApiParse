import requests
import pandas as pd
import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

my_key = os.getenv('MY_KEY')
params = os.getenv('PARAMS')
url = 'https://apis.data.go.kr/1613000/ExpBusArrInfoService/getExpBusTmnList?'+my_key+params
today = datetime.today().strftime("%Y%m%d")

if not (os.path.isdir('./data')):
    os.makedirs('./data/exp_each')
elif not(os.path.isdir('./data/exp_each')):
    os.mkdir('./data/exp_each')


res = requests.get(url)


tmnResponse_json = json.loads(res.content)
data = tmnResponse_json['response']['body']['items']['item']

tmnCdList = []
tmnNmList = []

for item in data:
    tmnCdList.append(item['tmnCd'])
    tmnNmList.append(item['tmnNm'])

for code in tmnCdList:
    resultData = list()
    routeUrl = 'https://apis.data.go.kr/1613000/ExpBusArrInfoService/getArrTmnFromDepTmn?'+my_key+params+'&depTmnCd='+code if type(code) is str else 'https://apis.data.go.kr/1613000/ExpBusArrInfoService/getArrTmnFromDepTmn?'+my_key+params+'&depTmnCd='+ str(code)
    routeRes = requests.get(routeUrl)
    routeResponse_json = json.loads(routeRes.content)
    if(len(routeResponse_json['response']['body']['items'])):
        if(not isinstance(routeResponse_json['response']['body']['items']['item'],list)):
            routeData = routeResponse_json['response']['body']['items']['item'] 
            arrCd = routeData['arrTmnCd']
            detailUrl = 'https://apis.data.go.kr/1613000/ExpBusInfoService/getStrtpntAlocFndExpbusInfo?'+my_key+params+'&depTerminalId=NAEK'+ str(code) +'&arrTerminalId=NAEK'+ str(arrCd) +'&depPlandTime='+today
            detailRes = requests.get(detailUrl)
            detailRes_json = json.loads(detailRes.content)
            if(detailRes_json['response']['body']['items']):
                if(not isinstance(detailRes_json['response']['body']['items']['item'],list)):
                    detailedRoute = detailRes_json['response']['body']['items']['item']
                    departTime = detailItem['depPlandTime'] % 10000
                    departHour = departTime//100
                    departMin = departTime%100
                    arriveTime = detailItem['arrPlandTime'] % 10000
                    arriveHour = arriveTime//100
                    arriveMin = arriveTime%100
                    tripTime = int(detailedRoute['arrPlandTime']) - int(detailedRoute['depPlandTime'])
                    tripHour = (tripTime//100 if (tripTime / 100) >= 1 else 0)
                    if ((tripTime%100)>=60) :
                        tripMin = (tripTime % 100) - 40
                    else:
                        tripMin = tripTime % 100 
                    charge = 0
                    if  'charge' in detailedRoute:
                        charge = detailedRoute['charge']
                    totalMin = (tripHour*60) + tripMin
                    totalTrip = str(tripHour) + '시간 ' + str(tripMin) + '분'
                    if 'arrPlaceNm' in detailedRoute:
                        arriveTerminal = detailedRoute['arrPlaceNm']
                    else:
                        arrCdIndex = tmnCdList.index(arrCd)
                        arriveTerminal = tmnNmList[arrCdIndex] 
                    departTerminal = detailedRoute['depPlaceNm']
                    rowData = [code,departTerminal,departHour,departMin,arrCd,arriveTerminal,arriveHour,arriveMin,totalTrip,totalMin,charge]
                    resultData.append(rowData)
                else:
                    detailedRoute = detailRes_json['response']['body']['items']['item']
                    for detailItem in detailedRoute: 
                        departTime = detailItem['depPlandTime'] % 10000
                        departHour = departTime//100
                        departMin = departTime%100
                        arriveTime = detailItem['arrPlandTime'] % 10000
                        arriveHour = arriveTime//100
                        arriveMin = arriveTime%100
                        tripTime = int(detailItem['arrPlandTime']) - int(detailItem['depPlandTime'])
                        tripHour = (tripTime//100 if (tripTime / 100) >= 1 else 0)
                        if ((tripTime%100)>=60) :
                            tripMin = (tripTime % 100) - 40
                        else:
                            tripMin = tripTime % 100 
                        charge = 0
                        if  'charge' in detailItem:
                            charge = detailItem['charge']
                        totalMin = (tripHour*60) + tripMin
                        totalTrip = str(tripHour) + '시간 ' + str(tripMin) + '분'
                        if 'arrPlaceNm' in detailItem:
                            arriveTerminal = detailItem['arrPlaceNm']
                        else:
                            arrCdIndex = tmnCdList.index(arrCd)
                            arriveTerminal = tmnNmList[arrCdIndex] 
                        departTerminal = detailItem['depPlaceNm']
                        rowData = [code,departTerminal,departHour,departMin,arrCd,arriveTerminal,arriveHour,arriveMin,totalTrip,totalMin,charge]
                        resultData.append(rowData)
            resultDf = pd.DataFrame(resultData,columns=['departTmnCd','departTmnNm','departTime','arriveTmnCd','arriveTmnNm','arriveTime','totalTrip','totalMin','charge'])
            print(resultDf)

            resultDf.to_csv('./data/exp_each/'+ departTerminal +'_Terminal_Route_TimeTable.csv',encoding='utf-8') 
        else:
            routeData = routeResponse_json['response']['body']['items']['item']
            for item in routeData:
                arrCd = item['arrTmnCd']
                detailUrl = 'https://apis.data.go.kr/1613000/ExpBusInfoService/getStrtpntAlocFndExpbusInfo?'+my_key+params+'&depTerminalId=NAEK'+ str(code) +'&arrTerminalId=NAEK'+ str(arrCd) +'&depPlandTime='+today
                detailRes = requests.get(detailUrl)
                detailRes_json = json.loads(detailRes.content)
                if(detailRes_json['response']['body']['items']):
                    if(not isinstance(detailRes_json['response']['body']['items']['item'],list)):
                        detailedRoute = detailRes_json['response']['body']['items']['item']
                        departTime = detailItem['depPlandTime'] % 10000
                        departHour = departTime//100
                        departMin = departTime%100
                        arriveTime = detailItem['arrPlandTime'] % 10000
                        arriveHour = arriveTime//100
                        arriveMin = arriveTime%100
                        tripTime = int(detailedRoute['arrPlandTime']) - int(detailedRoute['depPlandTime'])
                        tripHour = (tripTime//100 if (tripTime / 100) >= 1 else 0)
                        if ((tripTime%100)>=60) :
                            tripMin = (tripTime % 100) - 40
                        else:
                            tripMin = tripTime % 100 
                        charge = 0
                        if  'charge' in detailedRoute:
                            charge = detailedRoute['charge']
                        totalMin = (tripHour*60) + tripMin
                        totalTrip = str(tripHour) + '시간 ' + str(tripMin) + '분'
                        if 'arrPlaceNm' in detailedRoute:
                            arriveTerminal = detailedRoute['arrPlaceNm']
                        else:
                            arrCdIndex = tmnCdList.index(arrCd)
                            arriveTerminal = tmnNmList[arrCdIndex] 
                        departTerminal = detailedRoute['depPlaceNm']
                        rowData = [code,departTerminal,departHour,departMin,arrCd,arriveTerminal,arriveHour,arriveMin,totalTrip,totalMin,charge]
                        resultData.append(rowData)
                    else:
                        detailedRoute = detailRes_json['response']['body']['items']['item']
                        for detailItem in detailedRoute: 
                            departTime = detailItem['depPlandTime'] % 10000
                            departHour = departTime//100
                            departMin = departTime%100
                            arriveTime = detailItem['arrPlandTime'] % 10000
                            arriveHour = arriveTime//100
                            arriveMin = arriveTime%100
                            tripTime = int(detailItem['arrPlandTime']) - int(detailItem['depPlandTime'])
                            tripHour = (tripTime//100 if (tripTime / 100) >= 1 else 0)
                            if ((tripTime%100)>=60) :
                                tripMin = (tripTime % 100) - 40
                            else:
                                tripMin = tripTime % 100 
                            charge = 0
                            if  'charge' in detailItem:
                                charge = detailItem['charge']
                            totalMin = (tripHour*60) + tripMin
                            totalTrip = str(tripHour) + '시간 ' + str(tripMin) + '분'
                            if 'arrPlaceNm' in detailItem:
                                arriveTerminal = detailItem['arrPlaceNm']
                            else:
                                arrCdIndex = tmnCdList.index(arrCd)
                                arriveTerminal = tmnNmList[arrCdIndex] 
                            departTerminal = detailItem['depPlaceNm']
                            rowData = [code,departTerminal,departHour,departMin,arrCd,arriveTerminal,arriveHour,arriveMin,totalTrip,totalMin,charge]
                            resultData.append(rowData)
            resultDf = pd.DataFrame(resultData,columns=['departTmnCd','departTmnNm','departHour','departMin','arriveTmnCd','arriveTmnNm','arriveHour','arriveMin','totalTrip','totalMin','charge'])
            print(resultDf)

            resultDf.to_csv('./data/exp_each/'+ str(code) + '_' + departTerminal +'_Terminal_Route_TimeTable.csv',encoding='utf-8') 
