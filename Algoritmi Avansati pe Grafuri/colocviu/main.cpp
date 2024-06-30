#include <iostream>
#include<unordered_set>
#include<unordered_map>
#include<list>
#include<utility> //pair
#include <limits>
#include "graphs.hpp"
#include "graphs.cpp"
#include "lists.hpp"
#include "lists.cpp"
#include <fstream>
#include "search.hpp"
#include "search.cpp"

using namespace std;
/*
list<unsigned int> lexbfs3(unsigned int s, const Graph& G){

	list<unsigned int> output;
	unordered_set<unsigned int> visited;

	unordered_set<unsigned int> V;
	for(unsigned int v : G.vertex_list())
	 V.insert(v);
	partition_refinement p(V);

	unordered_set<unsigned int> S;
	S.insert(s);
	p.refine(S);

	while(!p.empty()){

		unsigned int v = p.next();
		visited.insert(v);
		output.push_back(v);

		S.clear();
		for(unsigned int u : G.neighbours(v))
		 if(visited.find(u) == visited.end())
		  S.insert(u);
		p.hopcroft_refine(S);
	}

	return output;
}

*/


list<unsigned int> cautare(Graph G, unsigned int s) {
	list<unsigned int> output;
	unordered_set<unsigned int> visited;
	queue<unsigned int> q;
    list<unsigned int> labels[G.vertex_list().size()];
    list<unsigned int> first;
    first.push_back(1);
    labels.push_back(first);

	visited.insert(s);
	for(unsigned int u : G.neighbours(s)) {
        labels[u].push_back(1);


	}
	q.push(s);

	while(!q.empty()){

		unsigned int v = q.front();
		q.pop();


		for(unsigned int u : G.neighbours(v))
		 if(visited.find(u) == visited.end()){
		     for ( unsigned int k : G.neighbours(v) ){
                unsigned int maxim =
		     }

		 	visited.insert(u);
		 	q.push(u);
		 }
	}

	return output;
}





int main()
{   Graph g;
    ifstream fopen("graf.in");
    int n, u, v;
    if (fopen.is_open()) {
        fopen >> n;
        for (int i=0; i<n; i++){
            g.add_node(i);
        }
        cout << n<<endl;;
        while (fopen >> u >> v) {
            g.add_edge(u, v, 1);
            //cout << u <<" - "<<v << endl;
        }
    }
/*
    for(unsigned int l : g.vertex_list() ) {
        cout << l;
    }

    list<unsigned int> l = lexbfs(0, g);

    for (unsigned int k : l ) {
        cout << k <<" ";
    }

    queue<unsigned int> q;
    q.push(1);
    q.push(3);
    int k = q.front();
    cout << k;
*/

    list<unsigned int> rez = lexbfs3(0, g);
    for  (auto i : rez ) {
        cout << i <<" ";
    }
    return 0;
}
