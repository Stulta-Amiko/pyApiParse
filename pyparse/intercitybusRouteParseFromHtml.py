import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import re

response = requests.get("https://transportation.asamaru.net/%EC%8B%9C%EC%99%B8%EB%B2%84%EC%8A%A4/%EC%8B%9C%EA%B0%84%ED%91%9C/수원종합버스터미널/")
html_data = BeautifulSoup(response.text, 'html.parser')
terminal_names = html_data.select('caption > h3')
tables = html_data.select('table')

resultName = list()
resultTime = list()
resultCost = list()

for tag in terminal_names:
	resultName.append(tag.get_text())

for table in tables:
	try:
		table_html = str(table)
		table_df_list = pd.read_html(table_html) 
		if len(table_df_list) > 0:		
			table_df = table_df_list[0]
			duration_data = table_df
			timelist = table_df['소요시간'][0].split(':')
			coststr = table_df['요금(어른)'][0]
			cost = re.sub(r'[^0-9]', '', coststr)
			print(timelist)
			resultCost.append(cost)
			totalTime = int(timelist[0]) * 60 + int(timelist[1])
			resultTime.append(totalTime)	
	except:
		resultTime.append(7700)
		print('pass')

resultData = list()

departTmn = '수원'

for tmnNm,tripTime,cost in zip(resultName,resultTime,resultCost):
    rowData = ['NAI1658501',departTmn,'NAI',tmnNm,tripTime,cost]
    resultData.append(rowData)
    
resultDf = pd.DataFrame(resultData,columns=['departTmnCd','departTmnNm','arriveTmnCd','arriveTmnNm','totalMin','charge'])
print(resultDf)

resultDf.to_csv('./data/indiData/'+departTmn+'_Terminal_List.csv',encoding='utf-8')
