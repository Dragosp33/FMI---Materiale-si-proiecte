import numpy as np
import matplotlib.pyplot as plt

# Define the potential field constants
k_att = 0.1
k_rep = 0.2
d_min = 1
k_collision = 1.0

# Define the simulation parameters
delta_t = 0.1
num_steps = 1000

# Generate random start positions for the agents
num_agents = 3
agent_positions = [np.random.rand(2) * 10.0 - 5.0 for _ in range(num_agents)]


# Define the goal position
p_goal = np.array([0.0, 0.0])

# Define the obstacle positions
obstacle_positions = [np.array([2.0, 2.0]), np.array([2.0, 1.0]), np.array([1.0, 1.0])]


def calculate_gradient(p, agent_index, agent_positions):
    grad_att = k_att * (p_goal - p)
    grad_rep = np.zeros_like(p)
    for obstacle_pos in obstacle_positions:
        d = np.linalg.norm(p - obstacle_pos)
        if d < d_min:
            grad_rep += k_rep * (1 / d - 1 / d_min) * ((p - obstacle_pos) / d)

    for j, agent_pos in enumerate(agent_positions):
        if j != agent_index:
            dij = np.linalg.norm(p - agent_pos)
            grad_collision = (np.abs(p - agent_pos) - dij ** 2)
            grad_collision = np.maximum(grad_collision, 0)  # Ensure non-negative values
            grad_rep += k_collision * grad_collision

    if np.linalg.norm(grad_att + grad_rep) < 1e-6:
        grad_perturb = np.random.randn(2) * 0.1
        return grad_perturb / np.linalg.norm(grad_perturb)

    return grad_att + grad_rep


# Initialize the states and trajectories for each agent
trajectories = [[] for _ in range(num_agents)]
for agent_index, p_start in enumerate(agent_positions):
    p = p_start
    trajectories[agent_index].append(p)

    for i in range(num_steps):
        u = calculate_gradient(p, agent_index, agent_positions)
        p = p + delta_t * u
        trajectories[agent_index].append(p)

# Plot the trajectories
for agent_index, trajectory in enumerate(trajectories):
    trajectory = np.array(trajectory)
    plt.plot(trajectory[:, 0], trajectory[:, 1])

# Plot the goal position, obstacle positions, and start positions
plt.plot(p_goal[0], p_goal[1], 'go')
for obstacle_pos in obstacle_positions:
    plt.plot(obstacle_pos[0], obstacle_pos[1], 'ro')
for agent_pos in agent_positions:
    plt.plot(agent_pos[0], agent_pos[1], 'bo')

plt.xlabel('x')
plt.ylabel('y')
plt.axis('equal')
plt.show()