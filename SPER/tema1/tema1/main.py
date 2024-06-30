import dubins
import math
import numpy as np
import matplotlib.pyplot as plt

# Define the four control points
x0, y0, a0 = 0, 0, math.pi/4
x1, y1, a1 = 1, 2, math.pi/3
x2, y2, a2 = 3, 3, math.pi/2
x3, y3, a3 = 5, 1, math.pi/6

# Define the start and end points
start = (x0, y0, a0)
end = (x3, y3, a3)

# Compute the Dubins path
path = dubins.shortest_path(start, end, 1.0)

# Compute the Bezier control points for each segment of the Dubins path
L, S, R = path.segments
QL = dubins.path_sample(L, 0.1)[0]
QR = dubins.path_sample(R, 0.1)[0]
QS = dubins.path_sample(S, 0.1)[0]
Q0 = (x0, y0)
Q3 = (x3, y3)

# Compute the Bezier control points for the left turn segment
t1 = math.atan2(QL[1]-Q0[1], QL[0]-Q0[0])
t2 = math.atan2(QR[1]-QS[1], QR[0]-QS[0])
P1 = (Q0[0]+math.cos(t1), Q0[1]+math.sin(t1), a0)
P2 = (QL[0]-math.cos(t1), QL[1]-math.sin(t1), t1)
P3 = (QR[0]+math.cos(t2), QR[1]+math.sin(t2), t2)

# Compute the Bezier control points for the straight segment
P4 = ((Q1[0]+Q2[0])/2, (Q1[1]+Q2[1])/2, S.psi)

# Compute the Bezier control points for the right turn segment
t3 = math.atan2(QS[1]-QR[1], QS[0]-QR[0])
t4 = math.atan2(Q3[1]-Q2[1], Q3[0]-Q2[0])
P5 = (QS[0]-math.cos(t3), QS[1]-math.sin(t3), t3)
P6 = (Q3[0]+math.cos(t4), Q3[1]+math.sin(t4), a3)

# Compute the Bezier curve for each segment of the Dubins path
t = np.linspace(0, 1, 100)
B1 = np.array([(1-t)**3*P1[0] + 3*t*(1-t)**2*P2[0] + 3*t**2*(1-t)*P3[0] + t**3*QL[0],
               (1-t)**3*P1[1] + 3*t*(1-t)**2*P2[1] + 3*t**2*(1-t)*P3[1] + t**3*QL[1],
               (1-t)**3*P1[2] + 3*t*(1-t)**2*P2[2] + 3*t**2*(1-t)*P3[2] + t**3*a0])
B2 = np.array([(1-t)**3*QL[0] + 3*t*(1-t)**2*P4[0] + t**3*QR[0],
               (1-t)**3*QL[1] + 3*t*(1-t)**2*P4[1] + t**3*QR[1],
               S.psi*np.ones_like(t)])
B3 = np.array([(1-t)**3*QR[0] + 3*t*(1-t)**2*P5[0] + 3*t**2*(1-t)*P6[0] + t**3*Q3[0],
               (1-t)**3*QR[1] + 3*t*(1-t)**2*P5[1] + 3*t**2*(1-t)*P6[1] + t**3*Q3[1],
               (1-t)**3*QR[2] + 3*t*(1-t)**2*P5[2] + 3*t**2*(1-t)*P6[2] + t**3*a3])

# Plot the Dubins path using Bezier curves
fig, ax = plt.subplots()
ax.plot([x0, Q1[0], QL[0], QR[0], Q2[0], QS[0], Q3[0]], [y0, Q1[1], QL[1], QR[1], Q2[1], QS[1], Q3[1]], 'bo--', label='Dubins path')
ax.plot(B1[0], B1[1], 'r-', label='Left turn')
ax.plot(B2[0], B2[1], 'g-', label='Straight')
ax.plot(B3[0], B3[1], 'b-', label='Right turn')
ax.legend()
ax.axis('equal')
plt.show()