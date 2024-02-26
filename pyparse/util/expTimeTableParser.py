import requests
from util import parseTool
import pandas as pd
import json
from datetime import datetime
import time



def timeTableParser(routeData,tmnCdList,tmnNmList,code,my_key,params):
    today = datetime.today().strftime("%Y%m%d")

    resultData = list()

    arrCd = routeData['arrTmnCd']

    detailUrl = 'https://apis.data.go.kr/1613000/ExpBusInfoService/getStrtpntAlocFndExpbusInfo?'+my_key+params+'&depTerminalId=NAEK'+ str(code) +'&arrTerminalId=NAEK'+ str(arrCd) +'&depPlandTime='+today
    try:
        detailRes = requests.get(detailUrl)
    except Exception as e:
        print('requests error')
        print('sleep 30sec and restart')
        time.sleep(15)
        print('retry...')
        detailRes = requests.get(detailUrl)
        
    try:
        detailRes_json = json.loads(detailRes.content)
    except Exception as e:   
        print('error occurred... sleep 60 sec') 
        time.sleep(60)
        print('catch: ', e)
        print('code: '+str(code)+'\n'+' url: ' + detailUrl)
        print('\n'+'retry...')
        detailRes_json = json.loads(detailRes.content)

    if(detailRes_json['response']['body']['items']):
        if(not isinstance(detailRes_json['response']['body']['items']['item'],list)):
            detailedRoute = detailRes_json['response']['body']['items']['item']
            rowData = parseTool.expJsonHandler(detailedRoute,tmnCdList,tmnNmList,code,arrCd)
            arrTmn = rowData[5]

            resultDf = pd.DataFrame(resultData,columns=['departTmnCd','departTmnNm','departHour','departMin','arriveTmnCd','arriveTmnNm','arriveHour','arriveMin','totalMin','charge'])
            print(resultDf)        
            resultDf.to_csv('./data/exp_each/'+tmnNmList[tmnCdList.index(code)]+'/'+ arrTmn +'_TimeTable.csv',encoding='utf-8') 
        else:
            detailedRoute = detailRes_json['response']['body']['items']['item']

            for detailItem in detailedRoute: 
                rowData = parseTool.expJsonHandler(detailItem,tmnCdList,tmnNmList,code,arrCd)
                resultData.append(rowData)
                arrTmn = rowData[5]

            resultDf = pd.DataFrame(resultData,columns=['departTmnCd','departTmnNm','departHour','departMin','arriveTmnCd','arriveTmnNm','arriveHour','arriveMin','totalMin','charge'])
            print(resultDf)        
            resultDf.to_csv('./data/exp_each/'+tmnNmList[tmnCdList.index(code)]+'/'+ arrTmn +'_TimeTable.csv',encoding='utf-8') 