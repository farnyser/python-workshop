import random
from collections import deque


class Node:
    def __init__(self, v):
        self.left = None
        self.right = None
        self.value = v

    def push(self, v):
        if v < self.value:
            if self.left is None:
                self.left = Node(v)
            else:
                self.left.push(v)
        else:
            if self.right is None:
                self.right = Node(v)
            else:
                self.right.push(v)

    def visit(self, f):
        if self.left is not None:
            self.left.visit(f)
        f(self.value)
        if self.right is not None:
            self.right.visit(f)

    def dfs(self, f):
        s = [self]

        while s:
            node = s.pop()
            if node is None:
                continue
            print(" > ", node.value)
            if f(node.value):
                return node
            s.append(node.left)
            s.append(node.right)

    def bfs(self, f):
        q = deque()
        q.append(self)

        while q:
            node = q.popleft()
            if node is None:
                continue
            print(" - ", node.value)
            if f(node.value):
                return node
            q.append(node.left)
            q.append(node.right)


if __name__ == '__main__':

    data = [i for i in range(1, 10)]
    random.shuffle(data)

    print(data)

    root = Node(data[0])
    for i in data[1:]:
        root.push(i)

    root.visit(print)

    print(root.dfs(lambda x: x == 3).value)
    print(root.bfs(lambda x: x == 3).value)