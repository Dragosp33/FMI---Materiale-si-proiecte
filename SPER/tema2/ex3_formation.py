import numpy as np
import matplotlib.pyplot as plt

# Constants
k_att = 0.1
k_rep = 0.1
d_min = 0.5
k_col = 0.1
k_form = 0.5  # Formation keeping constant
delta_t = 0.1  # Time step
max_iterations = 1000

# Function to calculate the gradient of the potential field at position p
def calculate_gradient(p, p_goal, obstacle_positions, p_other=None, relative_pos=None):
    grad_att = k_att * (p_goal - p)  # Attraction gradient
    grad_rep = np.zeros_like(p)  # Repulsion gradient
    grad_col = np.zeros_like(p)  # Collision avoidance gradient
    grad_form = np.zeros_like(p)  # Formation keeping gradient
    for obs_pos in obstacle_positions:
        diff = p - obs_pos
        dist = np.linalg.norm(diff)
        grad_rep += k_rep * (1/dist**3) * diff  # Repulsion gradient
        if dist < d_min:
            grad_col += k_col * ((1/dist) - (1/d_min)) * (diff / dist)  # Collision avoidance gradient
    if p_other is not None:
        diff = p - p_other
        dist = np.linalg.norm(diff)
        grad_col += k_col * ((1/dist) - (1/d_min)) * (diff / dist)  # Collision avoidance gradient
        if relative_pos is not None:
            grad_form += k_form * (p - (p_other + relative_pos))  # Formation keeping gradient
    return grad_att + grad_rep + grad_col + grad_form

# Initialize positions
p_leader = np.random.uniform(low=-20, high=20, size=(2,))
relative_pos = np.array([5.0, 0.0])  # Relative position of the follower with respect to the leader

p_goal = np.array([0.0, 0.0])
obstacle_positions = [np.array([-10.0, 0.0]), np.array([10.0, 0.0]), np.array([1.0, 1.0])]

# Initialize trajectories
leader_trajectory = np.zeros((max_iterations, 2))
follower_trajectory = np.zeros((max_iterations, 2))

# Simulation loop
for i in range(max_iterations):
    # Calculate gradients
    grad_leader = calculate_gradient(p_leader, p_goal, obstacle_positions, p_other=None, relative_pos=None)
    grad_follower = calculate_gradient(p_leader + relative_pos, p_goal, obstacle_positions, p_other=p_leader, relative_pos=relative_pos)

    # Update positions
    p_leader += delta_t * grad_leader
    p_follower = p_leader + relative_pos
    p_follower += delta_t * grad_follower

    # Maintain minimum distance between agents
    diff = p_follower - p_leader
    dist = np.linalg.norm(diff)
    if dist < d_min:
        p_follower = p_leader + (diff / dist) * d_min

    # Save positions to trajectories
    leader_trajectory[i] = p_leader
    follower_trajectory[i] = p_follower

    # Check if goal is reached
    if np.linalg.norm(p_follower - p_goal) < 0.5:
        print(f"Follower reached goal in {i} iterations!")
        break

# Plot the trajectories
plt.plot(leader_trajectory[:,0], leader_trajectory[:,1], label=' Leader')
plt.plot(follower_trajectory[:,0], follower_trajectory[:,1], label='Follower')
plt.plot(p_goal[0], p_goal[1], 'ro', label='Goal')
for obstacle_pos in obstacle_positions:
    plt.plot(obstacle_pos[0], obstacle_pos[1], 'ks', markersize=10, label='Obstacle')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('Leader-Follower System with Formation Keeping, Collision Avoidance, and Distance Maintenance')
plt.legend()
plt.show()