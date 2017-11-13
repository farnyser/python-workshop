from timeit import timeit

# Items are unlimited (we have an unlimited amount of each items)

def optimize(WV,C):
    best = 0
    for w,v in WV:
        if w <= C:
            a = v + optimize(WV, C-w)
            if a > best:
                best = a
    return best


def optimize_wcache(WV,C,cache = {}):
    best = 0
    if C in cache:
        return cache[C]
    for w,v in WV:
        if w <= C:
            a = v + optimize_wcache(WV, C-w, cache)
            if a > best:
                best = a
    cache[C] = best
    return best


def optimize_btup(WV,C,cache = {}):
    cache[0] = 0
    for i in range(1,C+1):
        cache[i] = 0
        for w,v in WV:
            if w <= i:
                cache[i] = max([cache[i], cache[i-w] + v])
    return cache[C]


print("--")

WV = [(1, 1),
      (3, 2),
      (5, 6)]

print(optimize(WV, 1))
print(optimize(WV, 2))
print(optimize(WV, 3))
print(optimize(WV, 4))
print(optimize(WV, 5))
print(optimize(WV, 25))

print("--")

WV = [(1, 1),
      (2, 3),
      (3, 9)]

print(optimize(WV, 1))
print(optimize(WV, 2))
print(optimize(WV, 3))
print(optimize(WV, 4))
print(optimize(WV, 5))
print(optimize(WV, 25))

print("--")

WV = [(2, 1),
      (3, 2),
      (5, 3)]

print(optimize(WV, 1))
print(optimize(WV, 2))
print(optimize(WV, 3))
print(optimize(WV, 4))
print(optimize(WV, 5))
print(optimize(WV, 25))

print("--")


WV = [(2, 1),
      (3, 2),
      (5, 3),
      (8, 10),
      (10,13),
      (15,15),
      (20,30)]

print(optimize(WV, 30))
print(optimize_wcache(WV, 30))

print("time:", timeit('optimize(WV,30)', setup='from __main__ import optimize; from __main__ import WV', number=100))
print("time:", timeit('optimize_wcache(WV,30)', setup='from __main__ import optimize_wcache; from __main__ import WV', number=100))

print(optimize_wcache(WV, 1000))
print(optimize_btup(WV, 1000))

print("time:", timeit('optimize_wcache(WV,1000)', setup='from __main__ import optimize_wcache; from __main__ import WV', number=100))

# print(optimize_wcache(WV, 10000)) - too many recursion
print(optimize_btup(WV, 10000))

print("time:", timeit('optimize_btup(WV,10000)', setup='from __main__ import optimize_btup; from __main__ import WV', number=100))
