import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime
import time
from util import expTimeTableParser
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
    routeUrl = 'https://apis.data.go.kr/1613000/ExpBusArrInfoService/getArrTmnFromDepTmn?'+my_key+params+'&depTmnCd='+code if type(code) is str else 'https://apis.data.go.kr/1613000/ExpBusArrInfoService/getArrTmnFromDepTmn?'+my_key+params+'&depTmnCd='+ str(code)

    try:
        routeRes = requests.get(routeUrl)
    except:
        print('requests error')
        print('sleep 30sec and restart')
        time.sleep(15)
        print('retry...')
        routeRes = requests.get(routeUrl) 

    routeResponse_json = json.loads(routeRes.content)
    if(len(routeResponse_json['response']['body']['items'])):
        if not (os.path.isdir('./data/exp_each/'+ tmnNmList[tmnCdList.index(code)])):
            os.makedirs('./data/exp_each/'+ tmnNmList[tmnCdList.index(code)])
        if(not isinstance(routeResponse_json['response']['body']['items']['item'],list)):
            routeData = routeResponse_json['response']['body']['items']['item'] 
            expTimeTableParser.timeTableParser(routeData,tmnCdList,tmnNmList,code,my_key,params)
        else:
            routeData = routeResponse_json['response']['body']['items']['item']
            for item in routeData:
                expTimeTableParser.timeTableParser(item,tmnCdList,tmnNmList,code,my_key,params)
