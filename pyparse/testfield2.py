import os
import csv
import pandas as pd

f = open('./data/omission_new2.csv','r')
rdr = csv.reader(f)
lines = []

fisrtpass = 0
newindex = 2016
for line in rdr:
    if fisrtpass == 0:
        fisrtpass += 1
    else:
        print(line[0])
        line[0] = newindex
        newindex += 1
    lines.append(line)
    
 
f = open('omission_new3.csv','w',newline='') #원본을 훼손할 위험이 있으니 다른 파일에 저장하는 것을 추천합니다.
wr = csv.writer(f)
wr.writerows(lines)
 
f.close()



'''
path = "./data/indiData/"
file_list = os.listdir(path)

print(file_list)

newIndex = 0
resultData = list()

for path in file_list:
    f = open('./data/indiData/'+path,'r')
    rdr = csv.reader(f)

    firstPass = 0

    for line in rdr:
        if firstPass == 0:
            firstPass += 1
        else:
            rowData = [line[1],line[2],line[3],line[4],line[5],line[6]]
            newIndex += 1
            resultData.append(rowData)

    
resultDf = pd.DataFrame(resultData,columns=['departTmnCd','departTmnNm','arriveTmnCd','arriveTmnNm','totalMin','charge'])

print(resultDf)

resultDf.to_csv('./data/indiData/omission_Bus_Route_detailed.csv',encoding='utf-8')
'''