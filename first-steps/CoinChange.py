from timeit import timeit


def best_change(N, coins):
    cache = {0: []}
    for n in range(N + 1):
        for c in coins:
            if n - c not in cache:
                continue
            k = len(cache[n - c]) + 1
            if n not in cache or k < len(cache[n]):
                cache[n] = list(cache[n - c])
                cache[n].append(c)
    return cache[N]


def key(k, l):
    return ':'.join(map(str, sorted(l)))


def possible_change_count(N, coins):
    cache = {0: {'_': []}}
    for n in range(N + 1):
        for c in coins:
            if n - c not in cache:
                continue
            if n not in cache:
                cache[n] = {}
            for k in cache[n - c]:
                l = list(cache[n - c][k])
                l.append(c)
                cache[n][key(k,l)] = l
    return len(cache[N].values())


def possible_change_count2(N, coins, m = None, cache = {}):
    if m is None:
        m = len(coins)

    if N == 0:
        return 1
    if N < 0 or m <= 0:
        return 0
    if (N,m) in cache:
        return cache[(N,m)]

    a = possible_change_count2(N, coins, m - 1)
    b = possible_change_count2(N - coins[m - 1], coins, m)
    cache[(N,m)] = a + b
    return a + b

print(best_change(7, [2, 5]))
print(best_change(17, [2, 5]))
print(best_change(7, [1, 2, 5]))
print(best_change(10, [1, 2, 5]))
print(best_change(17, [1, 2, 5]))
print(best_change(17, [1, 2, 5, 10, 20, 50, 100, 200]))
print(best_change(635, [1, 2, 5, 10, 20, 50, 100, 200]))
print(best_change(17, [1, 2, 5, 10, 15, 20, 50, 100, 200]))
print(best_change(6, [1, 3, 4, 10]))

print(possible_change_count(6, [1, 3, 4, 10]))
print(possible_change_count(50, [1, 3, 4, 10]))
#print(possible_change_count(635, [1, 2, 5, 10, 20, 50, 100, 200]))

print(possible_change_count2(6, [1, 3, 4, 10]))
print(possible_change_count2(50, [1, 3, 4, 10]))
print(possible_change_count2(635, [1, 2, 5, 10, 20, 50, 100, 200]))

print("meth1: ", timeit('possible_change_count(50, [1, 3, 4, 10])', setup='from __main__ import possible_change_count', number=100))
print("meth2: ", timeit('possible_change_count2(50, [1, 3, 4, 10])', setup='from __main__ import possible_change_count2', number=100))