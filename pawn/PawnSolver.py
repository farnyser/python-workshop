# Constraints
import random

if __name__ != '__main__':
    exit(1)

# Hardcoded test problem
# n = 4
# m = 2
# colors = [0, 0, 1, 1]
#
# # (xMin, xMax, yMin, yMax)
# bounds = [(10, 20, 80, 90),
#           (15, 30, 90, 100),
#           (20, 40, 92, 110),
#           (18, 20, 96, 103)]
#
# # (a, b, dist)
# distance = [(0, 1, 20),
#             (0, 2, 5)]

# generate random problem
n = 100
m = 50
colors = []
bounds = []
distance = []
span = 1000
distmax = 1000000
mapsize = 1000000

for i in range(n):
    colors.append(random.randint(0, 1))
    w = random.randint(1, span)
    h = random.randint(1, span)
    x = random.randint(0, mapsize - w)
    y = random.randint(0, mapsize - h)
    bounds.append((x, x+w, y, y+h))
for i in range(m):
    a = random.randint(0, n-1)
    b = random.randint(0, n-1)
    if a == b:
        b = (a+1) % (n - 1)
    d = random.randint(0, distmax)
    distance.append((a, b, d))

# print(colors)
# print(bounds)
# print(distance)


def set_color(p, x, c):
    s = len(p)
    cc = p[x]

    if cc < 0:
        p[x] = c
    elif cc != c:
        for i in range(s):
            if p[i] == cc:
                p[i] = c

    return p[x]


def in_rectangle(p, r):
    return r[0] <= p[0] <= r[1] and r[2] <= p[1] <= r[3]


def is_color(p, c):
    return ((p[0] + p[1]) % 2) == c


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def distance_min(d, pos, offx, offy, rect):
    h = len(rect)
    w = len(rect[0])
    if dist((w/2 + offx, h/2 + offy), pos) > d + 2 * max(w, h):
        return 0

    for y in range(len(rect)):
        for x in range(len(rect[y])):
            if rect[y][x] != 1:
                continue
            p = (x + offx, y + offy)
            dd = abs(p[0] - pos[0]) + abs(p[1] - pos[1])
            if dd <= d:
                return 1
    return 0


print("Trying to find position for %d pawns" % n)

pawn = {}
positions = {}
rect = {}
groups = {}

# Initialize
for i in range(n):
    pawn[i] = -1
    positions[i] = -1

print("Filter by color..")

for i in range(n):
    w = bounds[i][1] - bounds[i][0]
    h = bounds[i][3] - bounds[i][2]
    rect[i] = [[1] * w for i in range(h)]
    for x in range(w):
        for y in range(h):
            rect[i][y][x] = is_color((bounds[i][0]+x, bounds[i][2]+y), colors[i])

# Simplify distance constraints (if two constaints on the same pair, keep smallest only)
toRemove = set()
for d in distance:
    for dd in distance:
        if (d[0] == dd[0] and d[1] == dd[1]) or (d[0] == dd[1] and d[1] == dd[0]):
            if d == dd:
                continue
            elif d[2] <= dd[2]:
                toRemove.add(dd)
            else:
                toRemove.add(d)
for d in toRemove:
    distance.remove(d)
print("Removed => %d constraint(s) - because they were useless" % len(toRemove))
m = len(distance)

# Find subgroups
for i in range(m):
    a = distance[i][0]
    b = distance[i][1]
    c = set_color(pawn, a, i)
    set_color(pawn, b, c)

for i in range(n):
    if not pawn[i] in groups:
        groups[pawn[i]] = []
    groups[pawn[i]].append(i)

print("Groups (independent pawns) count =>", len(groups))

# handle unconstrained pawn first
for i in range(n):
    if pawn[i] == -1:
        positions[i] = (bounds[i][0], bounds[i][2])

        if not is_color(positions[i], colors[i]):
            if in_rectangle((positions[i][0], positions[i][1] + 1), bounds[i]):
                positions[i] = (positions[i][0], positions[i][1] + 1)
            elif in_rectangle((positions[i][0] + 1, positions[i][1]), bounds[i]):
                positions[i] = (positions[i][0] + 1, positions[i][1])
            else:
                positions[i] = -2


# handle constrained pawns ...

for g in groups:
    if g <= 0:
        continue
    gc = groups[g]
    print("Working on group =>", gc)
    if len(gc) >= 10:
        print(" -> hiding composition because there is too many pawns in there")
    else:
        for p in gc:
            print(" - pawn ", p, "=>", bounds[p])

    changed = 1
    while changed > 0:
        changed = 0
        for p in gc:
            # print(" p =>", p)
            for dc in distance:
                a = dc[0]
                b = dc[1]
                d = dc[2]
                if a != p:
                    continue

                if len(gc) < 10:
                    print(" -> working on constraint on pawn:%d and pawn:%d with dist max = %d" % (a, b, d))

                sum = 0
                for y in range(len(rect[a])):
                    for x in range(len(rect[a][y])):
                        if rect[a][y][x] == 1:
                            pos = (x + bounds[a][0], y + bounds[a][2])
                            rect[a][y][x] = distance_min(d, pos, bounds[b][0], bounds[b][2], rect[b])
                            changed = changed or rect[a][y][x] != 1
                            sum += rect[a][y][x]
                if sum == 0:
                    print("Constraint impossible for pawn/pawn : %d/%d and dist %d " % (a, b, d))
                    print("a => ", bounds[a])
                    print("b => ", bounds[b])
                    exit(-1)
    for p in gc:
        offx = bounds[p][0]
        offy = bounds[p][2]
        for y in range(len(rect[p])):
            for x in range(len(rect[p][y])):
                if rect[p][y][x] == 1:
                    positions[p] = (x + offx, y + offy)
                    break


print("Solution found !")
print("Positions =>", positions)