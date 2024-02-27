arrterminalName = '김해/고속'

if '/' in arrterminalName:
    arrterminalName = arrterminalName.replace('/','_')

print(arrterminalName)