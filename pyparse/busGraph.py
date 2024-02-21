import networkx as nx
import matplotlib.pyplot as plt
import csv
import os
from util import findTerminal

if not (os.path.isdir('./data')):
    os.makedirs('./data/graph')
elif not(os.path.isdir('./data/graph')):
    os.mkdir('./data/graph')

if not(os.path.isfile('./data/graph/busGraph.edgelist')):
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

    nx.write_weighted_edgelist(G,'./data/graph/busGraph.edgelist')
else:
    G = nx.read_weighted_edgelist('./data/graph/busGraph.edgelist')

weight = nx.get_edge_attributes(G, 'weight')
relation = nx.get_edge_attributes(G, 'relation')

exitcode = 1

print('종료하시려면 출/도착지 입력시 0을 눌러주세요')

while(exitcode == 1):
    
    depart = findTerminal.find('출발')
    if depart == 0:
        exitcode = 0
    arrive = findTerminal.find('도착')
    if arrive == 0:
        exitcode = 0

    path = nx.astar_path(G, depart, arrive, heuristic=None, weight='weight')
    length = nx.astar_path_length(G,depart, arrive, heuristic=None, weight='weight')
    print("Path: ", path)
    print("Path length: ", length)

