#include <iostream>
#include <vector>
#include <stack>
#include <algorithm>
using namespace std;

// Function to perform Tarjan's algorithm
void tarjanStrongModules(int v, vector<vector<int>>& graph, vector<int>& lowLink, vector<int>& index, vector<bool>& onStack, stack<int>& nodeStack, vector<vector<int>>& strongModules, int& currentIndex)
{
    // Set the index and lowLink values for the current vertex
    index[v] = currentIndex;
    lowLink[v] = currentIndex;
    currentIndex++;
    nodeStack.push(v);
    onStack[v] = true;

    // Traverse the neighbors of the current vertex
    for (int neighbor : graph[v])
    {
        if (index[neighbor] == -1)
        {
            // Recursive call for unvisited neighbor
            tarjanStrongModules(neighbor, graph, lowLink, index, onStack, nodeStack, strongModules, currentIndex);
            lowLink[v] = min(lowLink[v], lowLink[neighbor]);
        }
        else if (onStack[neighbor])
        {
            // Update lowLink value if neighbor is on the stack
            lowLink[v] = min(lowLink[v], index[neighbor]);
        }
    }

    // If v is a root of a strong module, pop nodes from the stack and add them to the strong module
    if (lowLink[v] == index[v])
    {
        vector<int> module;
        int node;
        do
        {
            node = nodeStack.top();
            nodeStack.pop();
            onStack[node] = false;
            module.push_back(node);
        } while (node != v);

        strongModules.push_back(module);
    }
}

// Function to find all strong modules in the graph
vector<vector<int>> findStrongModules(vector<vector<int>>& graph, int n)
{
    vector<int> lowLink(n, -1);
    vector<int> index(n, -1);
    vector<bool> onStack(n, false);
    stack<int> nodeStack;
    vector<vector<int>> strongModules;
    int currentIndex = 0;

    // Apply Tarjan's algorithm to find the strong modules
    for (int i = 0; i < n; ++i)
    {
        if (index[i] == -1)
        {
            tarjanStrongModules(i, graph, lowLink, index, onStack, nodeStack, strongModules, currentIndex);
        }
    }

    return strongModules;
}

int main()
{
    int n, m;
    cout << "Enter the number of vertices: ";
    cin >> n;
    cout << "Enter the number of edges: ";
    cin >> m;

    vector<vector<int>> graph(n);
    cout << "Enter the edges:\n";
    for (int i = 0; i < m; ++i)
    {
        int u, v;
        cin >> u >> v;
        graph[u].push_back(v);
        graph[v].push_back(u);
    }

    // Find strong modules in the graph
    vector<vector<int>> strongModules = findStrongModules(graph, n);

    // Print the strong modules
    cout << "Strong Modules:\n";
    int i = 0;
    for (const vector<int>& module : strongModules)
    {   cout << "componenta " << i <<": "<< endl;
        for (int vertex : module)
        {
            cout << vertex << " ";
        }
        cout << endl;
        i+=1;
    }

    return 0;
}
