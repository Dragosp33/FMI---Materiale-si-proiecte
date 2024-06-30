import numpy as np
import matplotlib.pyplot as plt

# Define the potential field constants
k_att = 0.1
k_rep = 1.0
d_min = 0.5
k_col = 1.0

# Define the simulation parameters
delta_t = 0.1
num_steps = 1000

# Generate random start positions for the leader and followers
#p_leader_start = np.random.rand(2) * 10.0 - 5.0
#p_follower_start = np.random.rand(2) * 10.0 - 5.0

p_leader_start = np.array([10.0, 10.0])
p_follower_start = np.array([10.0, 9.0])


# Define the goal position
p_goal = np.array([0.0, 0.0])

# Define the obstacle positions
obstacle_positions = [np.array([2.0, 2.0]), np.array([-3.0, 1.0]), np.array([1.0, -4.0])]


# Define a function to calculate the potential field gradient at a given position
def calculate_gradient(p, p_other=None):
    grad_att = k_att * (p_goal - p)
    grad_rep = np.zeros_like(p)
    for obstacle_pos in obstacle_positions:
        d = np.linalg.norm(p - obstacle_pos)
        if d < d_min:
            grad_rep += k_rep * (1 / d - 1 / d_min) * ((p - obstacle_pos) / d)
        if np.linalg.norm(grad_att + grad_rep) < 1e-6:
            grad_perturb = np.random.randn(2) * 0.1
            return grad_perturb / np.linalg.norm(grad_perturb)

    if p_other is not None:
        d_other = np.linalg.norm(p - p_other)
        if d_other < d_min:
            grad_col = k_col * (1 / d_other - 1 / d_min) * ((p - p_other) / d_other)
            return grad_att + grad_rep + grad_col

    return grad_att + grad_rep


# Initialize the leader and follower positions
p_leader = p_leader_start
p_follower = p_follower_start

# Initialize the trajectory arrays
leader_trajectory = [p_leader]
follower_trajectory = [p_follower]

# Run the simulation
for i in range(num_steps):
    # Calculate the potential field gradient for the leader
    u_leader = calculate_gradient(p_leader)

    # Update the leader position
    p_leader = p_leader + delta_t * u_leader

    # Append the new leader position to the trajectory array
    leader_trajectory.append(p_leader)

    # Calculate the potential field gradient for the follower
    u_follower = calculate_gradient(p_follower, p_leader)

    # Update the follower position
    p_follower = p_follower + delta_t * u_follower

    # Maintain a minimum distance between the leader and follower
    d_leader_follower = np.linalg.norm(p_leader - p_follower)
    if d_leader_follower < d_min:
        p_follower = p_leader + (p_follower - p_leader) / d_leader_follower * d_min

    # Append the new follower position to the trajectory array
    follower_trajectory.append(p_follower)

# Convert the trajectory arrays to numpy arrays
leader_trajectory = np.array(leader_trajectory)
follower_trajectory = np.array(follower_trajectory)


plt.plot(leader_trajectory[:,0], leader_trajectory[:,1], label='Leader')
plt.plot(follower_trajectory[:,0], follower_trajectory[:,1], label='Follower')
plt.plot(p_goal[0], p_goal[1], 'ro', label='Goal')
for obstacle_pos in obstacle_positions:
    plt.plot(obstacle_pos[0], obstacle_pos[1], 'ks', markersize=10, label='Obstacle')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('Leader-Followers System with Collision Avoidance')
plt.legend()
plt.show()