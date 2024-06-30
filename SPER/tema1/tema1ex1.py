import matplotlib.pyplot as plt
import numpy as np
import scipy
import math


def bezierPath(points):
    pathPoints = []
    for t in np.linspace(0, 1):
        pathPoints.append(z(t, points))
    return np.array(pathPoints)


def B(n, i, t):
    return scipy.special.comb(n, i) * t ** i * (1 - t) ** (n - i)


def z(t, points):
    n = len(points) - 1
    return np.sum([B(n, i, t) * points[i] for i in range(n + 1)], axis=0)

    
points = np.array([[-4, 3], [-2, 2], [-3, 0], [-1, -1], [1, -2], [3, -1], [4, 1], [2, 3]])
    
path = bezierPath(points)
    
graph = plt.subplot()
graph.plot(path.T[0], path.T[1],label="Bezier Path")
graph.plot(points.T[0], points.T[1],'--bo', label="Control Points")
graph.legend()
graph.grid(True)
plt.show()
