#Sortare topologica
#graf orientat
# drumul maxim -> timpul minim de incheiere


def citire(filename):
    f = open(filename)
    n, m = [ int(x) for x in f.readline().split()]
    la = [[] for x in range(n+1)] 
     #gradul intern al fiecarui nod
    for i in range(m):
        m1, m2, c = [ int(x) for x in f.readline().split()]
        la[m1].append((m2,c));

    f.close()
    
    return n,m,la


def SortareTopologica():
    
    g_int = [0]*(n+1) 
    for u in range(1,n+1):
        for v, c in la[u]:
            g_int[v]+=1
        
    sTop=[]
    poz=0
    for x in range(1, len(g_int)):
        if g_int[x] == 0:
            sTop.append(x)
    while len(sTop) != n :
        for i,cost in la[sTop[poz]]:
            g_int[i] -= 1
            if g_int[i] == 0:
                sTop.append(i)
        poz += 1
    return sTop
    
def distanteDag(sursa):
    sTop = SortareTopologica()
    tata = [0] *(n+1)
    d = [float('inf')] *(n+1)
    d[sursa] = 0
    
    for u in sTop:
        for vf,cost in la[u]:
            if d[vf] > d[u] + cost:
                d[vf] = d[u] +cost
                tata[vf] = u
    return d, tata
# print(sTop)


def drumMaximDag(sursa):
    sTop = SortareTopologica()
    tata = [0] *(n+1)
    d = [-float('inf')] *(n+1)
    d[sursa] = 0
    
    for u in sTop:
        for vf,cost in la[u]:
            if d[vf] < d[u] + cost:
                d[vf] = d[u] +cost
                tata[vf] = u
    return d, tata
# print(sTop)

n,m,la = citire("dag.in")
d, tata = distanteDag(5)
print(d,tata)
d, tata = drumMaximDag(5)
print(d,tata)
