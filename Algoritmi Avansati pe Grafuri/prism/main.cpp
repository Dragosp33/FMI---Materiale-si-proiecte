#include <iostream>
#include <vector>

using namespace std;

// Function to check if G contains a prism
bool containsPrism(vector<vector<int>>& graph) {
    int n = graph.size();

    for (int u = 0; u < n; u++) {
        for (int v = 0; v < n; v++) {
            if (u == v) continue;

            // Check if u and v have exactly two neighbors
            if (graph[u].size() == 2 && graph[v].size() == 2) {
                vector<int>& neighbors_u = graph[u];
                vector<int>& neighbors_v = graph[v];

                // Check if neighbors of u and v form a path
                int commonNeighbor = -1;
                for (int neighbor : neighbors_u) {
                    if (neighbor == v) continue;
                    if (neighbors_v[0] == neighbor || neighbors_v[1] == neighbor) {
                        commonNeighbor = neighbor;
                        break;
                    }
                }

                // If a common neighbor is found, check for the universal vertex
                if (commonNeighbor != -1) {
                    vector<int>& neighbors_common = graph[commonNeighbor];

                    // Check if the common neighbor is connected to all vertices of the path
                    if (neighbors_common.size() == 4) {
                        int count = 0;
                        for (int neighbor : neighbors_common) {
                            if (neighbor == u || neighbor == v)
                                count++;
                        }

                        // If the common neighbor is connected to all vertices of the path, we found the prism
                        if (count == 2)
                            return true;
                    }
                }
            }
        }
    }

    return false;
}

// Test the implementation
int main() {
    int n, m;
    cin >> n >> m;  // Number of vertices and edges

    vector<vector<int>> graph(n);  // Adjacency list representation of the graph

    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;  // Read an edge

        // Add the edge to the adjacency list
        graph[u].push_back(v);
        graph[v].push_back(u);
    }

    bool hasPrism = containsPrism(graph);

    if (hasPrism)
        cout << "Graph contains a prism with a 4-node path and a universal vertex." << endl;
    else
        cout << "Graph does not contain a prism with a 4-node path and a universal vertex." << endl;

    return 0;
}
