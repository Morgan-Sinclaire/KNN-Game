import numpy as np
import matplotlib.pyplot as plt

def dist(a,b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**.5


class Grid(object):
    """
    10 x 10 grid with red and blue points. Can classify new points
    using the K-Nearest Neighbors algorithm, typically with k = 1. Also
    approximates the area swept by each color, with higher n giving
    greater accuracy.
    """
    def __init__(self, reds=[], blues=[], k=1, size=10, n=100):
        self.reds = reds
        self.blues = blues
        self.k = k
        self.size = size
        self.n = n

    def add(self, point, color):
        """Add a point to the grid of a given color."""
        if color == "red":
            self.reds.append(point)
        if color == "blue":
            self.blues.append(point)

    def classify(self, point):
        """
        Given a point and a grid with red and blue points, classify
        it from a vote of its K-Nearest Neighbors.
        """
        nearest = []
        for p in self.reds:
            nearest.append((dist(point,p), 1))
        for p in self.blues:
            nearest.append((dist(point,p), 0))

        nearest = sorted(nearest)[:self.k]

        count = sum([n[1] for n in nearest])

        return count > self.k / 2

    def score(self):
        """
        Given a grid occupied by red and blue points, approximate the
        area KNN-covered by each color, using n x n evenly spaced
        gridpoints. Print the color with more area.
        """
        count = 0
        n = self.n
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
        """Given a grid with red and blue points, make a scatterplot."""
        if self.reds:
            plt.scatter(*zip(*self.reds), c='r')
        if self.blues:
            plt.scatter(*zip(*self.blues), c='b')
        plt.xlim(0,10)
        plt.ylim(0,10)
        plt.show()
