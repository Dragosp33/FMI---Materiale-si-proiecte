/*Cographs recognition and algorithms
@author: G. Ducoffe
*/

#ifndef __COGRAPH__
#define __COGRAPH__

#include "graphs.hpp"
#include <vector>
#include <list>
#include <unordered_map>
using namespace std;

vector<Graph> compute_cc(const Graph&);
vector<Graph> compute_co_cc(const Graph&);

bool is_cograph(const Graph&);

//COTREE

struct cotree{
	
	bool leaf;
	bool label; //unused if leaf
	unsigned int vertex; //unused if internal
	
	cotree *parent, *child, *next;

	~cotree() {
		if(child != nullptr){ cotree *c = child; child = nullptr; delete c; }
		if(next != nullptr){ cotree *n = next; next = nullptr; delete n; }
	}
	
};

cotree *build_cotree(const Graph&);

unsigned int clique_number(const Graph&);

list<unsigned int> pruning_sequence(const Graph&);

#endif
