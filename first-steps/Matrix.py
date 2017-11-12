from timeit import timeit

import numpy as np
from numpy import linalg as la


def dot(A, B):
    C = [[0 for i in range(len(A))] for j in range(len(A))]

    for row in range(len(A)):
        for col in range(len(A)):
            for a in range(len(B)):
                C[row][col] += A[row][a] * B[a][col]

    return C


def np_dot(A, B):
    a = np.array(A)
    b = np.array(B)

    return a.dot(b)


def power(A, k):
    assert (len(A) == len(A[0]))

    buffer = A
    for i in range(1,k):
        buffer = dot(buffer, A)

    return buffer

def power_exp(A, k):
    if k == 1:
        return A
    if k == 2:
        return dot(A,A)

    m = k % 2

    if m:
        return dot(A, power_exp(dot(A,A), k//2))

    return power_exp(dot(A,A), k//2)


def np_power_exp(A, k):
    if k == 1:
        return A
    if k == 2:
        return A.dot(A)

    m = k % 2

    if m:
        return A.dot(np_power_exp(A.dot(A), k//2))

    return np_power_exp(A.dot(A), k//2)


if __name__ == '__main__':
    A = [[1, 2, 0],
         [4, 3, -1]]
    B = [[5, 1],
         [2, 3],
         [3, 4]]

    C = dot(A, B)
    Cnp = np_dot(A, B)

    print(C)
    print(Cnp)

    print(power(C, 2))
    print(la.matrix_power(Cnp, 2))

    print(power(C, 3))
    print(la.matrix_power(Cnp, 3))

    print(power(C, 4))
    print(power_exp(C, 4))
    print(la.matrix_power(Cnp, 4))
    print(np_power_exp(Cnp, 4))

    print(power(C, 6))
    print(power_exp(C, 6))
    print(la.matrix_power(Cnp, 6))
    print(np_power_exp(Cnp, 6))

    print("naive method:", timeit('power(C,9)', number=10000,
                                  setup='from __main__ import power ; from __main__ import C'))
    print("naive fexp method:", timeit('power_exp(C,9)', number=10000,
                                  setup='from __main__ import power_exp ; from __main__ import C'))
    print("numpy method:", timeit('la.matrix_power(Cnp,9)',  number=10000,
                                  setup='from numpy import linalg as la; from __main__ import Cnp'))
    print("numpy fexp method:", timeit('np_power_exp(Cnp,9)',  number=10000,
                                  setup='from __main__ import np_power_exp; from __main__ import Cnp'))
