import sys
import copy

N = int(sys.stdin.readline())
Towers = [[N - i for i in range(N)], [], []]

visited = {}


def is_valid(T):
    for i in range(3):
        for j in range(1, len(T[i])):
            if T[i][j - 1] < T[i][j]:
                return False
    return True


def m(T, frm, to, act):
    TT = copy.deepcopy(T)
    if TT[frm]:
        TT[to].append(TT[frm].pop())
        return TT, appret(act,
                          "Move ring " + str(TT[to][0]) + " from " + ['A', 'B', 'C'][frm] + " to " + ['A', 'B', 'C'][
                              to])
    return TT, act


def appret(T, x):
    r = T[:]
    r.append(x)
    return r


def sel(x, y):
    if x and y:
        if len(x) < len(y):
            return x
        else:
            return y
    if x:
        return x
    else:
        return y


def make_key(T):
    return ':'.join(map(str, T[0])), ':'.join(map(str, T[1])), ':'.join(map(str, T[2]))


def run(x):
    T = x[0]
    actions = x[1]

    k = make_key(T)

    if k in visited:
        if len(actions) >= visited[k]:
            return []

    visited[k] = len(actions)
    if not is_valid(T):
        return []
    if not T[0] and not T[2]:
        return actions

    a = run(m(T, 0, 1, actions))
    f = run(m(T, 0, 2, actions))
    b = run(m(T, 1, 0, actions))
    c = run(m(T, 1, 2, actions))
    d = run(m(T, 2, 1, actions))
    e = run(m(T, 2, 0, actions))

    return sel(a, sel(b, sel(c, sel(d, sel(e, f)))))


sys.setrecursionlimit(10000)

actions = run((Towers, []))
for a in actions:
    print(a)