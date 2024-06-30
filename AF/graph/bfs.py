import collections


def citire(nume_fisier):
    f = open(nume_fisier)
    n, m, s = [int(x) for x in f.readline().split()]
    s -= 1
    l = [[] for i in range(n)]
    for linie in f:
    #for i in range(m):
        x, y = [int(a) for a in linie.split()]
        l[x - 1].append(y - 1)
    f.close()
    return n, s, l






f=open("rj.in")
a=[]
n,m=[int(x) for x in f.readline().split()]

i=0
for linie in f:
    ls=linie.rstrip("\n")
    a.append(ls)
    if 'R' in ls:
        celula_R=(i,ls.index('R'))
    if 'J' in ls:
        celula_J=(i,ls.index('J'))
    i+=1

def in_matrice(x,y):
    return (0<=x<n) and (0<=y<m)

def bfs(celula_start):
    viz = [[0 for i in range(m)] for j in range(n)]
    d = [[-1 for i in range(m)] for j in range(n)]
    c=collections.deque()
    c.append(celula_start)
    viz[celula_start[0]][celula_start[1]]=1
    d[celula_start[0]][celula_start[1]]=0
    depl=[(1,0),(-1,0),(0,1),(0,-1),(1,1), (1,-1), (-1,1),(-1,-1)]
    while len(c) > 0:
        x,y = c.popleft()
        for dir in depl:
            i = x+dir[0]
            j = y+dir[1]
            if in_matrice(i, j) and a[i][j] != 'X' and viz[i][j] == 0:
                viz[i][j] = 1
                c.append((i, j))
                d[i][j] = 1 + d[x][y]


    return d


d_r = bfs(celula_R)
d_j = bfs(celula_J)
intalnire = (n, m)

t_min = m+n

for i in range(n):
    for j in range(m):
        if d_j[i][j] == d_r[i][j] and d_r[i][j]!=-1 and d_r[i][j]<t_min:
            t_min = d_r[i][j]
            intalnire = (i,j)

print(t_min, intalnire)


"""
def bfs(s):
        c = collections.deque()
        c.append(s)
        d[s] = 0
        viz[s] = 1
        while c:
            x = c.popleft()
            for y in l[x]:
                if viz[y] == 0:
                    c.append(y)
                    viz[y] = 1
                    d[y] = d[x] + 1

"""
