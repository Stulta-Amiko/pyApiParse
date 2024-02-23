import requests
import pandas as pd
import json
import os
from dotenv import load_dotenv
from util import parseTool
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

print(res)

tmnResponse_json = json.loads(res.content)
data = tmnResponse_json['response']['body']['items']['item']

tmnCdList = []
tmnNmList = []

for item in data:
    tmnCdList.append(item['tmnCd'])
    tmnNmList.append(item['tmnNm'])

for code in tmnCdList:
    routeUrl = 'https://apis.data.go.kr/1613000/ExpBusArrInfoService/getArrTmnFromDepTmn?'+my_key+params+'&depTmnCd='+code if type(code) is str else 'https://apis.data.go.kr/1613000/ExpBusArrInfoService/getArrTmnFromDepTmn?'+my_key+params+'&depTmnCd='+ str(code)
    routeRes = requests.get(routeUrl)
    routeResponse_json = json.loads(routeRes.content)
    if(len(routeResponse_json['response']['body']['items'])):
        if not (os.path.isdir('./data/exp_each/'+ tmnNmList[tmnCdList.index(code)])):
            os.makedirs('./data/exp_each/'+ tmnNmList[tmnCdList.index(code)])
        if(not isinstance(routeResponse_json['response']['body']['items']['item'],list)):
            resultData = list()
            routeData = routeResponse_json['response']['body']['items']['item'] 
            arrCd = routeData['arrTmnCd']
            detailUrl = 'https://apis.data.go.kr/1613000/ExpBusInfoService/getStrtpntAlocFndExpbusInfo?'+my_key+params+'&depTerminalId=NAEK'+ str(code) +'&arrTerminalId=NAEK'+ str(arrCd) +'&depPlandTime='+today
            detailRes = requests.get(detailUrl)
            detailRes_json = json.loads(detailRes.content)
            if(detailRes_json['response']['body']['items']):
                if(not isinstance(detailRes_json['response']['body']['items']['item'],list)):
                    detailedRoute = detailRes_json['response']['body']['items']['item']
                    rowData = parseTool.expJsonHandler(detailedRoute,tmnCdList,tmnNmList,code,arrCd)
                    arrTmn = routeData[5]
                    resultDf = pd.DataFrame(resultData,columns=['departTmnCd','departTmnNm','departTime','arriveTmnCd','arriveTmnNm','arriveTime','totalTrip','totalMin','charge'])
                    print(resultDf)        
                    resultDf.to_csv('./data/exp_each/'+tmnNmList[tmnCdList.index(code)]+'/'+ arrTmn +'_TimeTable.csv',encoding='utf-8') 
                else:
                    detailedRoute = detailRes_json['response']['body']['items']['item']
                    for detailItem in detailedRoute: 
                        rowData = parseTool.expJsonHandler(detailedRoute,tmnCdList,tmnNmList,code,arrCd)
                        resultData.append(rowData)
                        arrTmn = routeData[5]
                    resultDf = pd.DataFrame(resultData,columns=['departTmnCd','departTmnNm','departTime','arriveTmnCd','arriveTmnNm','arriveTime','totalTrip','totalMin','charge'])
                    print(resultDf)        
                    resultDf.to_csv('./data/exp_each/'+tmnNmList[tmnCdList.index(code)]+'/'+ arrTmn +'_TimeTable.csv',encoding='utf-8') 
        else:
            routeData = routeResponse_json['response']['body']['items']['item']
            for item in routeData:
                resultData = list()
                arrCd = item['arrTmnCd']
                detailUrl = 'https://apis.data.go.kr/1613000/ExpBusInfoService/getStrtpntAlocFndExpbusInfo?'+my_key+params+'&depTerminalId=NAEK'+ str(code) +'&arrTerminalId=NAEK'+ str(arrCd) +'&depPlandTime='+today
                detailRes = requests.get(detailUrl)
                detailRes_json = json.loads(detailRes.content)
                if(detailRes_json['response']['body']['items']):
                    if(not isinstance(detailRes_json['response']['body']['items']['item'],list)):
                        detailedRoute = detailRes_json['response']['body']['items']['item']
                        rowData = parseTool.expJsonHandler(detailedRoute,tmnCdList,tmnNmList,code,arrCd)
                        arrTmn = routeData[5]
                        resultDf = pd.DataFrame(resultData,columns=['departTmnCd','departTmnNm','departTime','arriveTmnCd','arriveTmnNm','arriveTime','totalTrip','totalMin','charge'])
                        print(resultDf)        
                        resultDf.to_csv('./data/exp_each/'+tmnNmList[tmnCdList.index(code)]+'/'+ arrTmn +'_TimeTable.csv',encoding='utf-8') 
                    else:
                        detailedRoute = detailRes_json['response']['body']['items']['item']
                        for detailItem in detailedRoute: 
                            rowData = parseTool.expJsonHandler(detailedRoute,tmnCdList,tmnNmList,code,arrCd)
                            resultData.append(rowData)
                            arrTmn = routeData[5]
                        resultDf = pd.DataFrame(resultData,columns=['departTmnCd','departTmnNm','departTime','arriveTmnCd','arriveTmnNm','arriveTime','totalTrip','totalMin','charge'])
                        print(resultDf)        
                        resultDf.to_csv('./data/exp_each/'+tmnNmList[tmnCdList.index(code)]+'/'+ arrTmn +'_TimeTable.csv',encoding='utf-8') 

