#varianta cu obligatoriu ultimele k linii

def citire(nume_fisier):
    muchii_date=[]
    muchii=[]
    f = open(nume_fisier)
    n,m = [int(x) for x in f.readline().split()]
    for i in range(m):
        x, y, c = [int(x) for x in f.readline().split()]
        muchii.append((x,y,c))
    for linie in f:
        x,y = [int(x) for x in linie.split()]
        cost=0
        for u,v,c in muchii: #caut muchia in lista de muchii sa determin costuk
            if {x,y} == {u,v}:
                cost=c
        muchii_date.append((x,y,cost))
    print(muchii_date)
    for x,y,c in muchii:
        if (x,y) in muchii_date:
            poz=muchii_date.index((x,y))
            muchii_date[poz].append(c)
        elif (y,x) in muchii_date:
            poz=muchii_date.index((y,x))
            muchii_date[poz].append(c)



    f.close()
    return n,m,muchii,muchii_date

def comp(x):
    return x[2]

def intializare(i): #varful i formeaza un arbore (o componenta/o multime)
    tata[i] = 0
    h[i] = 0

#cu compresie de cale
def reprezentant(i): #radacina arborelui
    if tata[i]==0:
        return i
    tata[i] = reprezentant(tata[i]) #compresia de cale
    return tata[i]

def reuniune(x,y): #reuniune ponderata
    rx=reprezentant(x)  #radacina arborelui care contine x
    ry=reprezentant(y) #radacina arborelui care contine y
    if h[rx]>h[ry]:   # h vine de la inaltime
        tata[ry] = rx
    else:
        tata[rx] = ry
        if h[rx] == h[ry]: #inaltimea arb rezultat se modifica doar daca arborii aveau aceeasi inaltime
            h[ry] += 1

def kruskal():
    muchii_apcm = []
    muchii.sort(key=comp) #sort(v,v+m,compara) compara(x,y) returneaza adevarat daca x<y
                          #sortam muchiile crescator dupa cost
    print(muchii)
    #initial - fiecare varf formeaza o componenta
    for i in range(1,n+1):
        intializare(i)
    nr_m = 0
    cost_total=0
    for x,y,c in muchii_date:
        if reprezentant(x)!=reprezentant(y):
            reuniune(x,y)
            muchii_apcm.append((x,y))
            nr_m += 1
            cost_total+=c
        else:
            return [],0

    for x,y,c in muchii:
        if reprezentant(x)!=reprezentant(y):
            reuniune(x,y)
            muchii_apcm.append((x,y))
            nr_m += 1
            cost_total += c
            if nr_m==n-1:
                return muchii_apcm,cost_total

n,m,muchii, muchii_date = citire("apm.in")
print (muchii)
tata = [0]*(n+1)
h = [0]*(n+1)
muchii_apcm,cost_total = kruskal()
f = open("apm.out", "w")
if len(muchii_apcm) != 0:
    f.write(str(cost_total)+"\n")
    f.write(str(n-1)+"\n")
    for x,y in muchii_apcm:
        f.write("("+str(x)+" "+str(y)+")" +"\n")
else:
    f.write("Muchiile date au fost respinse!" + "\n")