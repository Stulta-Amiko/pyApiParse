


def jsonHandler(resJson, code, tmnNmList, tmnIDList, url):
    routeData = resJson['response']['body']['items']['item']
    arrTer = []
    for item in routeData:
        try:
            if not(item['arrPlaceNm'] in arrTer):
                arrTer.append(item['arrPlaceNm'])
                depterminalName = item['depPlaceNm']
                depterminalCode = code
                arrterminalName = item['arrPlaceNm']
                arrindex = tmnNmList.index(arrterminalName) #tmnNameList
                arrterminalCode = tmnIDList[arrindex] #tmnIdList
                tripTime = int(item['arrPlandTime']) - int(item['depPlandTime'])
                tripHour = (tripTime//100 if (tripTime / 100) >= 1 else 0)
                if ((tripTime%100)>=60) :
                    tripMin = (tripTime % 100) - 40
                else:
                    tripMin = tripTime % 100 
                charge = 0
                if  'charge' in item:
                    charge = item['charge']
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
                return rowData
                #resultData.append(rowData)
        except Exception as e:    
            print('catch: ', e)
            print('item' + item)
            print('code: '+code)
            print('url' + url) 