from timeit import timeit

# Items are limited (we have only one of each items)


def optimize(WV,C):
    p = lambda x: WV[x][0]
    v = lambda x: WV[x][1]

    n = len(WV)
    Opt = [[0] * (C+1) for _ in range(n + 1)]
    Sel = [[False] * (C+1) for _ in range(n + 1)]

    for cap in range(WV[0][0], C+1):
        Opt[0][cap] = WV[0][1]
        Sel[0][cap] = True

    for i in range(1, n):
        for cap in range(C + 1):
            if cap >= p(i) and Opt[i-1][cap - p(i)] + v(i) > Opt[i-1][cap]:
                Opt[i][cap] = Opt[i-1][cap - p(i)] + v(i)
                Sel[i][cap] = True
            else:
                Opt[i][cap] = Opt[i-1][cap]
                Sel[i][cap] = False

    cap = C
    sol = []
    for i in range(n-1, -1, -1):
        if Sel[i][cap]:
            sol.append(i)
            cap -= p(i)
    return Opt[n-1][C], sol


WV = [(2, 1),
      (3, 2),
      (5, 3),
      (8, 10),
      (10,13),
      (15,15),
      (20,30)]

print(optimize(WV, 1))
print(optimize(WV, 2))
print(optimize(WV, 3))
print(optimize(WV, 4))
print(optimize(WV, 5))
print(optimize(WV, 10))
print(optimize(WV, 50))