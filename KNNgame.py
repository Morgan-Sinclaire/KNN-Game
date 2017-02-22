import numpy as np
import matplotlib.pyplot as plt

def dist(a,b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**.5


class Grid(object):
    def __init__(self, size, blues=[], reds=[], k=1):
        self.size = size
        self.blues = blues
        self.reds = reds

    def add(self, point, color):
        if color == "blue":
            self.blues.append(point)
        if color == "red":
            self.reds.append(point)

    def classify(self, point, k=1):
        nearest = []
        for p in self.blues:
            nearest.append((dist(point,p), 0))
        for p in self.reds:
            nearest.append((dist(point,p), 1))

        nearest = sorted(nearest)[:k]

        count = sum([n[1] for n in nearest])

        return count > k/2

    def score(self, k=1, n=100):
        count = 0

        s = self.size
        step = s / n

        space = np.linspace(.5*s / n, s - .5*s / n, n)
        for i in space:
            for j in space:
                count += self.classify((i,j), k)

        pct = round(100*(count/n**2), 2)

        if pct >= 50:
            return "Red wins with {}%".format(pct)
        else:
            return "Blue wins with {}%".format(100 - pct)

    def graph(self):
        if self.reds:
            plt.scatter(*zip(*self.reds), c='r')
        if self.blues:
            plt.scatter(*zip(*self.blues), c='b')
        plt.xlim(0,10)
        plt.ylim(0,10)
        plt.show()


def game(n=100, size=10, k=1):
    ply = int(input("Enter number of ply:\n"))

    g = Grid(size=size, k=k)

    for i in range(ply//2):
        g.graph()
        p = input("Red, place your point as x, y:\n")
        p = tuple(map(float, p.replace(",", " ").split()))
        g.reds.append(p)

        g.graph()
        p = input("Blue, place your point as x, y:\n")
        p = tuple(map(float, p.replace(",", " ").split()))
        g.blues.append(p)

    g.graph()

    return g.score(k, n)

print(game())
