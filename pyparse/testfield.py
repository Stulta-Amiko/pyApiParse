import csv
 
f = open('./data/Intercity_Bus_Route_Detailed.csv','r')
rdr = csv.reader(f)
 
lines = []

for line in rdr:
    if line[5] == '5':
        print(line[1]+','+line[3])
'''
f = open('./example.csv','w',newline='') #원본을 훼손할 위험이 있으니 다른 파일에 저장하는 것을 추천합니다.
wr = csv.writer(f)
wr.writerows(lines)
'''
 
f.close()
 