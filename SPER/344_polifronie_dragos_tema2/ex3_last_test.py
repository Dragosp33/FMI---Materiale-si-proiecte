import numpy as np
import matplotlib.pyplot as plt

# Define the potential field constants
k_att = 0.1
k_rep = 1.0
d_min = 0.5

# Define the simulation parameters
delta_t = 0.1
num_steps = 1000

# Generate random start positions for leader and followers
p_start_leader = np.array([10.0, 10.0])
p_start_follower1 = np.array([11.0, 10.0])
p_start_follower2 = np.array([10.5, 11.0])

# Define the goal position
p_goal = np.array([0.0, 0.0])

# Define the obstacle positions
obstacle_positions = [np.array([2.0, 2.0]), np.array([2.0, 1.0]), np.array([1.0, 1.0])]


# Define a function to calculate the potential field gradient at a given position
def calculate_gradient(p, leader_pos=None):
    grad_att = k_att * (p_goal - p)
    grad_rep = np.zeros_like(p)

    # Calculate the repulsion gradient for obstacles
    for obstacle_pos in obstacle_positions:
        d = np.linalg.norm(p - obstacle_pos)
        if d < d_min:
            grad_rep += k_rep * (1 / d - 1 / d_min) * ((p - obstacle_pos) / d)

    # Calculate the repulsion gradient for other agents
    if leader_pos is not None:
        d_leader = np.linalg.norm(p - leader_pos)
        if d_leader < d_min:
            grad_rep += k_rep * (1 / d_leader - 1 / d_min) * ((p - leader_pos) / d_leader)

    # Add a random perturbation to the gradient if it is very small
    if np.linalg.norm(grad_att + grad_rep) < 1e-6:
        grad_perturb = np.random.randn(2) * 0.1
        return grad_perturb / np.linalg.norm(grad_perturb)

    return grad_att + grad_rep


# Initialize the states
p_leader = p_start_leader
p_follower1 = p_start_follower1
p_follower2 = p_start_follower2

# Initialize the trajectories array
trajectory_leader = [p_leader]
trajectory_follower1 = [p_follower1]
trajectory_follower2 = [p_follower2]

# Run the simulation
for i in range(num_steps):
    # Calculate the potential field gradients at the current positions
    u_leader = calculate_gradient(p_leader)
    u_follower1 = calculate_gradient(p_follower1, leader_pos=p_leader)
    u_follower2 = calculate_gradient(p_follower2, leader_pos=p_leader)

    # Update the positions
    p_leader = p_leader + delta_t * u_leader
    p_follower1 = p_follower1 + delta_t * u_follower1
    p_follower2 = p_follower2 + delta_t * u_follower2

    # Append the new positions to the trajectories array
    trajectory_leader.append(p_leader)
    trajectory_follower1.append(p_follower1)
    trajectory_follower2.append(p_follower2)

# Plot the trajectories
trajectory_leader = np.array(trajectory_leader)
trajectory_follower1 = np.array(trajectory_follower1)
trajectory_follower2 = np.array(trajectory_follower2)


plt.plot(trajectory_leader[:, 0], trajectory_leader[:, 1], label='Leader')
plt.plot(trajectory_follower1[:, 0], trajectory_follower1[:, 1], label='Follower 1')
plt.plot(trajectory_follower2[:, 0], trajectory_follower2[:, 1], label='Follower 2')

plt.plot(p_goal[0], p_goal[1], 'go')
for obstacle_pos in obstacle_positions:
    plt.plot(obstacle_pos[0], obstacle_pos[1], 'ro')

plt.xlabel('x')
plt.ylabel('y')
plt.axis('equal')
plt.legend()
plt.show()