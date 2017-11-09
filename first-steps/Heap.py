import random

from math import floor


class Heap:
    def __init__(self):
        self.data = []

    def __len__(self):
        return len(self.data)

    def push(self, value):
        self.data.append(value)
        self.up(len(self.data) - 1)

    def pop(self):
        root = self.data[0]
        self.data[0] = self.data[len(self) - 1]
        del self.data[len(self) - 1]
        if self:
            self.down(0)
        return root

    def up(self, i):
        x = self.data[i]

        while i >= 1 and self.data[i // 2] >= x:
            self.data[i] = self.data[i // 2]
            i //= 2
        self.data[i] = x

    def down(self, i):
        x = self.data[i]
        n = len(self)

        while True:
            left = 2 * i
            right = left + 1

            if right < n and self.data[right] < x and self.data[right] < self.data[left]:
                self.data[i] = self.data[right]
                i = right
            elif left < n and self.data[left] < x:
                self.data[i] = self.data[left]
                i = left
            else:
                self.data[i] = x
                return


if __name__ == '__main__':
    X = [floor(random.random() * 100) for i in range(0, 10)]
    H = Heap()

    for x in X:
        H.push(x)

    print(X)
    print(H.data)

    while H:
        print(H.pop())
