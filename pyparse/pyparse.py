import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import csv

my_key = 'serviceKey=SPnSFcbM%2BZu8clBECBE4aGJ9Eg%2BRPvmWYAReUVjslhpj3AoDShSTzWx3psY9rOhS1f%2BeWtRY7wEX1%2BNbdDR88A%3D%3D'
params = '&pageNo=1&numOfRows=500&_type=json'
url = 'https://apis.data.go.kr/1613000/ExpBusArrInfoService/getExpBusTmnList?'+my_key+params

resultData = list()
res = requests.get(url)
'''data = res.json()
print(data['response']['body']['items']['item'])'''

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

resultDf.to_csv('Terminal_List.csv',encoding='utf-8')
'''data = res.json()['SeniorStr'][1]['row']
# print(data[0])
df = pd.DataFrame(data)
columns = ["시군명", "매장명", "유형", "주소", "전화번호"]
new_df = df.iloc [: ,1:6]
new_df.columns=columns
new_df
'''