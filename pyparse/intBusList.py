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

today = datetime.today().strftime("%Y%m%d")

  

resultData = list()
res = requests.get(url)

# data 폴더 없을시 폴더 만듦 
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

def jsonHandler(resJson):
    routeData = resJson['response']['body']['items']['item']
    arrTer = []
    for item in routeData:
        try:
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
                #디버그용 print 코드
                print('출: '+depterminalName+' '+ depterminalCode+', 도: '+arrterminalName+' '+arrterminalCode + ' 소요시간: '+str(tripHour)+'시간 '+str(tripMin)+'분 '+str(totalMin)+'분 금액'+str(charge)+' 원 ')
                rowData = [depterminalCode,depterminalName,arrterminalCode,arrterminalName,totalMin,charge]
                return rowData
                #resultData.append(rowData)
        except Exception as e:    
            print('catch: ', e)
            print('item' + item)
            print('code: '+code)
            print('url' +routeUrl)  

for code in tmnIdList:
    routeUrl = 'https://apis.data.go.kr/1613000/SuburbsBusInfoService/getStrtpntAlocFndSuberbsBusInfo?'+my_key+params+'&depTerminalId='+code+'&depPlandTime='+today
    routeRes = requests.get(routeUrl)
    print(routeRes.content)
    try:
        routeResponse_json = json.loads(routeRes.content)
        if(len(routeResponse_json['response']['body']['items'])):
            routeData = routeResponse_json['response']['body']['items']['item']
            rowData = jsonHandler(routeData)
            resultData.append(rowData)
            arrTer = []
            for item in routeData:
                try:
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
                        #디버그용 print 코드
                        print('출: '+depterminalName+' '+ depterminalCode+', 도: '+arrterminalName+' '+arrterminalCode + ' 소요시간: '+str(tripHour)+'시간 '+str(tripMin)+'분 '+str(totalMin)+'분 금액'+str(charge)+' 원 ')
                        rowData = [depterminalCode,depterminalName,arrterminalCode,arrterminalName,totalMin,charge]
                        resultData.append(rowData)
                except Exception as e:    
                    print('catch: ', e)
                    print('item' + item)
                    print('code: '+code)
                    print('url' +routeUrl)
    except Exception as e:    
        print('catch: ', e)
        print('code: '+code)
        print('url' +routeUrl)



resultDf = pd.DataFrame(resultData,columns=['departTmnCd','departTmnNm','arriveTmnCd','arriveTmnNm','totalMin','charge'])
print(resultDf)

resultDf.to_csv('./data/Terminal_Route_detailed.csv',encoding='utf-8')