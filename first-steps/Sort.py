def mergesort(t, s=0, e=None):
    if e is None:
        e = len(t)
    if e - s <= 1:
        return [t[s]]

    k = s + round((e - s) / 2)

    a = mergesort(t, s, k)
    b = mergesort(t, k, e)
    r = []

    i = 0
    j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            r.append(a[i])
            i += 1
        else:
            r.append(b[j])
            j += 1
    while i < len(a):
        r.append(a[i])
        i += 1
    while j < len(b):
        r.append(b[j])
        j += 1

    return r


def quicksort(A, lo=0, hi=None):
    if hi is None:
        hi = len(A) - 1

    if lo < hi:
        p = partition(A, lo, hi)
        quicksort(A, lo, p)
        quicksort(A, p + 1, hi)


def partition(A, lo, hi):
    pivot = A[lo]
    i = lo - 1
    j = hi + 1

    while True:
        i += 1
        j -= 1

        while A[i] < pivot:
            i += 1

        while A[j] > pivot:
            j -= 1

        if i >= j:
            return j

        tmp = A[i]
        A[i] = A[j]
        A[j] = tmp

def bucketsort(A):
    min = max = None
    buckets = [[] for i in range(10)]

    for x in A:
        if min is None or x < min:
            min = x
        if max is None or x > max:
            max = x

    if min == max:
        return A

    inter = (max-min)/10

    for x in A:
        for i in range(10):
            if x <= min+(i+1)*inter:
                buckets[i].append(x)
                break

    result = []
    for b in buckets:
        bs = bucketsort(b)
        result.extend(bs)

    return result

if __name__ == '__main__':
    X = [1, 4, 9, 1, 2, 0, 7, 3, 7, 9, 10, 23, 93, 1, 32, 4, 46]
    Y = [4, 5, 3, 2, 3, 5, 4]

    pSorted = sorted(X)
    mSorted = mergesort(X)
    bSorted = bucketsort(X)
    qSorted = X[:]
    quicksort(qSorted)

    print("original:", X)
    print(pSorted)
    print(mSorted)
    print(qSorted)
    print(bSorted)

    pSorted = sorted(Y)
    mSorted = mergesort(Y)
    bSorted = bucketsort(Y)
    qSorted = Y[:]
    quicksort(qSorted)

    print("original:", Y)
    print(pSorted)
    print(mSorted)
    print(qSorted)
    print(bSorted)
