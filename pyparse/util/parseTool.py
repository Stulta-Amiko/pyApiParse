import time
import os
import pandas as pd


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


def intJsonHandlerEachFile(resJson, code, tmnNmList, tmnIDList):
    resultData = list()
    try:
        routeData = resJson['response']['body']['items']['item']
        arrTer = []
        depTer = ''
        for item in routeData:
            if('arrPlaceNm' in item):
                if not(item['arrPlaceNm'] in arrTer):
                    arrTer.append(item['arrPlaceNm'])

        for idx,val in enumerate(arrTer):
            globals()['data{}'.format(idx)] = list()

        for item in routeData:
            if('arrPlaceNm' in item):
                depterminalName = item['depPlaceNm']
                depterminalCode = code
                depTer = depterminalName
                if not (os.path.isdir('./data/int_each/'+ depterminalName)):
                    os.makedirs('./data/int_each/'+ depterminalName)
                departTime = item['depPlandTime'] % 10000
                departHour = departTime//100
                departMin = departTime%100
                arriveTime = item['arrPlandTime'] % 10000
                arriveHour = arriveTime//100
                arriveMin = arriveTime%100
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
                editArrive = arrterminalName
                if '/' in arrterminalName:
                        arrterminalName = arrterminalName.replace('/','_')
                if '/' in depterminalName:
                        depterminalName = depterminalName.replace('/','_')
                if tripHour >= 24:
                    tripHour = 77
                    tripMin = 0       
                    if not (os.path.isdir('./data/correction')):
                        os.mkdir('./data/correction')
                    if not(os.path.isdir('./data/correction/'+depterminalName+'_'+arrterminalName)):
                        os.mkdir('./data/correction/'+depterminalName+'_'+arrterminalName)
                totalMin = (tripHour*60) + tripMin
                #디버그용 print 코드
                print('출: '+depterminalName+' '+ depterminalCode+', 도: '+arrterminalName+' '+arrterminalCode + ' 소요시간: '+str(tripHour)+'시간 '+str(tripMin)+'분 '+str(totalMin)+'분 금액'+str(charge)+' 원 ')
                globals()['data{}'.format(arrTer.index(editArrive))].append([depterminalCode,depterminalName,departHour,departMin,arrterminalCode,arrterminalName,arriveHour,arriveMin,totalMin,charge])
                #rowData = [depterminalCode,depterminalName,arrterminalCode,arrterminalName,totalMin,charge]
                #resultData.append(rowData)
        for idx,val in enumerate(arrTer):
            resultData = list()
            for data in globals()['data{}'.format(idx)]:
                resultData.append(data)
            resultDf = pd.DataFrame(resultData,columns=['departTmnCd','departTmnNm','departHour','departMin','arriveTmnCd','arriveTmnNm','arriveHour','arriveMin','totalMin','charge'])
            print(resultDf)        
            if '/' in val:
                editValue = val.replace('/','_')
                resultDf.to_csv('./data/int_each/'+depTer+'/'+ editValue +'_TimeTable.csv',encoding='utf-8') 
            else:
                resultDf.to_csv('./data/int_each/'+depTer+'/'+ val +'_TimeTable.csv',encoding='utf-8') 
    except Exception as e:
        time.sleep(15)
        print('catch: ', e)
        print('item ' + item)
        print('code: '+code)
    print(resultData)
    return resultData


def expJsonHandler(detailItem,tmnCdList,tmnNmList,code,arrCd):
    departTime = detailItem['depPlandTime'] % 10000
    departHour = departTime//100
    departMin = departTime%100
    arriveTime = detailItem['arrPlandTime'] % 10000
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
    rowData = [code,departTerminal,departHour,departMin,arrCd,arriveTerminal,arriveHour,arriveMin,totalMin,charge]
    return rowData