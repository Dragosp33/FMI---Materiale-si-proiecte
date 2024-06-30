
from casadi import *

import matplotlib.pyplot as plt
import numpy as np
import scipy
import math
import scipy.integrate as integrate

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

def integrand(x, bezier_i, bezier_j):
    return bezier_i * bezier_j

    
points = np.array([[-4, 3], [-2, 2], [-3, 0], [-1, -1], [1, -2], [3, -1], [4, 1], [2, 3]])
    
path = bezierPath(points)



solver = casadi.Opti()

numControlPoints = 3 * len(path[:])
p = solver.variable(2,numControlPoints)
t = np.linspace(0.01, 0.99, len(path[:]))

values = [B(numControlPoints, i, t[int(i//(numControlPoints/len(path[:]))):][0]) for i in range(numControlPoints)]
    
for i in range(numControlPoints):
    solver.subject_to(casadi.mtimes(p, values) == path[1,:].T)

cost = 0
for i in range(numControlPoints-1):
    for j in range(numControlPoints-1):
        bezier_i = B(numControlPoints-1, i, t[int(i//(numControlPoints/len(path[:]))):][0])
        bezier_j = B(numControlPoints-1, j, t[int(i//(numControlPoints/len(path[:]))):][0])
        cost += p[:,i] * p[:,j] * integrate.quad(integrand, 0, 1, args=(bezier_i, bezier_j))[0]
    
solver.minimize(cost[1,:])
solver.solver('ipopt')
solver.solve()

pValues = solver.value(p)
newPath = bezierPath(pValues.T)

ax = plt.subplot()
ax.plot(newPath.T[0], newPath.T[1], color='r', label="Bezier Path")
ax.plot(pValues[0], pValues[1],'--bo', label="Control Points")
ax.legend()
ax.grid(True)
plt.show()

