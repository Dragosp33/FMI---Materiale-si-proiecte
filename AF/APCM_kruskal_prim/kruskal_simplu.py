
def cheie(x):
    return x[2]

def initializare(u):
    tata[u]=0
    h[u] = 0

def reprez(u):
    if tata[u]==0:
        return u
    tata[u]= reprez(tata[u]) #cu compresie de cale - tata[u] va deveni radacina arborelui
    return tata[u]
    #return reprez(tata[u]) - fara compresie

def reuniune(u,v):
    ru=reprez(u) #radacina arborelui care contine u
    rv=reprez(v) #radacina arborelui care contine v
    if h[ru]>h[rv]:
        tata[rv] = ru
    else:
        tata[ru] = rv #rv devina radacina
        if h[ru] == h[rv]:
            h[rv]+=1

def kruskal():
    global tata,h
    tata=[0]*(n+1)
    h=[0]*(n+1)
    nr_m=0

    muchii.sort(key=cheie)
    for u in range(1,n+1):
        initializare(u)

    for e in muchii:
        if reprez(e[0])!=reprez(e[1]):
            reuniune(e[0],e[1])
            print(e[0],e[1])
            nr_m=nr_m+1
            if nr_m==n-1:
                break


tata=[]
h=[]
f=open("apcm.in")
muchii=[]
n,m=[int(x) for x in f.readline().split()]
for linie in f:
    ls = linie.split()
    muchii.append((int(ls[0]),int(ls[1]),int(ls[2])))
f.close()
kruskal()