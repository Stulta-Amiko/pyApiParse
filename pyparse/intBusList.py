import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

my_key = os.getenv('MY_KEY')
params = os.getenv('PARAMS')
url = 'https://apis.data.go.kr/1613000/SuburbsBusInfoService/getSuberbsBusTrminlList?'+my_key+params
url2 = 'https://apis.data.go.kr/1613000/SuburbsBusInfoService/getStrtpntAlocFndSuberbsBusInfo?'+my_key+params

today = datetime.today().strftime("%Y%m%d")


resultData = list()
res = requests.get(url)

if not (os.path.isdir('./data')):
    os.mkdir('./data')

response_json = json.loads(res.content)
datas = []

data = response_json['response']['body']['items']['item']

tmnIdList = []
tmnNameList = []

for item in data:
    tmnIdList.append(item['terminalId'])
    tmnNameList.append(item['terminalNm'])

for code in tmnIdList:
    routeUrl = 'https://apis.data.go.kr/1613000/SuburbsBusInfoService/getStrtpntAlocFndSuberbsBusInfo?'+my_key+params+'&depTerminalId='+code+'&depPlandTime='+today
    routeRes = requests.get(routeUrl)
    routeResponse_json = json.loads(routeRes.content)
    if(len(routeResponse_json['response']['body']['items'])):
        routeData = routeResponse_json['response']['body']['items']['item']
        arrTer = []
        for item in routeData:
            if not(item['arrPlaceNm'] in arrTer):
                arrTer.append(item['arrPlaceNm'])
                depterminalName = item['depPlaceNm']
                depterminalCode = code
                arrterminalName = item['arrPlaceNm']
                arrindex = tmnNameList.index(arrterminalName)
                arrterminalCode = tmnIdList[arrindex]
                tripTime = int(item['arrPlandTime']) - int(item['depPlandTime'])
                tripHour = (tripTime//100 if (tripTime / 100) >= 1 else 0)
                if ((tripTime%100)>=60) :
                    tripMin = (tripTime % 100) - 40
                else:
                    tripMin = tripTime % 100 
                charge = 0
                if  'charge' in item:
                    charge = item['charge']
                totalMin = (tripHour*60) + tripMin
                '''
                if 'arrPlaceNm' in item:
                       arriveTerminal = item['arrPlaceNm']
                else:
                    arrCdIndex = tmnCdList.index(arrCd)
                    arriveTerminal = tmnNmList[arrCdIndex] 
                '''
                print('출: '+depterminalName+' '+ depterminalCode+', 도: '+arrterminalName+' '+arrterminalCode + ' 소요시간: '+str(tripHour)+'시간 '+str(tripMin)+'분 '+str(totalMin)+'분 금액'+str(charge)+' 원 ')



'''
for terminalId,terminalNm,terminalRegion in zip(tmnIdList,tmnNmList,tmnRegionList):
    rowData = [terminalId,terminalNm,terminalRegion]
    resultData.append(rowData)
    
resultDf = pd.DataFrame(resultData,columns=['terminalId','terminalNm','Region'])
print(resultDf)

resultDf.to_csv('./data/Terminal_List_Interbus.csv',encoding='utf-8')

'''