import copy
import time

# informatii despre un nod din arborele de parcurgere (nu nod din graful initial)
class NodParcurgere:
    def __init__(self, info,g=0, h=0,  parinte=None):
        self.info = info  # eticheta nodului, de exemplu: 0,1,2...
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g=g
        self.h=h
        self.f=g+h

    def drumRadacina(self):
        l = []
        nod = self
        while nod:
            l.insert(0, nod)
            nod = nod.parinte
        return l


    def vizitat(self): #verifică dacă nodul a fost vizitat (informatia lui e in propriul istoric)
        nodDrum = self.parinte
        while nodDrum:
            if (self.info == nodDrum.info):
                return True
            nodDrum = nodDrum.parinte

        return False

    def numaraFantome(self):
        cnt=0
        for stiva in self.info:
            for bloc in stiva:
                if bloc[0]=='b':
                    cnt+=1
        return cnt


    def sirAfisare(self):
        sir = ""
        maxInalt = max([len(stiva) for stiva in self.info])
        for inalt in range(maxInalt, 0, -1):
            for stiva in self.info:
                if len(stiva) < inalt:
                    sir += "   "
                else:
                    if len(stiva[inalt - 1])==2:
                        sir += stiva[inalt - 1] + " "
                    else:
                        sir += stiva[inalt - 1] + "  "
            sir += "\n"
        sir += "-" * (2 * len(self.info) - 1)
        sir += "\nCost pana acum: " + str(self.g) + "\n"
        #"Blocul neutru a plecat de pe stiva 0 pe stiva 4 cu costul 10. S-au distrus 2 fantome. Mai sunt 3 fantome."
        if self.parinte is not None:
            nrFantomeCurente=self.numaraFantome()
            nrFantomeParinte=self.parinte.numaraFantome()
            costMutare=nrFantomeCurente+ 1 if self.mutare[0]=="l" else 2
            print("Blocul {} a plecat de pe stiva {} pe stiva {} cu costul {}. S-au distrus {} fantome. Mai sunt {} fantome.".format(
                self.mutare[0],
                self.mutare[1] ,
                self.mutare[2],
                costMutare,
                nrFantomeParinte-nrFantomeCurente,
                nrFantomeCurente))
        return sir

    def __lt__(self, other):
        return self.f<other.f or self.f==other.f and self.g>other.g


    def __str__(self):
        return self.sirAfisare()

    def __repr__(self):
        return str(self.info)



class Graph:  # graful problemei

    def __init__(self,start):
        self.start = start  # informatia nodului de start

    def testeazaSuccesor(self, infoNod):
        cnt=0
        for stiva in infoNod:
            for bloc in stiva[::-1]:
                if bloc=="n":
                    cnt+=1
                elif bloc=="s":
                    break
        return cnt >= Graph.K


    # va genera succesorii sub forma de noduri in arborele de parcurgere
    def succesori(self, nodCurent):
        listaSuccesori = []
        for istiva, stiva in enumerate(nodCurent.info):
            if not stiva or stiva[-1] in ['bd', 'bs', 's']:
                continue
            copieStive=copy.deepcopy(nodCurent.info)
            bloc=copieStive[istiva].pop()
            if bloc=='l':
                costMutareBloc=1
            else:
                costMutareBloc = 2
            for istiva2, stiva2 in enumerate(copieStive):
                if istiva==istiva2 or (len(stiva2)>0 and stiva2[-1] in ['bd', 'bs']):
                    continue
                stareNoua=copy.deepcopy(copieStive)
                stareNoua[istiva2].append(bloc)
                stareFinalizata=copy.deepcopy(stareNoua)
                stareInvalida=False
                for istiva3, stiva3 in enumerate(stareNoua):
                    for ibloc3, bloc3 in enumerate(stiva3):
                        if bloc3=='bd':
                            if istiva3!= len(stareNoua)-1 and len(stareNoua[istiva3+1])>ibloc3:
                                if stareNoua[istiva3+1][ibloc3]=='l':
                                    stareFinalizata[istiva3][ibloc3]='l'
                                    stareFinalizata[istiva3+1][ibloc3] = 'bd'
                                else:
                                    stareInvalida = True
                            elif istiva3 > 0 and len(stareNoua[istiva3-1])>ibloc3 and stareNoua[istiva3-1][ibloc3]=='l':
                                if stareFinalizata[istiva3-1][ibloc3]=='l':
                                    stareFinalizata[istiva3][ibloc3]='l'
                                    stareFinalizata[istiva3-1][ibloc3] = 'bs'
                                elif stareFinalizata[istiva3-1][ibloc3][0]=='b':
                                    stareFinalizata[istiva3][ibloc3] = 'l'
                                    stareFinalizata[istiva3 - 1][ibloc3] = 'l'
                                else:
                                    stareInvalida=True
                        elif bloc3=='bs':
                            if istiva3 > 0 and len(stareNoua[istiva3-1])>ibloc3:
                                if stareNoua[istiva3-1][ibloc3]=='l':
                                    if stareFinalizata[istiva3-1][ibloc3]=='l':
                                        stareFinalizata[istiva3][ibloc3]='l'
                                        stareFinalizata[istiva3-1][ibloc3] = 'bs'
                                    elif stareFinalizata[istiva3-1][ibloc3][0]=='b':
                                        stareFinalizata[istiva3][ibloc3] = 'l'
                                        stareFinalizata[istiva3 - 1][ibloc3] = 'l'
                                    else:
                                        stareInvalida=True
                                elif stareNoua[istiva3-1][ibloc3] in ['n','s']:
                                    stareInvalida=True
                            elif istiva3!= len(stareNoua)-1 and len(stareNoua[istiva3+1])>ibloc3:
                                if stareNoua[istiva3+1][ibloc3]=='l':
                                    stareFinalizata[istiva3][ibloc3]='l'
                                    stareFinalizata[istiva3+1][ibloc3] = 'bd'
                                else:
                                    stareInvalida=True
                        if stareInvalida:
                            break
                    if stareInvalida:
                        break
                if stareInvalida:
                    continue
                for istiva3, stiva3 in enumerate(stareFinalizata):
                    for ibloc3, bloc3 in enumerate(stiva3):
                        if bloc3=='n':
                            if len(stiva3)>ibloc3+1 and stiva3[ibloc3+1][0]=='b':
                                stiva3[ibloc3]='s'
                            if ibloc3>0 and stiva3[ibloc3-1][0]=='b':
                                stiva3[ibloc3]='s'
                if not self.testeazaSuccesor(stareFinalizata):
                    continue
                nodNou=NodParcurgere(stareFinalizata, nodCurent.g+costMutareBloc, self.estimeaza_h(stareNoua),nodCurent )
                nodNou.g+=nodNou.numaraFantome()
                nodNou.mutare=(bloc, istiva,istiva2)
                if not nodNou.vizitat():
                    listaSuccesori.append(nodNou)
        return listaSuccesori

    def scop(self, infoNod):
        for st in infoNod:
            if all([e == 'n' for e in st]) and len(st)>=Graph.K :
                return True
        return False

    def estimeaza_h(self, infoNod):
        maxim=-1
        minim=9999999
        for stiva in infoNod:
            if all([e == 'n' for e in stiva]) :
                if maxim < len(stiva):
                    maxim=len(stiva)
            if not any([e == 's' for e in stiva]):
                if minim>len(stiva):
                    minim=len(stiva)
        if maxim !=-1:
            return 2*(Graph.K-maxim)
        else:
            return minim + 2*Graph.K











##############################################################################################
#                                 Initializare problema                                      #
##############################################################################################

def calculeazastive(listaConfig):
    return [st.strip().split() if st.strip()!='0' else [] for st in listaConfig]

f=open("input.txt", "r")
sirStart = f.read()
listeStart=sirStart.split('\n')
Graph.K=int(listeStart[0])
start=calculeazastive(listeStart[1:])
gr = Graph(start)
print(start)



def a_star(gr, nrSolutiiCautate):
    global noduriTot
    coada = [NodParcurgere( gr.start, 0, gr.estimeaza_h(gr.start))]
    noduri_inchise=[]
    noduriTot=1
    while len(coada) > 0:
        nodCurent = coada.pop(0)

        noduri_inchise.append(nodCurent)
        if gr.scop(nodCurent.info):
            print("Solutie: ")
            for nod in nodCurent.drumRadacina():
                print(str(nod), end="")
            print("\n----------------\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        noduriSuccesoare = gr.succesori(nodCurent)
        noduriTot+=len(noduriSuccesoare)
        #deja implementat: pentru fiecare succesor verificam ca se gaseste in coada si pastram nodul cel mai bun (cu f minim)
        for s in noduriSuccesoare:
            gasitC = False
            for nodC in coada:
                if s.info == nodC.info:
                    gasitC = True
                    if s.f >= nodC.f:
                        noduriSuccesoare.remove(s)
                    else:  # s.f<nodC.f
                        coada.remove(nodC)
                    break
            if not gasitC:
                for nodC in noduri_inchise:
                    if s.info == nodC.info:
                        if s.f >= nodC.f:
                            noduriSuccesoare.remove(s)
                        else:  # s.f<nodC.f
                            noduri_inchise.remove(nodC)
                        break

        coada.extend(noduriSuccesoare)
        coada.sort()
        #TO DO: ce ar trebui facut aici cu coada pentru a ramane ordonata dupa f?


# lSuccesori= gr.succesori(NodParcurgere( gr.start, 0, gr.estimeaza_h(gr.start)))
# print("================================================================")
# for x in lSuccesori:
#     print(x)
t1=time.time()
noduriTot=0
a_star(gr, nrSolutiiCautate=1)

t2=time.time()
print("Timp:", t2-t1)
print("Nr noduri", noduriTot)






