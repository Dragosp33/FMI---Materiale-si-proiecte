
from casadi import *

import matplotlib.pyplot as plt
import numpy as np
import scipy
import math
import scipy.integrate as integrate
from more_itertools import pairwise

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

#ztPrim
pointsZtPrim = []
for succesive_points in pairwise(path):
    dx = succesive_points[1][0] - succesive_points[0][0]
    dy = succesive_points[1][1] - succesive_points[0][1]
    D = math.sqrt(dx ** 2 + dy ** 2)
    pointsZtPrim.append( succesive_points[1]-succesive_points[0] )


ztPrim = len(path)*bezierPath(np.array(pointsZtPrim))


graph = plt.subplot()
graph.plot(ztPrim, label="z(t) prim")
graph.legend()
graph.grid(True)
plt.show()
    
# uV(t)
uVt=[]
for succesive_points in pairwise(ztPrim):
    dx = succesive_points[1][0] - succesive_points[0][0] 
    dy = succesive_points[1][1] - succesive_points[0][1] 
    D = math.sqrt(dx ** 2 + dy ** 2)
    uVt.append(D)
    
    
graph = plt.subplot()
graph.plot(uVt, label="uV(t)")
graph.legend()
graph.grid(True)
plt.show()

# ztSecund
pointsZtSecund = []
for i in range(0, len(path)-2, 1):
    P = path[i+2]-2*path[i+1]+path[i]
    pointsZtSecund.append(P)
pointsZtSecund = np.array(pointsZtSecund)

 
ZtSecund = len(path)*(len(path)-1) * bezierPath(pointsZtSecund)


graph = plt.subplot()
graph.plot(ZtSecund, label="z(t) secund")
graph.legend()
graph.grid(True)
plt.show()

#uO(t)

L = 1
uOt = []
for i in range(len(path)):
    z1prim = ztPrim[i][0]
    z2prim = ztPrim[i][1]
    z1secund = ZtSecund[i][0]
    z2secund = ZtSecund[i][1]
    uOt.append(np.arctan( L*( (z2secund*z1prim - z2prim*z1secund) / ((z1prim**2 + z2prim**2)**(3/2)) )))
uOt = np.array(uOt)


graph = plt.subplot()
graph.plot(uOt, label="Uo(t)")
graph.legend()
graph.grid(True)
plt.show()

