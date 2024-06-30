/*Neighbourhood diversity and Modular decomposition
@author: G. Ducoffe
*/

#ifndef __DECOMPOSITIONS__
#define __DECOMPOSITIONS__

#include "graphs.hpp"
#include<list>
using namespace std;

list< list<unsigned int> > twin_classes(const Graph&);

bool is_prime(const Graph&);

#endif
