import re
import os
files = os.listdir('./data/inter/')

#파일명 출력하기
find = list()
for file in files :
    numbers = re.sub(r'[^0-9]', '', file)
    find.append(numbers)

print(max(find))