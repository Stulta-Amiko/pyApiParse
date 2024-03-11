import csv

f = open('./data/int_each/광주(유·스퀘어)/태백_TimeTable.csv')
rdr = csv.reader(f)

for item in rdr:
    print(item)

