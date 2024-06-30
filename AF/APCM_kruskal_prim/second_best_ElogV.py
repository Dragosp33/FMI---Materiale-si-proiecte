from collections import defaultdict

# Class to represent a graph
class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = []

    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])

# Class to represent a disjoint set
class DisjointSet:
    def __init__(self, vertices):
        self.parent = [i for i in range(vertices)]
        self.rank = [0] * vertices

    def find(self, v):
        if self.parent[v] != v:
            self.parent[v] = self.find(self.parent[v])
        return self.parent[v]

    def union(self, v1, v2):
        root1 = self.find(v1)
        root2 = self.find(v2)

        if self.rank[root1] < self.rank[root2]:
            self.parent[root1] = root2
        elif self.rank[root1] > self.rank[root2]:
            self.parent[root2] = root1
        else:
            self.parent[root2] = root1
            self.rank[root1] += 1

# Function to find the second best minimum spanning tree
def find_second_best_mst(graph):
    V = graph.V
    ds = DisjointSet(V)

    # Sort the edges in non-decreasing order of their weights
    graph.graph.sort(key=lambda x: x[2])

    # Run Kruskal's algorithm
    mst = Graph(V)
    mst_weight = 0
    num_components = V

    for u, v, w in graph.graph:
        set_u = ds.find(u)
        set_v = ds.find(v)

        # If including the current edge does not form a cycle
        if set_u != set_v:
            # Add the edge to the second best minimum spanning tree
            mst.add_edge(u, v, w)
            mst_weight += w

            # Merge the connected components
            ds.union(set_u, set_v)
            num_components -= 1

            # If there is only one connected component, terminate the loop
            if num_components == 1:
                break

    # Identify the critical edge in the minimum spanning tree
    critical_edge = None
    max_weight = float('-inf')
    for u, v, w in mst.graph:
        if w > max_weight:
            max_weight = w
            critical_edge = [u, v]

    # Remove the critical edge from the minimum spanning tree
    mst.graph.remove(critical_edge)

    # Reset the disjoint set for the modified minimum spanning tree
    ds = DisjointSet(V)

    # Run Kruskal's algorithm on the modified minimum spanning tree
    second_best_mst = Graph(V)
    for u, v, w in mst.graph:
        set_u = ds.find(u)
        set_v = ds.find(v)

        # If including the current edge does not form a cycle
        if set_u != set_v:
            # Add the edge to the second best minimum spanning tree
            second_best_mst.add_edge(u, v, w)
            ds.union(set_u, set_v)

    return second_best_mst, mst_weight


# Example usage
g = Graph(4)
g.add_edge(0, 1, 10)
g.add_edge(0, 2, 6)
g.add_edge(0, 3, 5)
g.add_edge(1, 3, 15)
g.add_edge(2, 3, 4)

second_best_mst, weight = find_second_best_mst(g)
print("Edges in the second best minimum spanning tree:")
for u, v, w in second_best_mst.graph:
    print(f"{u} -- {v} : {w}")
print("Weight of the second best minimum spanning tree:", weight)