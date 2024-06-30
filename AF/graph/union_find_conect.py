class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return

        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1


def add_minimum_edges(input_file):
    with open(input_file, 'r') as file:
        n, m = map(int, file.readline().strip().split())
        edges = []

        for _ in range(m):
            x, y = map(int, file.readline().strip().split())
            edges.append((x - 1, y - 1))  # Adjust node labels to 0-based indexing

    # Construct the initial graph
    graph = [[] for _ in range(n)]
    for x, y in edges:
        graph[x].append(y)
        graph[y].append(x)

    # Find the components using Union-Find
    uf = UnionFind(n)
    for x, y in edges:
        uf.union(x, y)

    # Find the number of components
    components = set()
    for node in range(n):
        components.add(uf.find(node))

    num_components = len(components)
    print(components)

    # adauga o singura muchie pt a obtine cea mai mare componenta conexa:
    comp_n = [0] * n




    # Add the minimum number of edges to make the graph connected
    
    # !!! important:   ESTE PT TOATE NODURILE GRAFULUI,
    # !!!              DACA AVEM O MULTIME DE NODURI M => INLOCUIM NODE IN RANGE (1, n) cu node in M, si uf.find(0) si uf.union(0) cu uf.find(M[0]) / uf.union(M[0])

    added_edges = []
    for node in range(1, n):
        if uf.find(node) != uf.find(0):
            uf.union(0, node)
            added_edges.append((0, node))
            num_components -= 1

            if num_components == 1:
                break

    # Print the added edges
    print("Added edges:")
    for edge in added_edges:
        print(f"{edge[0]} {edge[1]}")


# Usage example
input_file = "file.in"
add_minimum_edges(input_file)