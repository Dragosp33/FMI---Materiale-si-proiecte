def citire(tip): #am pus tipul grafului ca parametru, nu ca data in fisier
    # ar merge trimis ca parametru si numele fisierului, sa nu il fixam ca fiind graf.in:
    # citire(numefisier,tip)
    f=open("graf.in") #open(numefisier)
    n,m=[int(x) for x in f.readline().split()]
    la = [[] for i in range(n+1)]
    for i in range(m):
        m1,m2= [int(x) for x in f.readline().split()]
        la[m1].append(m2)
        if tip==1: #tip = 1 neorientat; tip = 2 orientat
            la[m2].append(m1)
    f.close()
    return n,m,la

n,m,la = citire(1) #graf neorientat

viz=[0]*(n+1)
niv=[0]*(n+1)
niv_min=[0]*(n+1)
pc=[False]*(n+1)
def DFS(i):
    viz[i] = 1
    niv_min[i] = niv[i]
    for j in la[i]:
        if viz[j]==0:
            niv[j]=niv[i]+1
            DFS(j)
            #intoarcere din recursivitate: fiul j se intoarce in tatal i
            #test de m c
            if niv_min[j] > niv[i]:
                print(i,j)
            #test p c - pentru varfuri diferite de radacina
            if niv_min[j] >= niv[i]:
                #print(i," punct critic")
                pc[i]=True
            niv_min[i]=min(niv_min[i],niv_min[j])
        else:
            if niv[j]<niv[i]-1: #if j!=tata[i]:
                niv_min[i] = min(niv_min[i], niv[j])

for i in range(1,n+1):
    if viz[i]==0:
        DFS(i)
print(pc)
#TEST separat pentru radacina
for i in range(1,n+1):
    if pc[i] == True:
        print(i)