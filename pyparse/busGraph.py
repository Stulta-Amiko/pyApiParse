import networkx as nx
import matplotlib.pyplot as plt
import csv


G = nx.Graph() 
f = open('./data/Express_Bus_Route_Detailed.csv','r')
rdr = csv.reader(f)

firstPass = 0

for line in rdr:

    if firstPass == 0:
        firstPass += 1
    else:
        G.add_edge(line[2],line[4],weight=int(line[5]),relation='express')  


f = open('./data/Intercity_Bus_Route_Detailed.csv','r')
rdr = csv.reader(f)
 
firstPass = 0

for line in rdr:

    if firstPass == 0:
        firstPass += 1
    else:
        G.add_edge(line[2],line[4],weight=int(line[5]),relation='intercity')  


f.close()

#pos=nx.spring_layout(G)  각 노드, 엣지를 draw하기 위한 position 정보
pos = nx.kamada_kawai_layout(G)
weight = nx.get_edge_attributes(G, 'weight')
relation = nx.get_edge_attributes(G, 'relation')

nx.draw(G,pos,with_labels=True,font_family='AppleGothic', font_size=10)
nx.draw_networkx_edge_labels(G,pos, edge_labels=weight)

plt.show()


