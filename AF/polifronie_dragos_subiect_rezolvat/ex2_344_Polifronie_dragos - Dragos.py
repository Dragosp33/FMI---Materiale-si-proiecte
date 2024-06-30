
def listaMuchii(fisier):
    
    f = open(fisier)

    m = int(f.readline().split()[1])
    lista = [[] for _ in range(m)]

    i = 0
    for i in range(m):
        lista[i] = [int(x) for x in f.readline().split()]
        
    lista.sort(key = lambda x : x[2])
    u,v  = [int(x) for x in f.readline().split()]

    f.close()

    return lista, (u, v)

# functie ce uneste doua componente din graf
# prin cele doua noduri trimise ca parametru

def union(nod1, nod2, marker):

    m1 = marker[nod1 - 1]
    m2 = marker[nod2 - 1]

    for i in range (len(marker)):
        if marker[i] == m2:
            marker[i] = m1

def kruskal(lista):

    global n, marker
    arbore = []
    numar = 0
    marker = [i for i in range(n)]

    costMinim = 0

    for muchie in lista:

        # daca cele doua varfuri nu sunt deja unite
        # le adaugam in arborele de cost minim

        if marker[muchie[0] - 1] != marker[muchie[1] - 1]:
            
            arbore.append(muchie)

            # marcam cele doua noduri cu acelasi numar
            # pentru a arata ca sunt unite
            union(muchie[0], muchie[1], marker)
            costMinim = costMinim + muchie[2]

            numar = numar + 1
        
            if (numar == n - 1):
                break
    
    return arbore, costMinim


def kruskal2(lista, edge, cost_apm):
    # pentru a gasi al doilea arbore care are cost diferit si contine muchia uv,
    # pur si simplu adaugam la inceput muchia uv in arbore dupa care scadem costul din  
    # primul arbore de cost partial, iar ce ramane, va fi costul muchiei uv, pe care il returnam
    # scadem 1 pentru ca ne trebuie costuri diferite.

    global n, marker
    arbore = []
    numar = 0
    cost_init = cost_apm
    marker = [i for i in range(n)]

    arbore.append(edge)

            # marcam cele doua noduri cu acelasi numar
            #         # pentru a arata ca sunt unite
    union(edge[0], edge[1], marker)
    costMinim = cost_init - 1 # scadem 1 pt a fi diferite costurile din al doilea arbore.

    numar = numar + 1

    

    for muchie in lista:

        # daca cele doua varfuri nu sunt deja unite
        # le adaugam in arborele de cost minim

        if marker[muchie[0] - 1] != marker[muchie[1] - 1]:
            
            arbore.append(muchie)

            # marcam cele doua noduri cu acelasi numar
            # pentru a arata ca sunt unite
            union(muchie[0], muchie[1], marker)
            costMinim = costMinim - muchie[2]

            numar = numar + 1
        
            if (numar == n - 1):
                break
    
    return arbore, costMinim


lista, edge = listaMuchii("grafpond2.in")
print(edge)
f = open("grafpond2.in", "r")

n, m = [int(x) for x in f.readline().split()]

# lista prin care tin cont care
# noduri sunt unite intre ele
marker = [i for i in range(n)]

# a)
arboreCostMinim, costMinim = kruskal(lista)

print(costMinim, arboreCostMinim)

arbore2, cost2 = kruskal2(lista, edge, costMinim)
edge = [edge[0], edge[1], cost2]
print(arbore2, cost2)

