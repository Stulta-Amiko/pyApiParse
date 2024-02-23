import time
import os


def jsonHandler(resJson, code, tmnNmList, tmnIDList):
    resultData = list()
    try:
        routeData = resJson['response']['body']['items']['item']
        arrTer = []
        for item in routeData:
            if('arrPlaceNm' in item):
                if not(item['arrPlaceNm'] in arrTer):
                    arrTer.append(item['arrPlaceNm'])
                    depterminalName = item['depPlaceNm']
                    depterminalCode = code
                    arrterminalName = item['arrPlaceNm']
                    if arrterminalName in tmnNmList:
                        arrindex = tmnNmList.index(arrterminalName) #tmnNameList
                        arrterminalCode = tmnIDList[arrindex] #tmnIdList
                    else:
                        arrterminalCode = 'no information'
                    tripTime = int(item['arrPlandTime']) - int(item['depPlandTime'])
                    tripHour = (tripTime//100 if (tripTime / 100) >= 1 else 0)
                    if ((tripTime%100)>=60) :
                        tripMin = (tripTime % 100) - 40
                    else:
                        tripMin = tripTime % 100 
                    charge = 0
                    if  'charge' in item:
                        charge = item['charge']
                    if tripHour >= 24:
                        tripHour = 77
                        tripMin = 0
                        if '/' in arrterminalName:
                            arrterminalName = arrterminalName.replace('/','_')
                        if '/' in depterminalName:
                            depterminalName = depterminalName.replace('/','_')
                        if not (os.path.isdir('./data/correction')):
                            os.mkdir('./data/correction')
                        if not(os.path.isdir('./data/correction/'+depterminalName+'_'+arrterminalName)):
                            os.mkdir('./data/correction/'+depterminalName+'_'+arrterminalName)
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
        time.sleep(15)
        print('catch: ', e)
        print('item' + item)
        print('code: '+code)
    return resultData


def expJsonHandler(detailItem,tmnCdList,tmnNmList,code,arrCd):
    departTime = int(detailItem['depPlandTime']) % 10000
    departHour = departTime//100
    departMin = departTime%100
    arriveTime = int(detailItem['arrPlandTime']) % 10000
    arriveHour = arriveTime//100
    arriveMin = arriveTime%100
    tripTime = int(detailItem['arrPlandTime']) - int(detailItem['depPlandTime'])
    tripHour = (tripTime//100 if (tripTime / 100) >= 1 else 0)
    if ((tripTime%100)>=60) :
        tripMin = (tripTime % 100) - 40
    else:
        tripMin = tripTime % 100 
    charge = 0
    if  'charge' in detailItem:
        charge = detailItem['charge']
    totalMin = (tripHour*60) + tripMin
    totalTrip = str(tripHour) + '시간 ' + str(tripMin) + '분'
    if 'arrPlaceNm' in detailItem:
        arriveTerminal = detailItem['arrPlaceNm']
    else:
        arrCdIndex = tmnCdList.index(arrCd)
        arriveTerminal = tmnNmList[arrCdIndex] 
    departTerminal = detailItem['depPlaceNm']
    rowData = [code,departTerminal,departHour,departMin,arrCd,arriveTerminal,arriveHour,arriveMin,totalTrip,totalMin,charge]
    return rowData