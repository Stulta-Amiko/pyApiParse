import networkx as nx
import matplotlib.pyplot as plt
import csv
import os

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

path = nx.astar_path(G, '춘천', '충주', heuristic=None, weight='weight')
length = nx.astar_path_length(G,'춘천', '충주', heuristic=None, weight='weight')
print("Path: ", path)
print("Path length: ", length)

'''
nx.draw(G,pos,with_labels=True,font_family='AppleGothic', font_size=10)
nx.draw_networkx_edge_labels(G,pos, edge_labels=weight)
'''

plt.show()


