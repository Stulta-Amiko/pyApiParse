import os
import csv
import pandas as pd
import time

newIndex = 0
firstPass = 0

resultData = list()

f = open('./data/Intercity_Bus_Route_detailed.csv','r')

rdr = csv.reader(f)

for item in rdr:
    if firstPass == 0:
        firstPass += 1
    else:
        data = [item[1],item[2],item[3],item[4],item[5],item[6]]
        resultData.append(data)

print(resultData)
    
resultDf = pd.DataFrame(resultData,columns=['departTmnCd','departTmnNm','arriveTmnCd','arriveTmnNm','totalMin','charge'])

print(resultDf)

resultDf.to_csv('./clean_csv.csv',encoding='utf-8')
