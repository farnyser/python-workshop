import random
from concurrent.futures import ThreadPoolExecutor

import numpy


class MapReduce:
    def __init__(self, mapper, reducer):
        self.mapper = mapper
        self.reducer = reducer
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.tasks = []

    def __map(self, input):
        return list(self.mapper(input))

    def __reduce(self, d):
        self.tasks = []
        for k in d:
            self.tasks.append(self.executor.submit(self.reducer, k, d[k]))

    def __shuffle_and_sort(self):
        d = {}
        for task in self.tasks:
            for r in task.result():
                if not r[0] in d:
                    d[r[0]] = []
                d[r[0]].append(r[1])
        return d

    def __result(self):
        d = {}
        for task in self.tasks:
            k,v = task.result()
            d[k] = v
        return d

    def add_data(self, input):
        self.tasks.append(self.executor.submit(self.__map, input))

    def get_result(self):
        d = self.__shuffle_and_sort()
        self.__reduce(d)
        return self.__result()


def mapper(input):
    for c in input:
        yield c.lower(), 1


def reducer(key, values):
    return key, numpy.sum(values)


if __name__ == '__main__':
    A = ['I', 'see', 'a', 'red', 'door', 'and', 'I', 'want', 'it', 'painted', 'black']
    MR = MapReduce(mapper, reducer)

    for i in range(10000):
        input = ''.join([A[random.randint(0,len(A)-1)] for i in range(25)])
        MR.add_data(input)

    print(MR.get_result())