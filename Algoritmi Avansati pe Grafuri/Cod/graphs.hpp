/*Graph representations -- Support edge and vertex insertions/deletions
@author: G. Ducoffe
*/

#ifndef __GRAPHS__
#define __GRAPHS__

/*dependencies*/
#include<unordered_set>
#include<unordered_map>
#include<list>
#include<utility> //pair
#include <limits>
using namespace std;

typedef unsigned int Vertex;

class Graph {
	
	public: 
	
	/*intermediate structures*/
	
	//edge in an adjacency list (one end-vertex is implicit)
	struct Edge{
		double _weight; //edge weight
		list<Vertex>::iterator _pos; //position in the adjacency list
	};
	//neighborhood
	struct AdjList{
		list<Vertex> _list; //adjacency list
		unordered_map<Vertex,Edge> _map; //index
	};
	
	private:
		
	/*flags*/
	
	//directed flag (the graph is directed if set to true)
	bool is_directed;
	//weighted flag (the graph is edge-weighted if set to true)
	bool is_weighted;
	
	/*internal structure*/
		
	//number of edges (or arcs, if directed)
	unsigned int m;
		
	//out-neighborhood
	unordered_map< Vertex, AdjList > Out;
	//in-neighborhood (unused if undirected)
	unordered_map< Vertex, AdjList > In;
		
	//set of all vertices
	unordered_set<Vertex> vertices;
	
	//garbage: removed vertices
	list<Vertex> dead_vertices;
	 //generation of a default ID
	Vertex gen_id(void);
		
	public: 
	
		//constructors
		Graph(bool,bool = 0); //construction of a undirected/directed unweighted/weighted null graph
		Graph(); //construction of a null undirected unweighted graph
		Graph(const Graph&); //copy constructor
		
		//graph information
		inline unsigned int order(void) const {return vertices.size(); } //number of nodes
		inline unsigned int size(void) const { return m; } //number of edges
		inline bool directed(void) const { return is_directed; }
		inline bool weighted(void) const { return is_weighted; }
		
		//edge information
		list< pair<Vertex, Vertex> > edges(void) const; //enumerate all arcs
		double weight(Vertex,Vertex) const; //arc weight (1 if undirected, undefined if arc does not exist)
		bool adjacent(Vertex,Vertex) const;
		
		//vertex information
		list<Vertex> vertex_list(void) const; //enumerate all vertices
		int degree(Vertex) const; //total degree of a node (-1 if node does not exist)
		int out_degree(Vertex) const;
		int in_degree(Vertex) const;
		list<Vertex> neighbours(Vertex) const; //enumerate all (out-)neighbours of a node
		list<Vertex> in_neighbours(Vertex) const;
		
		//dynamic operations
		bool add_edge(Vertex,Vertex, double = 1); //adds a new edge, if it is not already present
		bool remove_edge(Vertex,Vertex); //removes an edge, if it is already present
		
		bool add_node(Vertex); //inserts a new isolated vertex, if it does not already exist
		Vertex add_node(void); //inserts a node, with an automatically generated id, and outputs this id
		bool remove_node(Vertex); //removes a node, being given its ID 
		
		void reorder(list<Vertex>); //reorder adjacency list according to some vertex permutation
		
		bool contract(Vertex,Vertex,Vertex); //contract two adjacent vertices
		int contract(Vertex,Vertex); //contract two adjacent vertices, and outputs the ID of the resulting node	
		
	private:
		
		void insert(AdjList&,Vertex,double);
		void erase(AdjList&,Vertex);
		void make_first(AdjList&,Vertex);
		
};

#endif
