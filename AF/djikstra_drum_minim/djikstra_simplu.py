#algoritm dijkstra
#graf orientat +neor
"""#algoritm prim
import heapq
def citire_liste_cost(nume_fisier):
    f=open(nume_fisier)
    n,m=[int(x) for x in f.readline().split()]
    w=[[] for j in range(n+1)] #lista adiacenta
    for linie in f:
        x,y,c = (int(x) for x in linie.split())
        w[x].append((y,c))
        w[y].append((x,c))
    f.close()
    return n,m,w

def prim(s):
    viz = [0]*(n+1)
    tata = [0] * (n + 1)
    d = [float("inf")]*(n+1)
    Q =[]
    d[s]=0
    heapq.heappush(Q,(d[s],s))#cost si varf
    for i in range(n):
        c,u=heapq.heappop(Q) #varful nevizitat cu d minim
        while (viz[u]==1): #putem avea copii
            c,u = heapq.heappop(Q)
        viz[u]=1
        for v,c in w[u]: #actualizam etichetele vecinilor nevizitati
            if viz[v]==0:
                if d[v]>c:
                    d[v]=c
                    tata[v]=u
                    heapq.heappush(Q,(c,v))
    cost_total=0
    for u in range(1,n+1):
        if tata[u]!=0:
            print(u,tata[u])
            cost_total+=d[u]
    print("cost total",cost_total)

n,m,w=citire_liste_cost("apcm.in")
prim(1)"""

# MAI SUS AVEM ALGORITMUL LUI PRIM - Minimum spanning tree

import heapq
def citire_liste_cost(nume_fisier,orientat):
    f=open(nume_fisier)
    n,m=[int(x) for x in f.readline().split()]
    w=[[] for j in range(n+1)] #lista adiacenta
    for linie in f:
        x,y,c = (int(x) for x in linie.split())
        w[x].append((y,c))
        if orientat==False:
            w[y].append((x,c))
    f.close()
    return n,m,w

def dijkstra(s):
    viz = [0]*(n+1)
    tata = [0] * (n + 1)
    d = [float("inf")]*(n+1)
    Q =[]
    d[s]=0
    heapq.heappush(Q,(d[s],s))#cost si varf
    while len(Q)>0:
        c,u=heapq.heappop(Q) #varful nevizitat cu d minim
        if (viz[u]==0):
            viz[u]=1
            for v,c in w[u]: #actualizam etichetele vecinilor nevizitati
                if viz[v]==0:
                    if d[v]>c+d[u]:
                        #if v in puncte_control:
                        d[v]=c+d[u]
                        tata[v]=u
                        heapq.heappush(Q,(c,v))
    return d,tata

#care e cel mai apropiat vf de control de start
n,m,w=citire_liste_cost("graf.in",False)
start=int(input("vf start: "))
p_control = [int(x) for x in input("puncte de control: ").split()]
d,tata=dijkstra(start)
print(d)
print(tata)
mini=100000000
dest=0
for i in p_control:
    if d[i]<mini:
        mini=d[i]
        dest=i
drum=[]
u=dest
drum.append(u)
while u!= start:
    u=tata[u]
    drum.append(u)
drum.reverse()
