import heapq
#cele mai apropiate puncte de control pentru toate varfurile
# graf orientat; djikstra - muchii cu cost

def dijkstra(graph, control_points):
    num_vertices = len(graph)
    num_control_points = len(control_points)
    distance = [[float('inf')] * num_control_points for _ in range(num_vertices)]
    closest_control_point = [-1] * num_vertices
    parent = [-1] * num_vertices

    queue = [(0, control_points[i], i) for i in range(num_control_points)]

    for i in range(num_control_points):
        control_point = control_points[i]
        distance[control_point][i] = 0

    while queue:
        dist, vertex, control_point_index = heapq.heappop(queue)
        # Check if a shorter path to vertex from control_point_index has been found
        if dist > distance[vertex][control_point_index]:
            continue

        for neighbor, weight in graph[vertex]:
            for i in range(num_control_points):
                control_point = control_points[i]
                # Calculate distance through control_point
                dist_neighbor = dist + weight
                if dist_neighbor < distance[neighbor][i]:
                    distance[neighbor][i] = dist_neighbor
                    closest_control_point[neighbor] = control_point
                    parent[neighbor] = vertex
                    heapq.heappush(queue, (dist_neighbor, neighbor, i))

    return distance, closest_control_point, parent


def get_path(vertex, parent):
    path = []
    path.append(parent)
    while vertex != parent:
        path.append(vertex)
        vertex = parent[vertex]
    return path[::-1]


# Example usage
if __name__ == '__main__':
    # Define the graph as an adjacency list with weights
    graph = [
        [(1, 5), (2, 3)],
        [(0, 5), (2, 2), (3, 6)],
        [(0, 3), (1, 2), (3, 7)],
        [(1, 6), (2, 7), (4, 4)],
        [(3, 4)]
    ]

    control_points = [0, 3]  # Example control points

    # Run Dijkstra's algorithm
    distance, closest_control_point, parent = dijkstra(graph, control_points)
    print(parent)
    # Print the closest control point, distance, and path for each vertex
    for vertex in range(len(graph)):
        #path = get_path(vertex, parent)
        print(f"Vertex {vertex}: Closest Control Point: {closest_control_point[vertex]}, "
              f"Distance: {distance[vertex]}") #, path {get_path( vertex, parent ) }
