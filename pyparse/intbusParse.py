import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import os
from dotenv import load_dotenv

load_dotenv()

my_key = os.getenv('MY_KEY')
params = os.getenv('PARAMS')
url = 'https://apis.data.go.kr/1613000/SuburbsBusInfoService/getSuberbsBusTrminlList?'+my_key+params

resultData = list()
res = requests.get(url)


response_json = json.loads(res.content)
datas = []

data = response_json['response']['body']['items']['item']

tmnIdList = []
tmnNmList = []
tmnRegionList = []

for item in data:
    tmnIdList.append(item['terminalId'])
    tmnNmList.append(item['terminalNm'])
    tmnRegionList.append(item['cityName'])

for terminalId,terminalNm,terminalRegion in zip(tmnIdList,tmnNmList,tmnRegionList):
    rowData = [terminalId,terminalNm,terminalRegion]
    resultData.append(rowData)
    
resultDf = pd.DataFrame(resultData,columns=['terminalId','terminalNm','Region'])
print(resultDf)

resultDf.to_csv('Terminal_List_Interbus.csv',encoding='utf-8')

