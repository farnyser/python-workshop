import random
from collections import deque

import sys


def prim_mst(graph, start):
    pred = {}
    cost = {}

    for node in range(len(graph)):
        cost[node] = sys.maxsize

    cost[start] = 0
    pred[start] = None

    while True:
        best = (sys.maxsize, None, None)
        for node in pred.keys():
            for out_node in range(len(AM[node])):
                out_cost = graph[node][out_node]
                if out_node not in pred and out_cost < best[0] and out_cost != 0:
                    best = (out_cost, node, out_node)

        if best[1] is None:
            break
        pred[best[2]] = best[1]
        cost[best[2]] = cost[best[1]] + best[0]

    R = [[0 for j in range(len(pred))] for i in range(len(pred))]
    for k in pred:
        v = pred[k]
        if v is not None:
            R[v][k] = graph[v][k]
            R[k][v] = graph[v][k]

    return R


if __name__ == '__main__':
    AM = [
        [0, 10, 30, 15], # 0
        [10, 0, 40, 0], # 1
        [30, 40, 0, 50], # 2
        [15, 0, 50, 0], # 3
    ]

    print("MST")
#    print(prim_mst(AM, 0))
#    print(prim_mst(AM, 1))
#    print(prim_mst(AM, 2))
#    print(prim_mst(AM, 3))

    AM2 = [
        [0,  10, 20, 0,  0], # 0
        [10, 0,  30, 5,  0], # 1
        [20, 30,  0, 15, 6], # 2
        [0,  5,  15, 0,  8], # 3
        [0,  0,   6, 8,  0], # 4
    ]

    print("other MST")
    print(prim_mst(AM2, 0))

