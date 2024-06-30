#include "decompositions.hpp"
#include "lists.hpp"
#include<unordered_set>
using namespace std;

list< list<unsigned int> > twin_classes(const Graph& G){

    list< list<unsigned int> > res;

    unordered_set<unsigned int> V;
    for(unsigned int v : G.vertex_list())
        V.insert(v);

    partition_refinement pf(V), pt(V);

    for(unsigned int v : V){
        unordered_set<unsigned int> N;
        for(unsigned int u : G.neighbours(v))
            N.insert(u);
        pf.refine(N); //false twins
        N.insert(v);
        pt.refine(N); //true twins
    }

	//get all nontrivial false twin classes
    for(list<unsigned int> C : pf.get_partition())
        if(C.size() > 1){
            res.push_back(C);
            for(unsigned int v : C) V.erase(v);
        }
    //get all nontrivial true twin classes
    for(list<unsigned int> C : pt.get_partition())
        if(C.size() > 1){
            res.push_back(C);
            for(unsigned int v : C) V.erase(v);
        }
    //get all remaining vertices
    for(unsigned int v : V){
        list<unsigned int> singleton;
        singleton.push_back(v);
        res.push_back(singleton);
    }

    return res;

}

bool is_prime(const Graph& G){

    if(G.order() < 4) return 0; //P4 is the smallest prime graph

    for(unsigned int u : G.vertex_list())
        for(unsigned int v : G.vertex_list()){
            if(u != v){
                unordered_set<unsigned int> M; //smallest module containing both u and v
                M.insert(u); M.insert(v);
                bool flag;
                do{
                    flag = 0;
                    for(unsigned int w : G.vertex_list()){
                        if(M.find(w) == M.end()){
                            unsigned int d(0);
                            for(unsigned int x : M)
                                if(G.adjacent(x,w)) d++;
                            if(d > 0 && d < M.size()) { flag = 1; M.insert(w); } //splitter
                        }
                    }
                }while(flag);
                if(M.size() != G.order()) return 0; //nontrivial module found
            }
        }

    return 1;

}
