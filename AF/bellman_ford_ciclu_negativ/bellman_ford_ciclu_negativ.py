def citire(nume_fisier):
    f=open(nume_fisier)
    n,m=[int(x) for x in f.readline().split()]
    lista_arce=[]
    for linie in f:
        lista_arce.append([int(x) for x in linie.split()])
    print(lista_arce)
    return n,lista_arce

def b_ford(n,lista_arce,start):
    d = [float("inf") for i in range(n+1)]
    tata = [0 for i in range(n + 1)]
    d[start] = 0
    for i in range(n-1): #de n-1 ori
        for u,v,cost in lista_arce:
            if d[v] > d[u] +cost:
                d[v] = d[u] + cost
                tata[v] = u
    are_circuit_neg=False
    for u, v, cost in lista_arce:
        if d[v] > d[u] + cost:
            d[v] = d[u] + cost
            tata[v] = u
            are_circuit_neg =True
            vf_modificat=v


    return d,tata,are_circuit_neg,vf_modificat

def afiseaza_circuit(v,tata,n):
    x=v
    for i in range(n):
        x=tata[x]

    circuit=[x]
    y=tata[x]
    while y!=x:
        circuit.append(y)
        y=tata[y]
    circuit.append(x)
    circuit.reverse()
    return circuit

n,lista_arce=citire("bford.in")
sursa=1
d,tata,are_circuit_neg,v=b_ford(n,lista_arce,sursa)
if are_circuit_neg:
    print("are circuit negativ")
    circuit = afiseaza_circuit(v,tata,n)
    print(circuit)
else:
    print(d)
