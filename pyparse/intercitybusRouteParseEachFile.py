import requests
import pandas as pd
import json
import os
import re
from dotenv import load_dotenv
from datetime import datetime
from util import parseTool
import time

load_dotenv()
# data 폴더 없을시 폴더 만듦 
if not (os.path.isdir('./data')):
    os.mkdir('./data')

#함수로 분리에정
my_key = os.getenv('MY_KEY')
params = os.getenv('PARAMS')
url = 'https://apis.data.go.kr/1613000/SuburbsBusInfoService/getSuberbsBusTrminlList?'+my_key+params

today = datetime.today().strftime("%Y%m%d")

resultData = list()
tmnIdList = list()
tmnNameList = list()



#시외버스 터미널 ID와 이름 조회 인덱스 별로 서로 매핑
res = requests.get(url)

response_json = json.loads(res.content)

data = response_json['response']['body']['items']['item']

for item in data:
    tmnIdList.append(item['terminalId'])
    tmnNameList.append(item['terminalNm'])

tryNum = 0

if not (os.path.isdir('./data/int_each')):
    os.makedirs('./data/int_each')

# 데이터 수집 중간에 끊겼을 때 기존 저장된 파일을 기반으로 앞에서 수집된 데이터는 넘기고 그 다음 데이터 부터 수집하는 코드
    
files = os.listdir('./data/int_each/')

find = list()

for file in files :
    numbers = re.sub(r'[^0-9]', '', file)
    find.append(numbers)

print('최근에 종료된 index 입력\n')
lastIndex = int(input())


# 터미널 ID를 기반으로 각 터미널별 거리가중치 및 갈수있는 루트 조회
for code in tmnIdList:
    if find and tryNum < lastIndex:
        tryNum += 1
        print(tryNum)

    if tryNum >= lastIndex: 
        routeUrl = 'https://apis.data.go.kr/1613000/SuburbsBusInfoService/getStrtpntAlocFndSuberbsBusInfo?'+my_key+params+'&depTerminalId='+code+'&depPlandTime='+today
        tryNum += 1
        try:
            routeRes = requests.get(routeUrl)
        except:
            print('requests error')
            print('sleep 30sec and restart')
            time.sleep(15)
            print('retry...')
            routeRes = requests.get(routeUrl) 

        try:
            routeResponse_json = json.loads(routeRes.content)
        except Exception as e:   
            print('error occurred... sleep 60 sec') 
            time.sleep(60)
            print('catch: ', e)
            print('code: '+code+'\n'+' url: ' +routeUrl)
            print('\n'+'retry...')
            routeResponse_json = json.loads(routeRes.content)

        if(len(routeResponse_json['response']['body']['items'])):
                rowData = parseTool.intJsonHandlerEachFile(routeResponse_json,code,tmnNameList,tmnIdList)
                for rowItem in rowData:
                    print(rowItem)
                    resultData.append(rowItem)
                    
        time.sleep(5)
        print(tryNum)
        '''
        if((tryNum % 200) == 0):
            resultDf = pd.DataFrame(resultData,columns=['departTmnCd','departTmnNm','arriveTmnCd','arriveTmnNm','totalMin','charge'])
            print(resultDf)

            resultDf.to_csv('./data/inter/'+ str(tryNum) +'Intercity_Bus_Route_detailed.csv',encoding='utf-8')
'''

print('finish')