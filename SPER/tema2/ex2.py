import numpy as np
import matplotlib.pyplot as plt

# Define the potential field constants
k_att = 0.1
k_rep = 1.0
d_min = 0.5

# Define the simulation parameters
delta_t = 0.1
num_steps = 1000

# Generate a random start position
#p_start = np.random.rand(2) * 10.0 - 5.0

p_start = np.array([10.0, 10.0])

# Define the goal position
p_goal = np.array([0.0, 0.0])

# Define the obstacle positions
obstacle_positions = [np.array([2.0, 2.0]), np.array([2.0, 1.0]), np.array([1.0, 1.0])]


# calculeaza gradientul campului potential pt fiecare punct
def calculate_gradient(p):
    grad_att = k_att * (p_goal - p)
    grad_rep = np.zeros_like(p)
    for obstacle_pos in obstacle_positions:
        d = np.linalg.norm(p - obstacle_pos)
        if d < d_min:
            grad_rep += k_rep * (1 / d - 1 / d_min) * ((p - obstacle_pos) / d)

    # random perturbation pt gradient daca e prea mic
    if np.linalg.norm(grad_att + grad_rep) < 1e-6:
        grad_perturb = np.random.randn(2) * 0.1
        return grad_perturb / np.linalg.norm(grad_perturb)

    return grad_att + grad_rep


# Initialize the state
p = p_start

# Initialize the trajectory array
trajectory = [p]

# Run the simulation
for i in range(num_steps):
    # Calculate the potential field gradient at the current position
    u = calculate_gradient(p)

    # Update the position
    p = p + delta_t * u

    # Append the new position to the trajectory array
    trajectory.append(p)

# Plot the trajectory
trajectory = np.array(trajectory)
plt.plot(trajectory[:, 0], trajectory[:, 1])
plt.plot(p_goal[0], p_goal[1], 'go')
for obstacle_pos in obstacle_positions:
    plt.plot(obstacle_pos[0], obstacle_pos[1], 'ro')
plt.xlabel('x')
plt.ylabel('y')
plt.axis('equal')
plt.show()