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


response_json = json.loads(res.content)
datas = []

data = response_json['response']['body']['items']['item']

tmnCdList = []
tmnNmList = []

for item in data:
    tmnCdList.append(item['tmnCd'])
    tmnNmList.append(item['tmnNm'])

print(tmnCdList)
for tmnCd,tmnNm in zip(tmnCdList,tmnNmList):
    rowData = [tmnCd,tmnNm]
    resultData.append(rowData)
    
resultDf = pd.DataFrame(resultData,columns=['tmnCd','tmnNm'])
print(resultDf)

resultDf.to_csv('./data/Terminal_List.csv',encoding='utf-8')
