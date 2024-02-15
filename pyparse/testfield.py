import ssl

result = list()

a = [[1,2,'2'],[3,4,'5']]
b = [[5,6,'6'],[6,7,[7]]]

for item in a:
    result.append(item)

for item in b:
    result.append(item)

print(result)