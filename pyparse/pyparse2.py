import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import os
from dotenv import load_dotenv

load_dotenv()

my_key = os.getenv('MY_KEY')
params = os.getenv('PARAMS')
url = 'https://apis.data.go.kr/1613000/ExpBusArrInfoService/getExpBusTmnList?'+my_key+params


resultData = list()
resultData2 = list()
res = requests.get(url)


response_json = json.loads(res.content)
datas = []

data = response_json['response']['body']['items']['item']

tmnCdList = []
tmnNmList = []
tmnDesList = []

for item in data:
    tmnCdList.append(item['tmnCd'])
    tmnNmList.append(item['tmnNm'])

for code in tmnCdList:
    url2 = 'https://apis.data.go.kr/1613000/ExpBusArrInfoService/getArrTmnFromDepTmn?'+my_key+params+'&depTmnCd='+code if type(code) is str else 'https://apis.data.go.kr/1613000/ExpBusArrInfoService/getArrTmnFromDepTmn?'+my_key+params+'&depTmnCd='+ str(code)
    res2 = requests.get(url2)
    response_json2 = json.loads(res2.content)
    print(response_json2)
    if(len(response_json2['response']['body']['items'])):
        if(not isinstance(response_json2['response']['body']['items']['item'],list)):
            data2 = response_json2['response']['body']['items']['item'] 
            rowData = [code,data2['arrTmnCd'],data2['arrTmnNm']]
            resultData2.append(rowData)
        else:
            data2 = response_json2['response']['body']['items']['item']
            for item in data2:
                rowData = [code,item['arrTmnCd'],item['arrTmnNm']]
                resultData2.append(rowData)

    
resultDf = pd.DataFrame(resultData2,columns=['departTmn','tmnCd','tmnNm'])
print(resultDf)

resultDf.to_csv('Terminal_Route.csv',encoding='utf-8')

