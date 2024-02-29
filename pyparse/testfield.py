from os import path
import csv
import time
import pandas as pd

f = open('./data/Intercity_Bus_Route_detailed.csv','r')
rdr = csv.reader(f)
lines = []
 
firstpass = 0

for line in rdr:
	if not firstpass == 0:	
		if not path.isfile('./data/int_each/'+line[2] +'/'+ line[4]+'_TimeTable.csv'):
			if path.isfile('./data/int_each/'+line[2] +'/'+'울산신복_TimeTable.csv'):
				copylist = []
				firstTemp = 0
				f2 = open('./data/int_each/'+line[2] +'/'+'울산신복_TimeTable.csv')
				modiReader = csv.reader(f2)
				for item in modiReader:
					if firstTemp == 0:
						firstTemp += 1
					else:
						row = [item[1],item[2],item[3],item[4],item[5],'신복환승센터',item[7],item[8],item[9],item[10]]
						copylist.append(row)
				print(copylist)
				resultDf = pd.DataFrame(copylist,columns=['departTmnCd','departTmnNm','departHour','departMin','arriveTmnCd','arriveTmnNm','arriveHour','arriveMin','totalMin','charge'])
				print(resultDf)

				resultDf.to_csv('./data/int_each/'+line[2] +'/'+'신복환승센터_TimeTable.csv',encoding='utf-8')
			print('./data/int_each/'+line[2] +'/'+ line[4]+'_TimeTable.csv')
			lines.append('./data/int_each/'+line[2] +'/'+ line[4]+'_TimeTable.csv')
	firstpass+=1
      
f = open('modify.csv','w',newline='') #원본을 훼손할 위험이 있으니 다른 파일에 저장하는 것을 추천합니다.
wr = csv.writer(f)
wr.writerows(lines)

f.close()