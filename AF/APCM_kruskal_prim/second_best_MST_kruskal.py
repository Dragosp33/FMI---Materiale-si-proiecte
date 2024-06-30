# Python implementation to find the
# second best MST
 
# used to implement union-find algorithm
parent = [i for i in range(100005)]
 
# to keep track of edges in MST
present = []
 
# to keep track of number of edges
# in spanning trees other than the MST
edg = 0
 
# a structure to represent a
# weighted edge in graph
class Edge:
    def __init__(self, src, dest, weight):
        self.src = src
        self.dest = dest
        self.weight = weight
 
# array edges is of type edge.
 
# Compare two edges according
# to their weights.
# Used in sorted() for sorting
# an array of edges
def cmp(x, y):
    return x.weight < y.weight
 
# initialising the array -
# each vertex is its own parent
# initially
def initialise(n):
    # 1-indexed
    for i in range(1, n+1):
        parent[i] = i
 
# Implementing the union-find algorithm
def find(x):
    if parent[x] == x:
        return x
    parent[x] = find(parent[x])
    return parent[x]
 
# Function to find the union
# for the Minimum spanning Tree
def union1(i, sum):
    global edg
    x = find(edges[i].src)
    y = find(edges[i].dest)
    if x != y:
        # parent of x = y (LCA) -
        # both are edge connected
        parent[x] = y
 
        # keeping track of edges in MST
        present.append(i)
 
        # finding sum of weights
        # of edges in MST
        sum += edges[i].weight
    return sum
 
# Function to find the second
# best minimum spanning Tree
 
 
def union2(i, sum):
    global edg
    x = find(edges[i].src)
    y = find(edges[i].dest)
    if x != y:
        # parent of x = y (LCA) -
        # both are edge connected
        parent[x] = y
 
        # sum of weights of edges
        # in spanning tree
        sum += edges[i].weight
        edg += 1
    return sum
 
# Driver Code
if __name__ == "__main__":
    # V-> Number of vertices,
    # E-> Number of edges
    V = 5
    E = 8
 
# initialising the array to
# be used for union-find
    initialise(V)
 
# src, dest and weights can
# also be taken from user as
# input the following vectors
# represent - source[0],
# destination[0] are connected
# by an edge with
# weight[0]
    source = [1, 3, 2, 3, 2, 5, 1, 3]
    destination = [3, 4, 4, 2, 5, 4, 2, 5]
    weights = [75, 51, 19, 95, 42, 31, 9, 66]
    # create a list of Edge objects
edges = [Edge(0, 0, 0) for _ in range(E)]
 
# fill in the values for each edge
for i in range(E):
    edges[i].src = source[i]
    edges[i].dest = destination[i]
    edges[i].weight = weights[i]
 
# sorting the array of edges
# based on edge weights
edges = sorted(edges, key=lambda x: x.weight)
sum = 0
for i in range(E):
    sum = union1(i, sum)
 
# printing the cost of MST
print("MST: ", sum)
 
# sorting the array of edges
# based on edge weights
edges = sorted(edges, key=lambda x: x.weight)
 
# initialising cost of second best MST
sec_best_mst = float('inf')
 
# setting the sum to zero again.
sum = 0
j = 0
while j < len(present):
    initialise(V)
    edg = 0
    i = 0
    while i < E:
        # excluding one edge of
        # MST at a time
        # and forming spanning tree
        # with remaining
        # edges
        if i == present[j]:
            i += 1
            continue
        sum = union2(i, sum)
        i += 1
    # checking if number of edges = V-1 or not
    # since number of edges in a spanning tree of
    # graph with V vertices is (V-1)
    if edg != V - 1:
        sum = 0
        j += 1
        continue
 
    # storing the minimum sum
    # in sec_best_mst
    if sec_best_mst > sum:
        sec_best_mst = sum
    sum = 0
    j += 1
 
# printing the cost of second best MST
print("Second Best MST: ", sec_best_mst)