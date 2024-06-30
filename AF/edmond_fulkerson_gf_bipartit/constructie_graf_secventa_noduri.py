from collections import deque

def construct_graph(s1, s2):
    n = len(s1)
    m = sum(s1)

    if sum(s1) != sum(s2):
        return "NO"

    graph = [[] for _ in range(n + 2)]
    capacities = [[0] * (n + 2) for _ in range(n + 2)]

    # Create edges from source to nodes
    for i in range(n):
        graph[0].append(i + 1)
        graph[i + 1].append(0)
        capacities[0][i + 1] = s1[i]

    # Create edges from nodes to sink
    for i in range(n):
        graph[i + 1].append(n + 1)
        graph[n + 1].append(i + 1)
        capacities[i + 1][n + 1] = s2[i]

    while True:
        parent = [-1] * (n + 2)
        parent[0] = 0
        queue = deque([0])

        # Use BFS to find augmenting path
        while queue:
            u = queue.popleft()

            for v in graph[u]:
                if parent[v] == -1 and capacities[u][v] > 0:
                    parent[v] = u
                    queue.append(v)
                    if v == n + 1:  # Reached sink node
                        break

        if parent[n + 1] == -1:  # No augmenting path found
            break

        # Find the minimum capacity along the augmenting path
        path = []
        v = n + 1
        while v != 0:
            u = parent[v]
            path.append((u, v))
            v = u
        c_min = min(capacities[u][v] for u, v in path)

        # Reduce capacities along the augmenting path
        for u, v in path:
            capacities[u][v] -= c_min
            capacities[v][u] += c_min

    if sum(capacities[0]) == 0:
        arcs = [(i, j) for i in range(n) for j in graph[i + 1] if j != 0]
        return arcs
    else:
        return "NO"


# Read input from file
with open('sequences.in', 'r') as file:
    n = int(file.readline().strip())
    s1 = list(map(int, file.readline().strip().split()))
    s2 = list(map(int, file.readline().strip().split()))

# Construct the graph and get the arcs or "NO" if not possible
result = construct_graph(s1, s2)

# Display the arcs or "NO"
print(result)