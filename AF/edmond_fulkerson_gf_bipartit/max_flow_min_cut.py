from collections import deque

def bfs(graph, source, sink, parent):
    visited = [False] * len(graph)
    queue = deque()
    queue.append(source)
    visited[source] = True
    
    while queue:
        u = queue.popleft()
        
        for v in range(len(graph)):
            if not visited[v] and graph[u][v] > 0:
                queue.append(v)
                visited[v] = True
                parent[v] = u
                if v == sink:
                    return True
    
    return False


def edmonds_karp(graph, source, sink):
    parent = [-1] * len(graph)
    max_flow = 0
    
    while bfs(graph, source, sink, parent):
        path_flow = float('inf')
        s = sink
        
        while s != source:
            path_flow = min(path_flow, graph[parent[s]][s])
            s = parent[s]
        
        max_flow += path_flow
        
        v = sink
        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow
            graph[v][u] += path_flow
            v = parent[v]
    
    # Find minimum cut using BFS in the residual graph
    cut = []
    visited = [False] * len(graph)
    queue = deque()
    queue.append(source)
    visited[source] = True
    
    while queue:
        u = queue.popleft()
        
        for v in range(len(graph)):
            if not visited[v] and graph[u][v] == 0:
                queue.append(v)
                visited[v] = True
                cut.append((u, v))
    
    return max_flow, cut