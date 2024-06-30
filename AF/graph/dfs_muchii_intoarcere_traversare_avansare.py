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
tata=[0]*(n+1)
muchii_intoarcere = []
muchii_traversare = []
muchii_avansare = []



def DFS(i):
    viz[i] = 1
    for j in la[i]:
        if viz[j]==0:
            tata[j]=i
            DFS(j)
        else:
            if j!=tata[i]:
                if viz[j]==1:
                    print("ciclu inchis de muchia de intoarcere",i,j)
                    x=i
                    while x!=j:
                        print(x,end=" ")
                        x=tata[x]
                    print(j,i)
                    print()
                    #exit(0)
    viz[i] = 2

for i in range(1,n+1):
    if viz[i]==0:
        DFS(i)