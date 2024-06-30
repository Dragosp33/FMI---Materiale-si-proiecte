import heapq
def distanta(p1,p2):
    return (p1[0]-p2[0])**2+(p1[1]-p2[1])**2
def citire(nume_fisier):
    f = open(nume_fisier)
    n, m, e = [int(x) for x in f.readline().split()]
    coordonate=[]
    for i in range(n+m):
        coordonate.append([int(x) for x in f.readline().split()])
    l = [[] for i in range(n+m+1)]
    # for linie in f:
    for i in range(e):
        x, y= [int(a) for a in f.readline().split()]
        c=distanta(coordonate[x-1],coordonate[y-1])
        l[x].append((y,c))
        l[y].append((x,c))
    f.close()
    print(l)
    return n,m,l

def prim(nr_surse):
    Q=[]
    tata = [0] * (n + 1)
    viz = [0] * (n + 1)
    d = [float("inf")] * (n + 1)
    for s in range(1,nr_surse+1):
        d[s] = 0
        heapq.heappush(Q,(d[s],s))
    while len(Q)>0:
        du, u = heapq.heappop(Q)
        while viz[u]==1 and len(Q)>0: #copii ramase in heap !!se poate goli
            du, u = heapq.heappop(Q)
        if len(Q)==0:
            break
        viz[u] = 1
        for v, w_uv in la[u]:  # actualizam etichetele vecinilor nevizitati
            if viz[v] == 0 :
                if d[v] > w_uv:
                    d[v] = w_uv
                    tata[v] = u
                    heapq.heappush(Q, (d[v], v))


    cost_total = 0
    for u in range(1, n + 1):
        if tata[u] != 0:
            print(u, tata[u])
            cost_total += d[u] #costul muchiei este in d[u]
    print("cost total", cost_total)
n,m,la=citire("retea.in")
nr_surse=n
print(nr_surse)
n=n+m

prim(nr_surse)