def terminalNametoFlat(name):
    a = name

    if '광주종합버스터미널' in a:
        a = a.replace('광주종합버스터미널','광주(유·스퀘어)')
    
    if '센트럴시티터미널' in a:
        a = a.replace('센트럴시티터미널','센트럴시티(서울)')

    if '문화' in a:
        a = a.replace('문화','')

    if '시외' in a:
        a = a.replace('시외','')

    if '고속' in a:
        a = a.replace('고속','')

    if '정류소' in a:
        a = a.replace('정류소','')

    if '정류장' in a:
        a = a.replace('정류장','')

    if '공용' in a:
        a = a.replace('공용','')

    if '종합' in a:
        a = a.replace('종합','')

    if '버스' in a:
        a = a.replace('버스','')

    if '터미널' in a:
        a = a.replace('터미널','')  
    
    if '내포신도시' in a:
        a = a.replace('내포신도시','내포신도시고속')
    
    return a

b = '세종청사(하행)'

if '(하행)' in b:
    b = b.replace('(하행)','')

print(b)
