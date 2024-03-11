import csv
import heapq

def graphFromCsv(rdr,graph):
    firstpass = 0
    for item in rdr:
        if firstpass == 0:
            firstpass += 1
        else:
            if not item[2] in graph:
                graph.setdefault(item[2])
                graph[item[2]] = {item[4]: int(item[5])}
            else:
                graph[item[2]].setdefault(item[4],int(item[5])) 
    return graph

def dijkstra(graph, start):
    # 초기화
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    queue = [(0, start)]

    while queue:
        current_cost, current_node = heapq.heappop(queue)
        # 인접한 노드 탐색
        for neighbor, weight in graph[current_node].items():
            cost = current_cost + weight
            if neighbor in graph:
                if cost < distances[neighbor]:
                    distances[neighbor] = cost
                    heapq.heappush(queue, (cost, neighbor))

    return distances

def find_other_paths(graph, start, target, num_paths):
    # 다익스트라 알고리즘으로 최단 경로 찾기
    shortest_distances = dijkstra(graph, start)

    # 최단 경로 제외하고 다른 경로 탐색
    other_paths = []
    visited = set()

    def dfs(node, path, total_cost):
        if node == target:
            other_paths.append((total_cost, path))
            return

        visited.add(node)
        if node in graph:
            for neighbor, weight in graph[node].items():
                if neighbor not in visited:
                    dfs(neighbor, path + [neighbor], total_cost + weight)
                    print(neighbor)
        visited.remove(node)

    dfs(start, [start], 0)

    # 비용이 적은 순서대로 정렬
    other_paths.sort(key=lambda x: x[0])

    return other_paths[:num_paths]


graph = {}

f = open('./data/Intercity_Bus_Route_detailed.csv','r')
rdr = csv.reader(f)

graph = graphFromCsv(rdr,graph)

f = open('./data/Express_Bus_Route_Detailed.csv','r')
rdr = csv.reader(f)

graph = graphFromCsv(rdr,graph)

start_node = '춘천'
end_node = '충주'
num_other_paths = 2

other_paths = find_other_paths(graph, start_node, end_node, num_other_paths)
for i, (cost, path) in enumerate(other_paths, 1):
    print(f"{i}. Cost: {cost}, Path: {' -> '.join(path)}")
