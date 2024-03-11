import heapq
import csv

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
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    queue = []
    heapq.heappush(queue, [distances[start], start])

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if distances[current_node] < current_distance:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, [distance, neighbor])

    return distances

# Example usage:
graph = {
    'A': {'B': 8, 'C': 1, 'D': 2},
    'B': {},
    'C': {'B': 5, 'D': 2},
    'D': {'E': 3, 'F': 5},
    'E': {'F': 1},
    'F': {'A': 5}
}

shortest_distances = dijkstra(graph, 'A')
print(shortest_distances)
