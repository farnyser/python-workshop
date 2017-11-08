import sys

from portage import os

def step_1():
    A = [1, 2, 3]
    B = A[::-1]

    for i in A:
        print(i)

    for i in B:
        print(i)

    h, w = map(int, sys.stdin.readline().split())
    print(h, w)

    input = map(int, os.read(0, 10000).split())

    for i in input:
        print(i)


def readarray(type):
    return list(map(type, sys.stdin.readline().split()))

def readmatrix(type, n):
    M=[]
    for _ in range(n):
        row = readarray(type)
        assert len(row) == n
        M.append(row)
    return M

def step_2():
    print("A:")
    A = readmatrix(int, 3)
    print("B:")
    B = readmatrix(int, 3)
    print("A==B?")

    res = 1
    for i in range(3):
        for j in range(3):
            if A[i][j] != B[i][j]:
                res = 0
                break
    print(res)

class SimpleQueue:
    def __init__(self):
        self.ins = []
        self.outs = []

    def __len__(self):
        return len(self.ins) + len(self.outs)

    def push(self, o):
        self.ins.append(o)

    def pop(self):
        if not self.outs:
            self.outs = self.ins[::-1]
            self.ins = []
        return self.outs.pop()

def step_3():
    q = SimpleQueue()
    q.push(1)
    q.push(3)
    q.push(7)

    while q:
        print(q.pop())

def step_4():
    a = max((i,i*2) for i in range(4))
    print(a)

    b = [(i,i*2,i*i) for i in range(4, -1, -1)]

    print(sorted(b, reverse=True)[0])
    print(sorted(b, reverse=False)[0])

def scalar_product(A,B):
    assert len(A) == len(B)
    return sum(A[i] * B[i] for i in range(len(A)))

def step_5():
    print(scalar_product([1,2,3], [2,4,6]))
    #print(scalar_product([1,2,3], [44]))

def fibo_recurs(n):
    if n <= 1:
        return n
    return fibo_recurs(n-1) + fibo_recurs(n - 2)

def fibo_recursk(n, k = None):
    if n <= 1:
        return n

    k2 = fibo_recursk(n - 2)
    if k == None:
        k = fibo_recursk(n-1, k2)

    return k + k2

def fibo_iter(n):
    k_2 = 0
    k_1 = 1
    if n <= 1:
        return n

    for i in range(1,n):
        k = k_2 + k_1
        k_2 = k_1
        k_1 = k

    return k

if __name__ == "__main__":
    print("Hello %s, the answer is %i !" % ("dude", 42))

    #step_1()
    #step_2()
    #step_3()
    #step_4()
    #step_5()

    print(fibo_recurs(35))
    print(fibo_recursk(35))
    print(fibo_iter(35))

    #print(fibo_recurs(55)) dead
    print(fibo_recursk(55))
    print(fibo_iter(55))

    #print(fibo_recurs(100)) dead
    #print(fibo_recursk(100)) dead
    print(fibo_iter(100))