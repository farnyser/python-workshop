def bellman_ford(AM, start):
    predecessor = [None] * len(AM)
    distance = [None] * len(AM)
    distance[start] = 0

    for _ in range(len(AM) + 2):
        changed = False
        for u in range(len(AM)):
            for v in range(len(AM[u])):
                w = AM[u][v]
                if w == 0:
                    continue
                if distance[u] is None:
                    continue
                if distance[v] is None or distance[u] + w < distance[v]:
                    distance[v] = distance[u] + w
                    predecessor[v] = u
                    changed = True
        if not changed:
            return distance, predecessor, False
    return distance, predecessor, True


AM = [
    [0, 0, 8, 2, 0],  # 0
    [3, 1, 1, 0, 0],  # 1
    [0, 0, 1, 2, 3],  # 2
    [0, 5, 1, 4, 0],  # 3
    [2, 0, 1, 1, 1],  # 4
]

AM2 = [
    [0, 0, 8, -2, 0],  # 0
    [3, 1, 1, 0, 0],  # 1
    [0, 0, 1, 2, 3],  # 2
    [0, 5, 1, 4, 0],  # 3
    [2, 0, 1, 1, 1],  # 4
]

AM3 = [
    [0, 0, 8, -2, 0],  # 0
    [3, 1, 1, 0, 0],  # 1
    [0, 0, 1, 2, 3],  # 2
    [1, 5, 1, 4, 0],  # 3
    [2, 0, 1, 1, 1],  # 4
]

print(bellman_ford(AM, 0))
print(bellman_ford(AM2, 0))
print(bellman_ford(AM3, 0))
