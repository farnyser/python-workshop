import heapq


def dijkstra(adj_matrix, start_node, destination_node):
    pred = {}
    visited = {}

    todo = [(0, start_node, None)]
    while todo:
        (cost, current, previous) = heapq.heappop(todo)
        if current in visited:
            continue
        visited[current] = cost
        pred[current] = previous
        if current is destination_node:
            break
        for i in range(len(adj_matrix[current])):
            if adj_matrix[current][i] > 0:
                heapq.heappush(todo, (cost + adj_matrix[current][i], i, current))

    path = [destination_node]
    while True:
        p = pred[path[len(path)-1]]
        if p is None:
            break
        path.append(p)

    path.reverse()
    return visited[destination_node], path

if __name__ == '__main__':
    AM = [
        [0, 0, 8, 2, 0], # 0
        [3, 1, 1, 0, 0], # 1
        [0, 0, 1, 2, 3], # 2
        [0, 5, 1, 4, 0], # 3
        [2, 0, 1, 1, 1], # 4
    ]

    for node in AM:
        print(node)

    (c, path) = dijkstra(AM, 3, 1)
    print("going from %i to %i has a cost of %i" % (path[0], path[len(path)-1], c))
    print("path: ", path)