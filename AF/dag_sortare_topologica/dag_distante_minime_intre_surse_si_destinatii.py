# surse multiple,
# destinatii multiple
# distante dintre multimi

from collections import defaultdict

class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.adjacency_list = defaultdict(list)

    def add_edge(self, u, v, weight):
        self.adjacency_list[u].append((v, weight))

    def topological_sort(self):
        visited = [False] * self.vertices
        stack = []

        def dfs(vertex):
            visited[vertex] = True

            for neighbor, _ in self.adjacency_list[vertex]:
                if not visited[neighbor]:
                    dfs(neighbor)

            stack.append(vertex)

        for vertex in range(self.vertices):
            if not visited[vertex]:
                dfs(vertex)

        stack.reverse()
        return stack

    def min_distance_dag(self, sources, destinations):
        topological_order = self.topological_sort()
        distance = [float('inf')] * self.vertices

        for source in sources:
            distance[source] = 0

        for vertex in topological_order:
            for neighbor, weight in self.adjacency_list[vertex]:
                for source in sources:
                    new_distance = distance[vertex] + weight
                    if new_distance < distance[neighbor]:
                        distance[neighbor] = new_distance

        min_distance = float('inf')
        for destination in destinations:
            min_distance = min(min_distance, distance[destination])

        return min_distance

# Read input from file
with open("graf.in", "r") as file:
    v, e = map(int, file.readline().split())
    graph = Graph(v)

    for _ in range(e):
        a, b, c = map(int, file.readline().split())
        graph.add_edge(a, b, c)

    s = list(map(int, file.readline().split()))
    t = list(map(int, file.readline().split()))

# Run the algorithm
min_distance = graph.min_distance_dag(s, t)
print("Minimum distance:", min_distance)