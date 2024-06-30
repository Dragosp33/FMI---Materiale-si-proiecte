import copy

class Nod:
    L_MATRICE = 9
    L_CADRAN = 3
    NR_MAX = 9
    def __init__(self, info):
        self.info = info
        self.h = self.calc_h()


    def calc_h(self):
        M = self.info
        h = 0
        for linie in M:
            h+=linie.count("#")
        return h

    def testeaza_scop(self):

        M = self.info
        for linie in M:
            if linie.count("#") > 0:
                return 0
        return 1


class NodParcurgere:
    def __init__(self,  fisier=None, nodCurent=None):
        if nodCurent == None:
            f = open(fisier, "r")
            informatie = []
            for i in range(Nod.L_MATRICE):
                linie = f.readline().split()
                informatie.append(linie)

            nodCurent = Nod(informatie)

        self.nod = nodCurent
        self.g = 1
        self.f = self.g + self.nod.h

    def testeaza_valoare(self, i, j, value):
        square_i = (i // 3) * 3  # Calculate the starting row index of the 3x3 square
        square_j = (j // 3) * 3  # Calculate the starting column index of the 3x3 square

        #print("val lui self.nod.info in test valoare: "),
        #for linie in self.nod.info:
        #   print(linie)

        #for x in range()
        #return square_i, square_j
        #TODO:
        # de la square_i -> square_i + 3 si square_j -> square_j + 3
        for index1 in range(square_i, square_i+3):
            for index2 in range(square_j, square_j+3):
                if str(self.nod.info[index1][index2]) == str(value) :
                    return False

        for column in range(self.nod.L_MATRICE):
            if str(self.nod.info[i][column]) == str(value):
                return False

        # Check column
        for row in range(self.nod.L_MATRICE):
            if str(self.nod.info[row][j]) == str(value):
                return False
        #print("linia {} coloana {} nu are valoarea {} ".format(i, j, value))
        return True


    #def testeaza_mutare(self):


    def genereaza_succesori(self):
        l_succesori = []
        for i in range(self.nod.L_MATRICE):
            for j in range(self.nod.L_MATRICE):
                if self.nod.info[i][j] == "#":
                    M = copy.deepcopy(self.nod.info)
                    for valoare in range(1, 10):
                        if self.testeaza_valoare(i, j, valoare):
                            M[i][j] = valoare
                           # Nodnou = Nod(M)
                            l_succesori.append((NodParcurgere(nodCurent=Nod(M))))

        return l_succesori



def a_star(nrSolutiiCautate, fisier_input):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    cost = 0
   # c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
    c = [NodParcurgere(fisier=fisier_input)]


    while len(c) > 0:
        nodCurent = c.pop(0)

        for j in nodCurent.nod.info:
            print(j)
        print("\n----------------\n")
        if nodCurent.nod.testeaza_scop():
            print("Solutie: ")

            print("\n----------------\n")
            input()
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = nodCurent.genereaza_succesori()
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # diferenta fata de UCS e ca ordonez dupa f
                if c[i].f >= s.f:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)

a_star(1, fisier_input="input2.txt")

"""
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # diferenta fata de UCS e ca ordonez dupa f
                if c[i].f >= s.f:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)"""








