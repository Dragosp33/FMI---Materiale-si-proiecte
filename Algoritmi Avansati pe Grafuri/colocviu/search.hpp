/*Graph searches for unweighted graphs
--> (Lex)DFS, (Lex)BFS, MCS
@author: G. Ducoffe
*/

#ifndef __SEARCH__
#define __SEARCH__

#include "graphs.hpp"

list<unsigned int> dfs(unsigned int,const Graph&);
list<unsigned int> bfs(unsigned int,const Graph&);
list<unsigned int> mcs(unsigned int,const Graph&);
list<unsigned int> lexbfs(unsigned int,const Graph&);
list<unsigned int> lexdfs(unsigned int,const Graph&);

bool verif_dfs(unsigned int, Graph, const list<unsigned int>&);
bool verif_bfs(unsigned int, Graph, const list<unsigned int>&);
bool verif_mcs(unsigned int, Graph, const list<unsigned int>&);
bool verif_lexbfs(unsigned int, Graph, const list<unsigned int>&);
bool verif_lexdfs(unsigned int, Graph, const list<unsigned int>&);

#endif
