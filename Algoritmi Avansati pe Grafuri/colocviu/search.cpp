#include "search.hpp"

#include "lists.hpp"
#include <queue>
#include <stack>
#include <unordered_set>
using namespace std;

/*-------------------------------------------- Graph Search -----------------------------------------*/

list<unsigned int> dfs(unsigned int s,const Graph& G){
	list<unsigned int> output;
	unordered_set<unsigned int> visited;
	stack<unsigned int> p;
	
	p.push(s);
	
	while(!p.empty()){
		
		unsigned int v = p.top();
		p.pop();
		
		if(visited.find(v) == visited.end()){
			visited.insert(v);
			output.push_back(v);
			list<unsigned int> Nv = G.neighbours(v);
			Nv.reverse(); 
			for(unsigned int u : Nv)
			 p.push(u);
		}
		
	}
	
	return output;
}


list<unsigned int> bfs(unsigned int s,const Graph& G){
	list<unsigned int> output;
	unordered_set<unsigned int> visited;
	queue<unsigned int> q;
	
	visited.insert(s);
	q.push(s);
	
	while(!q.empty()){
	
		unsigned int v = q.front();
		q.pop();
		output.push_back(v);
	
		for(unsigned int u : G.neighbours(v))
		 if(visited.find(u) == visited.end()){
		 	visited.insert(u);
		 	q.push(u);
		 }
	}
	
	return output;
}

list<unsigned int> mcs(unsigned int s,const Graph& G){
	list<unsigned int> output;
	unordered_set<unsigned int> visited;
	frequency_queue q;
	
	visited.insert(s);
	q.insert(s);
	
	while(!q.empty()){
		
		unsigned int v = q.peek_max();
		q.erase_max();
		
		visited.insert(v);
		output.push_back(v);
		
		for(unsigned int u : G.neighbours(v))
		 if(visited.find(u) == visited.end())
		  q.insert(u);
		  
	}
	
	return output;
}

list<unsigned int> lexbfs(unsigned int s, const Graph& G){
	
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
		p.refine(S);
	}
	
	return output;
}

list<unsigned int> lexdfs(unsigned int s, const Graph& G){
	
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

/*-------------------------------------------- Search Verification -----------------------------------------*/

bool compare_lists(const list<unsigned int>& a, const list<unsigned int>& b){
	auto ita = a.begin(), itb = b.begin();
	while(ita != a.end() && itb != b.end()){
		if(*ita != *itb)
		 return 0;
		ita++; itb++;
	}
	return (ita == a.end() && itb == b.end());
}

bool verif_dfs(unsigned int s, Graph G, const list<unsigned int>& L){
	G.reorder(L);
	return compare_lists(L,dfs(s,G));
}
bool verif_bfs(unsigned int s,Graph G, const list<unsigned int>& L){
	G.reorder(L);
	return compare_lists(L,bfs(s,G));
}

bool verif_mcs(unsigned int s,Graph G, const list<unsigned int>& L){
    
	unordered_set<unsigned int> visited;
	frequency_queue q;
	
	q.insert(s);
	
	auto p = L.begin();
	while(!q.empty() && p != L.end()) {
	
		while(!q.empty() && visited.find(q.peek_max()) != visited.end())
		 q.erase_max();
		
		unsigned int v = *p;
		visited.insert(v);
		
		if(q.empty() || q.count(v) < q.count(q.peek_max())) 
		 return 0;
		 	
		for(unsigned int u : G.neighbours(v))
		 if(visited.find(u) == visited.end())
		  q.insert(u);
		
		p++;
		  
	}
	
	return (p == L.end());
}

bool verif_lexbfs(unsigned int s,Graph G, const list<unsigned int>& L){
	
	unordered_set<unsigned int> visited;
	
	unordered_set<unsigned int> V;
	for(unsigned int v : G.vertex_list())
	 V.insert(v);
	partition_refinement p(V);
	
	unordered_set<unsigned int> S;
	S.insert(s);
	p.refine(S);
	
	auto it = L.begin();
	while(!p.empty() && it != L.end()){
		
		unsigned int v = *it;
		if(!p.make_next(v))
		 return 0;
		visited.insert(v);
		
		S.clear();
		for(unsigned int u : G.neighbours(v))
		 if(visited.find(u) == visited.end())
		  S.insert(u);
		p.refine(S);
		
		it++;
	}
	
	return (it == L.end()); 
}

bool verif_lexdfs(unsigned int s, Graph G, const list<unsigned int>& L){
	unordered_set<unsigned int> visited;
	
	unordered_set<unsigned int> V;
	for(unsigned int v : G.vertex_list())
	 V.insert(v);
	partition_refinement p(V);
	
	unordered_set<unsigned int> S;
	S.insert(s);
	p.refine(S);
	
	auto it = L.begin();
	while(!p.empty() && it != L.end()){
		
		unsigned int v = *it;
		if(!p.make_next(v))
		 return 0;
		visited.insert(v);
		
		S.clear();
		for(unsigned int u : G.neighbours(v))
		 if(visited.find(u) == visited.end())
		  S.insert(u);
		p.hopcroft_refine(S);
		
		it++;
		
	}
	
	return (it == L.end());
}
