import os
import csv
import requests
import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from util import parseTool

load_dotenv()

link = os.getenv('PARSELINK')

while(1):
	print('시간표 링크의 터미널 이름을 입력해주세요.\n')
	requestLink = input()

	print(link+requestLink+"/")
	response = requests.get(link+requestLink+"/")


	html_data = BeautifulSoup(response.text, 'html.parser')
	terminal_names = html_data.select('caption > h3')
	tables = html_data.select('table')

	resultName = list()
	resultTime = list()
	resultCost = list()

	print('출발지 터미널이름을 입력해주세요.\n')
	departTmn = input()

	f = open('./data/Terminal_List_Interbus.csv','r')
	rdr = csv.reader(f)
	lines = []

	for line in rdr:
		if line[2] == departTmn:
			departTmnCd = line[1]
	
	f.close()

	if not (os.path.isdir('./data/int_each/'+ departTmn)):
		os.mkdir('./data/int_each/'+ departTmn)

	for table, tag in zip(tables, terminal_names):
		resultData = list()
		try:
			table_html = str(table)
			arriveTerminal = parseTool.terminalNametoFlat(tag.get_text())
			print(arriveTerminal)
			table_df_list = pd.read_html(table_html) 
			if len(table_df_list) > 0:		
				table_df = table_df_list[0]
				for item in table_df_list:
					for depTime,arrTime,tripTime,cash in zip(item['출발'],item['도착'],item['소요시간'],item['요금(어른)']):
						departTime = depTime.split(':') 
						departHour = int(departTime[0])
						departMin = int(departTime[1])
						arriveTime = arrTime.split(':') 
						arriveHour = int(arriveTime[0])
						arriveMin = int(arriveTime[1])
						timelist = tripTime.split(':')
						totalTime = int(timelist[0]) * 60 + int(timelist[1])
						cash = cash.replace(' 원','')
						cashlist = cash.split(',')
						charge = int(cashlist[0]) * 1000 + int(cashlist[1])
						resultData.append([departTmnCd,departTmn,departHour,departMin,'NAI',arriveTerminal,arriveHour,arriveMin,totalTime,charge])

				resultDf = pd.DataFrame(resultData,columns=['departTmnCd','departTmnNm','departHour','departMin','arriveTmnCd','arriveTmnNm','arriveHour','arriveMin','totalMin','charge'])
				resultDf.to_csv('./data/int_each/'+departTmn+'/'+ arriveTerminal +'_TimeTable.csv',encoding='utf-8') 
		except Exception as e:
			print(e)
			print('pass')
	print('출발지: '+ departTmn +' csv 작성완료.')
	print('저장경로: /data/int_each/'+departTmn + '\n')
