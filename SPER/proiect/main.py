import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Load the map image
map_image = Image.open("map1.png").convert("L")
map_array = np.array(map_image)

# Define the start and goal points
start = (50, 50)
goal = (350, 350)

# RRT algorithm implementation
class RRT:
    def __init__(self, start, goal, map_array):
        self.start = start
        self.goal = goal
        self.map_array = map_array
        self.tree = {}
        self.tree[start] = None

    def generate_random_point(self):
        x = np.random.randint(0, self.map_array.shape[1])
        y = np.random.randint(0, self.map_array.shape[0])
        return x, y

    def get_nearest_node(self, point):
        distances = np.linalg.norm(np.array(list(self.tree.keys())) - np.array(point), axis=1)
        nearest_node = list(self.tree.keys())[np.argmin(distances)]
        return nearest_node

    def steer(self, from_node, to_node, step_size):
        direction = np.array(to_node) - np.array(from_node)
        distance = np.linalg.norm(direction)
        if distance > step_size:
            direction = direction / distance * step_size
        new_node = tuple(np.array(from_node) + direction.astype(int))
        return new_node

    def is_collision_free(self, from_node, to_node):
        line_points = self.bresenham_line(from_node, to_node)
        for point in line_points:
            if self.map_array[point[1], point[0]] != 255:
                return False
        return True

    def bresenham_line(self, from_node, to_node):
        x0, y0 = from_node
        x1, y1 = to_node
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        line_points = []
        err = dx - dy

        while True:
            line_points.append((x0, y0))
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
        return line_points

    def find_path(self, max_iter=1000, step_size=10):
        for _ in range(max_iter):
            random_point = self.generate_random_point()
            nearest_node = self.get_nearest_node(random_point)
            new_node = self.steer(nearest_node, random_point, step_size)

            if self.is_collision_free(nearest_node, new_node):
                self.tree[new_node] = nearest_node
                if np.linalg.norm(np.array(new_node) - np.array(self.goal)) < step_size:
                    self.tree[self.goal] = new_node
                    break

    def plot_tree(self):
        plt.imshow(self.map_array, cmap="gray")
        for node in self.tree:
            if self.tree[node]:
                plt.plot([node[0], self.tree[node][0]], [node[1], self.tree[node][1]], "b", linewidth=1)
        plt.scatter(*self.start, color="green", label="Start")
        plt.scatter(*self.goal, color="red", label="Goal")

        path = []
        node = self.goal
        while node != self.start:
            path.append(node)
            node = self.tree[node]

        for i in range(len(path) - 1):
            plt.plot([path[i][0], path[i + 1][0]], [path[i][1], path[i + 1][1]], "r", linewidth=2)

        plt.legend()
        plt.show()


map_image = Image.open("map1.png").convert("L")

map_array = np.array(map_image)

start = (50, 50)

goal = (250, 250)

# Create an instance of RRT and find the path
rrt = RRT(start, goal, map_array)
rrt.find_path()

# Plot the resulting path
rrt.plot_tree()
