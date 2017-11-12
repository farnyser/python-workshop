import random


class ReservoirSample:
    def __init__(self, size):
        self.maximum_size = size
        self.count = 0
        self.samples = []

    def __len__(self):
        return len(self.samples)

    def append(self, x):
        self.count += 1
        probability = self.maximum_size / self.count
        t = random.random()
        if t < probability:
            if len(self) < self.maximum_size:
                self.samples.append(x)
            else:
                self.samples[random.randint(0,self.maximum_size-1)] = x

    def __getitem__(self, item):
        return self.samples[item]


class WeightedReservoirSample:
    def __init__(self, size):
        self.maximum_size = size
        self.weight = 0
        self.samples = []

    def __len__(self):
        return len(self.samples)

    def append(self, x, w):
        self.weight += w / (1+len(self))
        if len(self) < self.maximum_size:
            self.samples.append(x)
            return

        probability = w / self.weight
        t = random.random()
        if t < probability:
            self.samples[random.randint(0,self.maximum_size-1)] = x

    def __getitem__(self, item):
        return self.samples[item]


if __name__ == '__main__':
    S = ReservoirSample(10)

    for x in range(1000000):
        input = random.randint(0,1000)
        S.append(input)

    for x in S:
        print(x)


    print("---")

    WS = WeightedReservoirSample(10)

    for x in range(1000000):
        input = random.randint(0,1000)
        WS.append(input, 100*(input % 2) + 1)

    for x in WS:
        print(x)