#include <iostream>
#include <vector>
#include <stack>
#include <algorithm>
using namespace std;

void tarjanStrongModules(int v, vector<vector<int>>& graph, vector<int>& lowLink, vector<int>& index, vector<bool>& onStack, stack<int>& nodeStack, vector<vector<int>>& strongModules, int& currentIndex)
{
    index[v] = currentIndex;
    lowLink[v] = currentIndex;
    currentIndex++;
    nodeStack.push(v);
    onStack[v] = true;

    for (int neighbor : graph[v])
    {
        if (index[neighbor] == -1)
        {
            tarjanStrongModules(neighbor, graph, lowLink, index, onStack, nodeStack, strongModules, currentIndex);
            lowLink[v] = min(lowLink[v], lowLink[neighbor]);
        }
        else if (onStack[neighbor])
        {
            lowLink[v] = min(lowLink[v], index[neighbor]);
        }
    }

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

        bool isMaximal = true;
        for (const auto& existingModule : strongModules)
        {
            if (includes(existingModule.begin(), existingModule.end(), module.begin(), module.end()))
            {
                isMaximal = false;
                break;
            }
        }

        if (isMaximal && module.size() != graph.size())
        {
            strongModules.push_back(module);
        }
    }
}

vector<vector<int>> findMaximalStrongModules(vector<vector<int>>& graph, int n)
{
    vector<int> lowLink(n, -1);
    vector<int> index(n, -1);
    vector<bool> onStack(n, false);
    stack<int> nodeStack;
    vector<vector<int>> strongModules;
    int currentIndex = 0;

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
    }

    vector<vector<int>> maximalStrongModules = findMaximalStrongModules(graph, n);

    cout << "Maximal Strong Modules:\n";
    for (const vector<int>& module : maximalStrongModules)
    {
        for (int vertex : module)
        {
            cout << vertex << " ";
        }
        cout << endl;
    }

    return 0;
}
