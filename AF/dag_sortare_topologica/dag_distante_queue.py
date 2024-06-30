import collections


def citire(file):
    f = open(file)
    ls = f.readline().split()
    n = int(ls[0])
    m = int(ls[1])

    # adj = [[] for i in range(n)]
    adj = []
    for i in range(n + 1):
        adj.append([])

    for i in range(m):
        ls = f.readline().split()
        x = int(ls[0])
        y = int(ls[1])
        cost = int(ls[2])
        adj[x].append([y, cost])

    return n, m, adj


def sort(n, adj):
    deg = [0 for i in range(n + 1)]
    for i in range(1, n + 1):
        for j, cost in adj[i]:
            deg[j] += 1
    q = collections.deque()
    for i in range(1, n + 1):
        if deg[i] == 0:
            q.append(i)
    sorttop = []
    while len(q) > 0:
        varf = q.popleft()
        sorttop.append(varf)
        for j, cost in adj[varf]:
            deg[j] -= 1
            if deg[j] == 0:
                q.append(j)

    return sorttop


def dist_dag(n, adj, start, dest):
    sorttop = sort(n, adj)
    d = [float("inf") for i in range(n + 1)]
    d[start] = 0
    pred = [0 for i in range(n + 1)]
    for i in sorttop:
        for j, cost in adj[i]:
            if d[j] > d[i] + cost:
                d[j] = d[i] + cost
                pred[j] = i
    drum = []
    while dest != start:
        drum.append(dest)
        dest = pred[dest]

    drum.append(start)

    drum.reverse()
    print(drum)


def drum_max_dag(n, adj, start, dest):
    sorttop = sort(n, adj)
    d = [-float("inf") for i in range(n + 1)]
    d[start] = 0
    pred = [0 for i in range(n + 1)]
    for i in sorttop:
        for j, cost in adj[i]:
            if d[j] < d[i] + cost:
                d[j] = d[i] + cost
                pred[j] = i
    drum = []
    while dest != start:
        drum.append(dest)
        dest = pred[dest]

    drum.append(start)

    drum.reverse()
    print(drum)


n, m, adj = citire("dag.txt")

dist_dag(n, adj, 1, 6)
drum_max_dag(n, adj, 1, 6)
