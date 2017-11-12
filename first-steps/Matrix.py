import numpy as np

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
