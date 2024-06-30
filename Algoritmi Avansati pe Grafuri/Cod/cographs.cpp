#include "cographs.hpp"
#include "lists.hpp"
#include "search.hpp"
#include <utility>
#include <unordered_set>
#include<queue>

vector<Graph> compute_cc(const Graph& G){

	unsigned int nr_cc(0);
	unordered_map<unsigned int, unsigned int> cc;

	for(unsigned int v : G.vertex_list())
	 if(cc.find(v) == cc.end()){
	 	cc[v] = nr_cc++;
	 	for(unsigned int u : bfs(v,G))
	 	 cc[u] = cc[v];
	 }

	vector<Graph> all_cc(nr_cc);

	for(unsigned int v : G.vertex_list())
      all_cc[cc[v]].add_node(v);

	for(pair<unsigned int, unsigned int> e : G.edges())
	  all_cc[cc[e.first]].add_edge(e.first,e.second);

	return all_cc;
}

vector<Graph> compute_co_cc(const Graph& G){

	unsigned int nr_co_cc(-1);
	unordered_map<unsigned int, unsigned int> co_cc;

	//LexBFS in the complement
	vector<unsigned int> vertices;
	unordered_set<unsigned int> visited;

	unordered_set<unsigned int> V;
	for(unsigned int v : G.vertex_list())
	 V.insert(v);
	partition_refinement p(V);

	unordered_set<unsigned int> S;
	while(!p.empty()){

		unsigned int v = p.next();
		visited.insert(v);
		vertices.push_back(v);

		S.clear();
		for(unsigned int u : G.neighbours(v))
		 if(visited.find(u) == visited.end())
		  S.insert(u);
		p.rrefine(S);


	}


	//extract co-connected components from output
	unordered_map<unsigned int,unsigned int> deg;
	for(unsigned int i = 0; i < G.order(); i++){
		unsigned int u = vertices[i];
		if(deg[u]==i) co_cc[u] = ++nr_co_cc;
		else co_cc[u] = nr_co_cc;
		for(unsigned int v : G.neighbours(u))
		 deg[v]++;
	}
	nr_co_cc++;

	//construct the subgraphs induced by each co-connected component
	vector<Graph> all_co_cc(nr_co_cc);

	for(unsigned int v : G.vertex_list())
      all_co_cc[co_cc[v]].add_node(v);

	for(pair<unsigned int, unsigned int> e : G.edges()){
		if(co_cc[e.first] == co_cc[e.second]) all_co_cc[co_cc[e.first]].add_edge(e.first,e.second);
	}

	return all_co_cc;

}

bool is_cograph(const Graph& G){

	if(G.order()<=1) return 1;

	vector<Graph> comp = compute_cc(G);
	if(comp.size() > 1){
		for(Graph H : comp)
		 if(!is_cograph(H))
		  return 0;
	}else{
		comp = compute_co_cc(G);
		if(comp.size() == 1) return 0;
		for(Graph H : comp)
		 if(!is_cograph(H))
		  return 0;
	}

	return 1;
}

cotree *build_cotree(const Graph& G){

	if(G.order() == 0) return nullptr;

	cotree *r = new cotree;
	r->parent = r->next = r->child = nullptr;

	if(G.order() == 1){
		unsigned int v = G.vertex_list().front();
		r->leaf = 1;
		r->vertex = v;
	}else{ //>=2 vertices
		r->leaf = 0;

		vector<Graph> comp = compute_cc(G);
		if(comp.size() > 1)
		 r->label = 0;
		else{
			comp = compute_co_cc(G);
			r->label = 1;
		}

		for(Graph H : comp){
			cotree *c = build_cotree(H);
			c->parent = r;
			c->next = r->child;
			r->child = c;
		}
	}

	return r;
}

unsigned int compute_clique_number(cotree *n){
	if(n==nullptr) return 0;
	if(n->leaf) return 1;
	unsigned int res(0);
	for(cotree *c = n->child; c != nullptr; c = c->next){
		unsigned int k = compute_clique_number(c);
		if(n->label) res += k;
		else if(res < k) res = k;
	}
	return res;
}

unsigned int clique_number(const Graph& G){
	cotree *r = build_cotree(G);
	unsigned int k = compute_clique_number(r);
	if(r != nullptr) delete r;
	return k;
}

list<cotree*> bfs_cotree(cotree *r){
	list<cotree*> output;

	queue<cotree*> q;
	if(r != nullptr) q.push(r);

	while(!q.empty()){
		cotree *n = q.front();
		q.pop();
		output.push_front(n);
		for(cotree *c = n->child; c != nullptr; c = c->next)
		 q.push(c);
	}

	return output;
}

list<unsigned int> pruning_sequence(const Graph& G){

	cotree *r = build_cotree(G);

	list<cotree*> bfs_order = bfs_cotree(r);

	list<unsigned int> ans;

	for(cotree *n : bfs_order){
		if(n->leaf){
			if(n->parent != nullptr && n->parent->child == n){ //last child
				n->parent->leaf = 1;
				n->parent->vertex = n->vertex;
			}else{
				ans.push_back(n->vertex);
			}
		}
	}

	delete r;
	return ans;
}
