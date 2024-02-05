import requests
import pandas as pd
import json
import os
from dotenv import load_dotenv

load_dotenv()

my_key = os.getenv('MY_KEY')
params = os.getenv('PARAMS')
url = 'https://apis.data.go.kr/1613000/ExpBusArrInfoService/getExpBusTmnList?'+my_key+params


resultData = list()
res = requests.get(url)


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
    print(routeResponse_json)
    if(len(routeResponse_json['response']['body']['items'])):
        if(not isinstance(routeResponse_json['response']['body']['items']['item'],list)):
            routeData = routeResponse_json['response']['body']['items']['item'] 
            rowData = [code,routeData['arrTmnCd'],routeData['arrTmnNm']]
            resultData.append(rowData)
        else:
            routeData = routeResponse_json['response']['body']['items']['item']
            for item in routeData:
                rowData = [code,item['arrTmnCd'],item['arrTmnNm']]
                resultData.append(rowData)

    
resultDf = pd.DataFrame(resultData,columns=['departTmnCd','arriveTmnCd','arriveTmnNm'])
print(resultDf)

resultDf.to_csv('Terminal_Route.csv',encoding='utf-8')

