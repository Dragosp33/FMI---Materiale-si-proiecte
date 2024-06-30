#Sortare topologica
#graf orientat

def citire(filename):
    f = open(filename)
    n = int(f.readline())
    durata = [ int(x) for x in f.readline().split()]
    m = int(f.readline())
    la = [[] for x in range(n+3)] 
     
    for i in range(m):
        m1, m2 = [ int(x) for x in f.readline().split()]
        la[m1].append((m2,durata[m1-1]))

    #gradul intern al fiecarui nod
    g_int = [0]*(n+1) 
    for u in range(1,n+1):
        for v, c in la[u]:
            g_int[v]+=1
            
    s = n + 1
    t = n + 2
    for i in range(1, n+1):
        if g_int[i] == 0:
            la[s].append((i,0))
        if len(la[i]) == 0:
            la[i].append((t,durata[i-1]))
    f.close()
    
    return n+2,s,t, la, durata


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

n,s,t,la , durata= citire("drumuri.in")
d, tata = drumMaximDag(s)
print(d,tata)
print(d[t])

i=t
while tata[i] != s:
    print(tata[i], end =" ")
    i = tata[i]
print()  
for i in range(1, n-1):
    print(f"{i}: {d[i]}, {d[i]+durata[i-1]}")