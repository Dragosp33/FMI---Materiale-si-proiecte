import numpy as np
import matplotlib.pyplot as plt

# Define the workspace limits
x_min, x_max = -10, 10
y_min, y_max = -10, 10

# Define the robot and goal positions
p_robot = np.array([0, 0])
p_goal = np.array([8, 8])

# Define the obstacle positions
p_obstacles = np.array([
    [2, 2],
    [-3, 5],
    [-7, -5],
    [10, 2],
    [3, 3],
    [2, 3],
    [3, 2]
])

# Define the constants
k_att = 1.0
k_rep = 10.0
R = 1.0

# Define the grid
n_points = 100
x_grid = np.linspace(x_min, x_max, n_points)
y_grid = np.linspace(y_min, y_max, n_points)
X, Y = np.meshgrid(x_grid, y_grid)

# camp potential pt fiecare punct
Z = np.zeros((n_points, n_points))
for i in range(n_points):
    for j in range(n_points):
        p = np.array([X[i,j], Y[i,j]])
        att = 0.5 * k_att * np.linalg.norm(p - p_goal)**2
        rep = 0.0
        for k in range(len(p_obstacles)):
            d = np.linalg.norm(p - p_obstacles[k])
            if d < R:
                rep += 0.5 * k_rep * (1/d - 1/R) ** 2
                Z[i, j] = att + rep




plt.imshow(Z, extent=[x_min, x_max, y_min, y_max], origin='lower', cmap='binary')
plt.colorbar()
plt.plot(p_robot[0], p_robot[1], 'bo', label='robot')
plt.plot(p_goal[0], p_goal[1], 'go', label='goal')
for k in range(len(p_obstacles)):
    plt.plot(p_obstacles[k,0], p_obstacles[k,1], 'ro', label=f'obstacle {k+1}')
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Potential Field')
plt.show()

"""




fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_aspect('equal')
ax.set_xlabel('X')
ax.set_ylabel('Y')
c = ax.pcolormesh(X, Y, Z, cmap='coolwarm', shading='auto')
fig.colorbar(c, ax=ax)
ax.plot(p_robot[0], p_robot[1], 'bo', markersize=10)
ax.plot(p_goal[0], p_goal[1], 'go', markersize=10)
for i in range(len(p_obstacles)):
    ax.plot(p_obstacles[i,0], p_obstacles[i,1], 'ro', markersize=10)

plt.show()
"""

