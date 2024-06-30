import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


class RRT:
    #initializare obiect rrt, bias = 0.1
    # step_size poate fi inlocuit, in functie de dificultatea hartii;
    # pentru harti nu foarte complexe, un step_size = 20 da rezultate destul de constante

    def __init__(self, start, goal, map_array, bias_prob=0.1, step_size=5):
        self.start = start
        self.goal = goal
        self.map_array = map_array
        self.tree = {}
        self.tree[start] = None
        self.bias_prob = bias_prob
        self.step_size = step_size

    def generate_random_point(self):
        if np.random.uniform(0, 1) < self.bias_prob:
            return self.goal
        else:
            x = np.random.randint(0, self.map_array.shape[1])
            y = np.random.randint(0, self.map_array.shape[0])
            return x, y

    def get_nearest_node(self, point):
        distances = np.linalg.norm(np.array(list(self.tree.keys())) - np.array(point), axis=1)
        #distanta euclidiana

        nearest_node = list(self.tree.keys())[np.argmin(distances)]
        return nearest_node

    def steer(self, from_node, to_node):
        direction = np.array(to_node) - np.array(from_node)
        distance = np.linalg.norm(direction)

        if distance > self.step_size:
            direction = direction / distance * self.step_size
        new_node = tuple(np.array(from_node) + direction.astype(int))
        return new_node

    def is_collision_free(self, from_node, to_node):
        line_points = self.bresenham_line(from_node, to_node)
        for point in line_points:
            if self.map_array[point[1], point[0]] != 255:
                return False
        return True

    # algoritm bresenham, pt a evita coliziuni, folosit mai sus
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

    #numarul maxim de pasi dat prin max_iter;
    # din nou, nr maxim de pasi poate fi schimbat in functie de dificultatea hartii,
    # pentru harti mai usoare ( cu mai putine obstacole, max_iter = 10000 ) ar trebui sa fie de ajuns
    def find_path(self, max_iter=10000):
        for _ in range(max_iter):
            # generare punct, gaseste cel mai apropiat nod si indreapta-te spre el
            random_point = self.generate_random_point()
            nearest_node = self.get_nearest_node(random_point)
            new_node = self.steer(nearest_node, random_point)

            # verifica coliziuni
            if self.is_collision_free(nearest_node, new_node):
                self.tree[new_node] = nearest_node
                # daca nu are coliziuni, adauga in arbore
                if np.linalg.norm(np.array(new_node) - np.array(self.goal)) < self.step_size:
                    # daca e goal, break
                    self.tree[self.goal] = new_node
                    break

    def plot_tree(self):
        plt.imshow(self.map_array, cmap="gray")
        for node in self.tree:
            if self.tree[node]:
                plt.plot([node[0], self.tree[node][0]], [node[1], self.tree[node][1]], "b", linewidth=1)

        plt.scatter(*self.start, color="green", label="Start")
        plt.scatter(*self.goal, color="red", label="Goal")
        # daca s-a ajuns la goal, acesta este in self.tree, si urmeaza nod cu nod
        # drumul de la goal inapoi la start.

        if self.goal in self.tree:
            path = []
            node = self.goal
            while node != self.start:
                path.append(node)
                node = self.tree[node]

            for i in range(len(path) - 1):
                plt.plot([path[i][0], path[i + 1][0]], [path[i][1], path[i + 1][1]], "r", linewidth=2)

        plt.legend()
        plt.show()

def choose_start_goal(event):
        if event.dblclick:
            x = int(event.xdata)
            y = int(event.ydata)

            if not plt.get_current_fig_manager().toolbar.mode:
                global start, goal
                if start is None:
                    start = (x, y)
                    plt.scatter(x, y, color="green", label="Start")
                    plt.draw()
                elif goal is None:
                    goal = (x, y)
                    plt.scatter(x, y, color="red", label="Goal")
                    plt.draw()

def main(nume_imagine):
        global start, goal
        start = None
        goal = None

        # Load the map image
        map_image = Image.open(nume_imagine).convert("L")
        map_array = np.array(map_image)

        #convertim imaginea in array

        fig = plt.figure()
        fig.canvas.mpl_connect("button_press_event", choose_start_goal)


        plt.imshow(map_array, cmap="gray")
        plt.axis("off")

        plt.show()

        if start is not None and goal is not None:
            # creaza obiect rrt
            rrt = RRT(start, goal, map_array, bias_prob=0.1, step_size=20)
            rrt.find_path()
            # gaseste drum
            # ploteaza arborele

            rrt.plot_tree()
        else:
            print("Start and/or goal position not selected.")

main("map4.png")
