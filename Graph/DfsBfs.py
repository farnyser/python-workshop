import random
from collections import deque


def dfs(graph, start, callback):
    seen = set()
    stack = [start]
    while stack:
        current = stack.pop()
        if current in seen:
            continue
        seen.add(current)
        for n in graph[current]:
            stack.append(n)
        callback(current)


def bfs(graph, start, callback):
    seen = set()
    queue = deque()
    queue.append(start)
    while queue:
        current = queue.pop()
        if current in seen:
            continue
        seen.add(current)
        for n in graph[current]:
            queue.appendleft(n)
        callback(current)


if __name__ == '__main__':
    G = [
        [int(random.random()*10) for i in range(3)]
        for j in range(10)
    ]

    print(G)

    print("DFS")
    dfs(G, 0, lambda x: print(x, G[x]))

    print("BFS")
    bfs(G, 0, lambda x: print(x, G[x]))
