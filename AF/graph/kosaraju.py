from collections import deque
def get_lista(file, tip):
    fisier = open(file,"r")
    n, m = [int(x) for x in (fisier.readline().split())]

    l_adiacenta = [[] for i in range(n+1)]
    for i in range(m):
        x, y = [int(k) for k in (fisier.readline().split())]
        l_adiacenta[x].append(y)
        if(tip=="neorientat"):
            l_adiacenta[y].append(x)
    return l_adiacenta, n
l, n = get_lista("kosaraju.in","orientat")
print(l)
fin = []
viz = [0] * (n+1)  #len(l) = nr varfuri
def DFS(start,l,tip = "initial"):
    viz[start] = 1
    for v in l[start]:
        if(viz[v]==0):
            DFS(v,l,tip)
    if(tip == "transpus"):
        print(start,end=" ")
    else:
        fin.append(start)

for i in range(1,n+1):
    if viz[i] == 0:
        DFS(i,l)

print(fin[::-1])

def construieste_transpusa(lista,n):
    l_trans = [[] for i in range(n+1)]
    for x in range(1,n+1):
        for y in lista[x]:
            l_trans[y].append(x)
    return l_trans
l_trans = construieste_transpusa(l,n)
print(l_trans)
viz = [0] * (n+1)
for i in fin[::-1]:
    if viz[i] == 0:
        DFS(i,l_trans,"transpus")
        print()