import collections

#cele mai apropiate puncte de control pentru un singur nod, graf fara muchii cu cost

class graph:
    def __init__(self, fisier="file.in", oriented=False):

        self.orientation = oriented
        self.n, self.m, self.adj_list = self.read_file(fisier)
        #self.distances = [-1 for _ in range(self.n)]

    # citeste n -  nr noduri , m - nr muchii
    # pt i=0,m citeste fiecare muchie si o adauga
    # a se modifica in functie de problema
    def read_file(self, fisier):
        f = open(fisier)
        n, m = [int(x) for x in f.readline().split()]

        l = [[] for i in range(n)]
        for linie in f:
            # for i in range(m):

            x, y = [int(a) for a in linie.split()]
            l[x - 1].append(y - 1)
            if self.orientation == False:
                l[y - 1].append(x- 1)
        f.close()
        return n,m,l

    def bfs(self, s):
        viz = [0] * self.n
        distances = [-1] * self.n
        c = collections.deque()
        c.append(s)
        distances[s] = 0
        viz[s] = 1
        while c:
            x = c.popleft()
            for y in self.adj_list[x]:
                if viz[y] == 0:
                    c.append(y)
                    viz[y] = 1
                    distances[y] = distances[x] + 1
        return distances


def bfs_pct_control(graf, s, puncte):
    parinte = [-1] * graf.n
    viz = [0] * graf.n
    distances = [-1] * graf.n
    s-=1
    c = collections.deque()
    c.append(s)
    distances[s] = 0
    viz[s] = 1
    while c:
        x = c.popleft()
        for y in graf.adj_list[x]:
            if viz[y] == 0:
                c.append(y)
                viz[y] = 1
                distances[y] = distances[x] + 1
                parinte[y] = x
                print(y+1)
                if (y+1) in puncte:
                    print("cel mai apropiat punct de control este: ", y+1)
                    print("distanta este:  ", distances[y])
                    drum = []
                    j = y
                    drum.append(j)
                    while j:

                        j = parinte[j]
                        drum.append(j)
                    print(drum)
                    return True




    return distances


g = graph("graf.in", oriented=True)
p_control = [8, 9]
d = bfs_pct_control(g, 1, p_control)
print(d)