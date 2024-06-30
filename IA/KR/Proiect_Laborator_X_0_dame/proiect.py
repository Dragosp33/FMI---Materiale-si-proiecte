import copy
import sys

import pygame
import time
import numpy as np
from random import randrange, randint



"""
Bazat pe implementarea jocului x si 0.
In loc de 0 (zero) am folosit o (o mic) pentru al doilea jucator
Deoarece aveam costurile de la 0 la 3 notate in patratele.
Costurile 0 nu le-am mai afisat in interfata grafica pentru a nu fi confundat cu simbolul jucatorului
De la 1 la 3 costurile (numerele din patratica goala) sunt afisate in interfata
"""


ADANCIME_MAX=3



def rand_nr(k):
	return randrange(k)

class Joc:
	"""
	Clasa care defineste jocul. Se va schimba de la un joc la altul.
	"""
	NR_COLOANE=5
	JMIN=None
	JMAX=None
	GOL='#'
	buget_JMAX = 10
	buget_JMIN = 10

	@classmethod
	def initializeaza(cls, display, NR_COLOANE=3, dim_celula=100):
		cls.display=display
		cls.dim_celula=dim_celula
		cls.x_img = pygame.image.load('ics.png')
		cls.zero_img = pygame.image.load('zero.png')
		cls.cost_unu_img = pygame.image.load('unu.png')
		cls.cost_doi_img = pygame.image.load('doi.png')
		cls.cost_trei_img=pygame.image.load('trei.png')

		cls.x_img = pygame.transform.scale(cls.x_img, (dim_celula, dim_celula))
		cls.zero_img = pygame.transform.scale(cls.zero_img, (dim_celula,dim_celula))
		cls.cost_unu_img = pygame.transform.scale(cls.cost_unu_img, (dim_celula, dim_celula))
		cls.cost_doi_img = pygame.transform.scale(cls.cost_doi_img, (dim_celula, dim_celula))
		cls.cost_trei_img = pygame.transform.scale(cls.cost_trei_img, (dim_celula, dim_celula))
		cls.celuleGrid=[] #este lista cu patratelele din grid
		for linie in range(Joc.NR_COLOANE):
			for coloana in range(Joc.NR_COLOANE):
				patr = pygame.Rect(coloana*(dim_celula+1), linie*(dim_celula+1), dim_celula, dim_celula)
				cls.celuleGrid.append(patr)

	def __init__(self, tabla=None, varianta='a', k=4, buget_JMIN=10, buget_JMAX=10):
		self.buget_JMAX = buget_JMAX
		self.buget_JMIN = buget_JMIN
		if tabla:
			self.matr = tabla

		else:
			self.matr = tabla or [randint(0, k-1) for _ in range(Joc.NR_COLOANE ** 2)]
			print(self.matr)


	# functie folosita in rularea jocului in interfata pentru a arata si valida capturile
	def gaseste_capturi(self, i):
		jucator = Joc.JMIN
		diagonale = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
		capturi = []

		for (di, dj) in diagonale:
			linie_i = i // Joc.NR_COLOANE
			col_i = i % Joc.NR_COLOANE

			# cate capturi am facut in lant
			n = 0
			copie_matr = copy.deepcopy(self.matr)

			# buget ramas
			buget = self.buget_JMIN if jucator == self.JMIN else self.buget_JMAX

			while (0 <= linie_i + di < Joc.NR_COLOANE and 0 <= col_i + dj < Joc.NR_COLOANE and buget >= 0):
				# daca nu e simbol opus iesim din loop
				if copie_matr[(linie_i + di) * Joc.NR_COLOANE + col_i + dj] != self.jucator_opus(jucator):
					break

				if not (0 <= linie_i + 2 * di < Joc.NR_COLOANE and 0 <= col_i + 2 * dj < Joc.NR_COLOANE):
					break

				if 0 <= linie_i + 2 * di < Joc.NR_COLOANE and 0 <= col_i + 2 * dj < Joc.NR_COLOANE:
					if copie_matr[(linie_i + 2 * di) * Joc.NR_COLOANE + col_i + 2 * dj] not in [0, 1, 2, 3]:
						break
					buget = buget - n * self.matr[(linie_i + 2 * di) * Joc.NR_COLOANE + col_i + 2 * dj]
					if buget >= 0:
						# punem 0 de unde mutam simbolul
						copie_matr[i] = 0
						# punem blocat_opus pt piesa capturata
						copie_matr[(linie_i + di) * Joc.NR_COLOANE + col_i + dj] = "_" + self.jucator_opus(jucator)
						# punem piesa jucatorului pe diagonala
						copie_matr[(linie_i + 2 * di) * Joc.NR_COLOANE + col_i + 2 * dj] = jucator

						# trimitem inapoi pozitiile noi, bugetul ramas, pozitia veche pt a verifica cu de_mutat
						# - poate avem posibilitatea de a captura o piesa din mai multe pozitii -
						# si tabla noua
						capturi.append({'position': (linie_i + 2 * di) * Joc.NR_COLOANE + col_i + 2 * dj, 'buget': buget, 'old': i, 'tabla_noua': copie_matr} )

						# adaugam 1 la capturi
						n += 1
						# avansam pe diagonala cu 2
						linie_i = linie_i + 2 * di
						col_i = col_i + 2 * dj
					else:
						break
		return capturi


	def deseneaza_grid(self, marcaj=None): # tabla de exemplu este ["#","x","#","0",......]

		for ind in range(len(self.matr)):
			linie=ind//Joc.NR_COLOANE # // inseamna div
			coloana=ind%Joc.NR_COLOANE

			if marcaj==ind:
				#daca am o patratica selectata, o desenez cu rosu
				# si calculez capturile
				culoare=(255,0,0)
				capturi = self.gaseste_capturi(ind)
				print("SE CAUTA CAPTURI:::: ", capturi)
				# deseneaza cu verde locul unde vom ateriza dupa capturi
				if capturi:
					for mark in capturi:
						culoare_verde = (0, 255, 128)
						pygame.draw.rect(self.__class__.display, culoare_verde, self.__class__.celuleGrid[mark['position']])
			else:
				#altfel o desenez cu alb
				culoare=(255,255,255)
			pygame.draw.rect(self.__class__.display, culoare, self.__class__.celuleGrid[ind]) #alb = (255,255,255)


			if self.matr[ind]=='x':
				self.__class__.display.blit(self.__class__.x_img,(coloana*(self.__class__.dim_celula+1),linie*(self.__class__.dim_celula+1)))
			elif self.matr[ind]=='o':
				self.__class__.display.blit(self.__class__.zero_img,(coloana*(self.__class__.dim_celula+1),linie*(self.__class__.dim_celula+1)))
			elif self.matr[ind]==1:
				self.__class__.display.blit(self.__class__.cost_unu_img, (
				coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
			elif self.matr[ind]==2:
				self.__class__.display.blit(self.__class__.cost_doi_img, (
				coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
			elif self.matr[ind] == 3:
				self.__class__.display.blit(self.__class__.cost_trei_img, (
					coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
			elif self.matr[ind] == "_"+Joc.JMIN:
				culoare_gri = (128, 128, 128)
				pygame.draw.rect(self.__class__.display, culoare_gri, self.__class__.celuleGrid[ind])
		#pygame.display.flip() # !!! obligatoriu pentru a actualiza interfata (desenul)
		pygame.display.update()

	@classmethod
	def jucator_opus(cls, jucator):
		return cls.JMAX if jucator == cls.JMIN else cls.JMIN


	def evaluare_windows_of_4(self):
		eval = 0
		eval += self.buget_JMAX * self.matr.count(self.JMAX) - self.buget_JMIN * self.matr.count(self.JMIN)

		for i in range(0, Joc.NR_COLOANE*(Joc.NR_COLOANE-1) - 1 ):
			if((i+1) % Joc.NR_COLOANE == 0 ):
				continue
			window  = [self.matr[i], self.matr[i+1], self.matr[Joc.NR_COLOANE + i], self.matr[Joc.NR_COLOANE + i+1]]

			##nu mai verificam pt 4 pt ca e stare finala.

			# window de 3 simboluri, fara simbol opus, si fara window blocat
			if(window.count(self.JMAX) == 3 and window.count(self.JMIN) == 0 and window.count("_"+self.JMAX) == 0):
				# daca avem captura facuta, deci opus blocat, scor f mare pt ca rezulta in win la urmatoarea miscare
				if(window.count("_"+self.JMIN)):
					eval+=300
				else:
					eval+=100

			#pt jmin avem -
			elif(window.count(self.JMIN) == 3 and window.count(self.JMAX) == 0 and window.count("_"+self.JMIN) == 0):
				# daca avem captura facuta, deci opus blocat, scor f mic pt ca rezulta in pierdere la urmatoarea miscare
				if (window.count("_" + self.JMAX)):
					eval -= 300
				else:
					eval -= 100

			#window de 2 - evaluare 20 daca am blocat un O, evaluare 10 altfel
			elif(window.count(self.JMAX) == 2 and window.count(self.JMIN) == 0 and window.count("_"+self.JMAX) == 0):
				if (window.count("_" + self.JMIN)):
					eval += 20
				else:
					eval += 10
			elif (window.count(self.JMIN) == 2 and window.count(self.JMAX) == 0 and window.count(
					"_" + self.JMIN) == 0):
				if (window.count("_" + self.JMIN)):
					eval -= 20
				else:
					eval -= 10
		return eval


	def final(self):
		# evaluare window de 4: i, i+1, i+N, i+N+1
		for i in range(0, Joc.NR_COLOANE*(Joc.NR_COLOANE-1) - 1 ):
			if((i+1) % Joc.NR_COLOANE == 0 ):
				continue
			if(self.matr[i] == self.matr[i+1] == self.matr[Joc.NR_COLOANE + i] == self.matr[Joc.NR_COLOANE + i + 1]):
				return self.matr[i]

		# daca mai sunt patratele cu cost 0 , 1 , 2 ,3 atunci nu e final
		if any(element in self.matr for element in [0,1,2,3]):
			return False
		else:
			return 'remiza'

	def mutari(self, jucator):  # jucator = simbolul jucatorului care muta
		l_mutari = []
		mutare_blocata = "_"+self.JMAX if jucator == Joc.JMAX else "_"+self.JMIN
		# punem o mutare blocata, pentru capturarea piesei
		for i in range(len(self.matr)):
			if self.matr[i] != Joc.JMIN and self.matr[i] != Joc.JMAX and self.matr[i] != mutare_blocata:
				copie_matr = copy.deepcopy(self.matr)
				copie_matr[i] = jucator
				buget_JMIN = self.buget_JMIN
				buget_JMAX = self.buget_JMAX

				# daca in casuta nu e int inseamna ca a fost capturat deci nu se adauga la buget
				if jucator == self.JMAX and isinstance(self.matr[i], int):
					buget_JMAX += self.matr[i]
				elif jucator == self.JMIN and isinstance(self.matr[i], int):
					buget_JMIN += self.matr[i]
				#new_vector = [new_value if x == old_value else x for x in vector]

				# stergem mutarile blocate.
				copie_matr = [0 if x == "_"+jucator else x for x in copie_matr]
				l_mutari.append(Joc(copie_matr, buget_JMAX=buget_JMAX, buget_JMIN=buget_JMIN))

			## capturi:

			elif self.matr[i] == jucator:

				diagonale = [(-1, -1), (1, -1), (1, 1), (-1, 1)]

				for (di, dj) in diagonale:
					linie_i = i // Joc.NR_COLOANE
					col_i = i % Joc.NR_COLOANE

					#cate capturi am facut in lant
					n = 0
					copie_matr = copy.deepcopy(self.matr)

					# buget ramas
					buget = self.buget_JMIN if jucator == self.JMIN else self.buget_JMAX

					while (0 <= linie_i+di < Joc.NR_COLOANE and 0 <= col_i+dj < Joc.NR_COLOANE and buget >= 0):
						# daca nu e simbol opus iesim din loop
						if copie_matr[(linie_i+di) * Joc.NR_COLOANE + col_i + dj] != self.jucator_opus(jucator):
							break

						if not(0 <= linie_i + 2 * di < Joc.NR_COLOANE and 0 <= col_i + 2 * dj < Joc.NR_COLOANE):
							break

						if 0 <= linie_i+2*di < Joc.NR_COLOANE and 0 <= col_i+2*dj < Joc.NR_COLOANE:
							if copie_matr[(linie_i+2*di) * Joc.NR_COLOANE + col_i+2*dj] not in [0, 1, 2, 3]:
								break
							buget = buget - n*self.matr[(linie_i+2*di) * Joc.NR_COLOANE + col_i+2*dj]
							if buget >= 0:
								# punem 0 de unde mutam simbolul
								copie_matr[i] = 0
								# punem blocat_opus pt piesa capturata
								copie_matr[(linie_i+di) * Joc.NR_COLOANE + col_i+dj] = "_"+self.jucator_opus(jucator)
								# punem piesa jucatorului pe diagonala
								copie_matr[(linie_i+2*di) * Joc.NR_COLOANE + col_i+2*dj] = jucator
								# stergem mutarile blocate. vom face o noua copie pt a pastra blocajele pt lant
								copie_secundara = copy.deepcopy(copie_matr)
								copie_secundara = [0 if x == "_" + jucator else x for x in copie_secundara]
								# extra copie aici pt ca nu s a terminat mutarea in cazul capturilor in lant


								if jucator == Joc.JMAX:
									l_mutari.append(Joc(copie_secundara, buget_JMAX=buget, buget_JMIN=self.buget_JMIN))
								else:
									l_mutari.append(Joc(copie_secundara, buget_JMAX=self.buget_JMAX, buget_JMIN=buget))

								# adaugam 1 la capturi
								n += 1
								# avansam pe diagonala cu 2
								linie_i = linie_i+2*di
								col_i = col_i+2*dj
							else:
								break



						# elimina simbol opus
						# schimba pozitia lui x
						# adauga la mutari; elimina si simbolurile proprii blocate.
						# continua pe aceeasi directie, poate avea mai multe capturi.




		#print("PRIMA MUTARE IN:::: " , l_mutari[0].matr)
		return l_mutari


	def estimeaza_scor(self, adancime):
		t_final = self.final()

		if t_final == self.__class__.JMAX:
			return (9999 + adancime)
		elif t_final == self.__class__.JMIN:
			return (-9999 - adancime)
		elif t_final == 'remiza':
			return 0
		else:
			#schimbare---
			return self.evaluare_windows_of_4()

	def sirAfisare(self):
		sir = "  |"
		sir += " ".join([str(i) for i in range(self.NR_COLOANE)]) + "\n"
		sir += "-" * (self.NR_COLOANE + 1) * 2 + "\n"
		for i in range(self.NR_COLOANE):  # itereaza prin linii
			sir += str(i) + " |" + " ".join(
				[str(x) for x in self.matr[self.NR_COLOANE * i: self.NR_COLOANE * (i + 1)]]) + "\n"
		# [0,1,2,3,4,5,6,7,8]
		return sir

	def __str__(self):
		return self.sirAfisare()

	def __repr__(self):
		return self.sirAfisare()


class NodArbore:
	"""
	Clasa folosita de algoritmii minimax si alpha-beta
	Are ca proprietate tabla de joc
	Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
	De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile in urma mutarii unui jucator
	"""

	def __init__(self, tabla_joc, j_curent, adancime, parinte=None, estimare=None):
		self.buget_JMAX = self.buget_JMIN = 10
		self.tabla_joc = tabla_joc
		self.j_curent = j_curent

		# adancimea in arborele de stari
		self.adancime = adancime

		# estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
		self.estimare = estimare

		# lista de mutari posibile din starea curenta
		self.mutari_posibile = []

		# cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
		self.stare_aleasa = None

	def mutari(self):
		l_mutari = self.tabla_joc.mutari(self.j_curent)
		juc_opus = Joc.jucator_opus(self.j_curent)
		l_stari_mutari = [NodArbore(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

		return l_stari_mutari

	def __str__(self):
		sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent + ")\n"
		sir += "\n" + "Buget MAX: " + str(self.tabla_joc.buget_JMAX) + "Buget MIN: " + str(self.tabla_joc.buget_JMIN)
		sir += "\n" + "Estimare Stare: " + str(self.estimare)
		return sir


""" Algoritmul MinMax """


def min_max(stare):
	if stare.adancime == 0 or stare.tabla_joc.final():
		stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
		return stare

	# calculez toate mutarile posibile din starea curenta
	stare.mutari_posibile = stare.mutari()

	# aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
	mutariCuEstimare = [min_max(mutare) for mutare in stare.mutari_posibile]

	if stare.j_curent == Joc.JMAX:
		# daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
		stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)
	else:
		# daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
		stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)
	stare.estimare = stare.stare_aleasa.estimare
	return stare


def alpha_beta(alpha, beta, stare):
	if stare.adancime == 0 or stare.tabla_joc.final():
		stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
		return stare

	if alpha > beta:
		return stare  # este intr-un interval invalid deci nu o mai procesez

	stare.mutari_posibile = stare.mutari()

	if stare.j_curent == Joc.JMAX:
		estimare_curenta = float('-inf')

		for mutare in stare.mutari_posibile:
			# calculeaza estimarea pentru starea noua, realizand subarborele
			stare_noua = alpha_beta(alpha, beta, mutare)

			if (estimare_curenta < stare_noua.estimare):
				stare.stare_aleasa = stare_noua
				estimare_curenta = stare_noua.estimare
			if (alpha < stare_noua.estimare):
				alpha = stare_noua.estimare
				if alpha >= beta:
					break

	elif stare.j_curent == Joc.JMIN:
		estimare_curenta = float('inf')

		for mutare in stare.mutari_posibile:

			stare_noua = alpha_beta(alpha, beta, mutare)

			if (estimare_curenta > stare_noua.estimare):
				stare.stare_aleasa = stare_noua
				estimare_curenta = stare_noua.estimare

			if (beta > stare_noua.estimare):
				beta = stare_noua.estimare
				if alpha >= beta:
					break
	stare.estimare = stare.stare_aleasa.estimare

	return stare


def afis_daca_final(stare_curenta):
	final = stare_curenta.tabla_joc.final()
	if (final):
		if (final == "remiza"):
			print("Remiza!")
		else:
			print("A castigat " + final)

		return True

	return False


# informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
	def __init__(self, info, parinte, cost=0, h=0):
		self.adancime = 0
		self.info = info
		self.parinte = parinte  # parintele din arborele de parcurgere
		self.g = cost  # consider cost=1 pentru o mutare
		self.h = h
		self.f = self.g + self.h

	def obtineDrum(self):
		l = [self];
		nod = self
		while nod.parinte is not None:
			l.insert(0, nod.parinte)
			nod = nod.parinte
		return l

	def afisDrum(self, afisCost=False, afisLung=False):  # returneaza si lungimea drumului
		l = self.obtineDrum()
		for i, nod in enumerate(l):
			print(i + 1, ")\n", str(nod), sep="")
		if afisCost:
			print("Cost: ", self.g)
		if afisCost:
			print("Lungime: ", len(l))
		return len(l)

	def contineInDrum(self, infoNodNou):
		nodDrum = self
		while nodDrum is not None:
			if (infoNodNou == nodDrum.info):
				return True
			nodDrum = nodDrum.parinte

		return False

	def __repr__(self):
		sir = ""
		sir += str(self.info)
		return (sir)

	# euristica banală: daca nu e stare scop, returnez 1, altfel 0

	def __str__(self):
		sir = ""
		for linie in self.info:
			sir += " ".join([str(elem) for elem in linie]) + "\n"
		sir += "\n"
		return sir



class Graph: #graful problemei
	def __init__(self, nume_fisier):
		f=open(nume_fisier, "r")
		sirFisier=f.read()
		try:
			listaLinii=sirFisier.strip().split("\n")
			self.start=[]
			for linie in listaLinii:
				self.start.append([int(x) for x in linie.strip().split(" ")])
			print(self.start)
			#verificarea corectitudinii starii de start
			#self.scopuri=[  [[1,2,3],[4,5,6],[7,8,0]]  ]
			#print(self.scopuri)
		except:
			print("Eroare la parsare!")
			sys.exit(0) #iese din program


	# ca scop avem : nicio miscare pe diagonala nu mai e posibila
	def testeaza_scop(self, nodCurent):
		i = nodCurent.info.pozitie
		linie_i = i // Joc.NR_COLOANE
		col_i = i % Joc.NR_COLOANE
		diagonale = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
		# daca gasim o diagonala cu captura, nu e scop.
		for (di, dj) in diagonale:
			if 0 <= linie_i+di < Joc.NR_COLOANE and 0 <= col_i+dj < Joc.NR_COLOANE and nodCurent.info.buget >= 0:
				if 0 <= linie_i+2*di < Joc.NR_COLOANE and 0 <= col_i+2*dj < Joc.NR_COLOANE:
					if nodCurent.info.matr[(linie_i+di) * Joc.NR_COLOANE + dj] == Joc.jucator_opus(nodCurent.info.jucator):
						if nodCurent.info.matr[(linie_i + 2*dj) * Joc.NR_COLOANE + 2*dj] in [0, 1, 2, 3]:
							if nodCurent.info.buget >= nodCurent.adancime * nodCurent.info.matr[(linie_i+di) * Joc.NR_COLOANE + dj]:
								return False
		return True


	#va genera succesorii sub forma de noduri in arborele de parcurgere


	def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):
		listaSuccesori=[]
		poz = nodCurent.info.pozitie_piesa

		linie_i = poz // Joc.NR_COLOANE
		col_i = poz % Joc.NR_COLOANE

		#stanga, dreapta, sus, jos
		#directii=[[poz, cGol-1],[lGol, cGol+1], [lGol-1, cGol], [lGol+1, cGol] ]

		diagonale = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
		piesa_blocata = "_"+Joc.JMIN if nodCurent.info.jucator == Joc.JMAX else "_"+Joc.JMAX
		for di, dj in diagonale:
			if 0 <= linie_i+di < Joc.NR_COLOANE and 0 <= col_i+dj < Joc.NR_COLOANE and nodCurent.info.buget >= 0:
				if 0 <= linie_i+2*di < Joc.NR_COLOANE and 0 <= col_i+2*dj < Joc.NR_COLOANE:
					if nodCurent.info.matr[(linie_i+di) * Joc.NR_COLOANE + dj] == Joc.jucator_opus(nodCurent.info.jucator):
						if nodCurent.info.matr[(linie_i + 2 * dj) * Joc.NR_COLOANE + 2 * dj] in [0, 1, 2, 3]:
							if nodCurent.info.buget >= (nodCurent.adancime +1) * nodCurent.info.matr[(linie_i+di) * Joc.NR_COLOANE + dj]:
								copieMatrice=copy.deepcopy(nodCurent.info.matr)
								copieMatrice[(linie_i+di) * Joc.NR_COLOANE + dj] = piesa_blocata
								copieMatrice[(linie_i + 2*di) * Joc.NR_COLOANE + 2*dj] = nodCurent.info.jucator

								if not nodCurent.contineInDrum(
										copieMatrice):  # and not self.nuAreSolutii(copieMatrice):
									costArc = nodCurent.info.matr[(linie_i+di) * Joc.NR_COLOANE + dj] * (nodCurent.adancime + 1)
									listaSuccesori.append(NodParcurgere(copieMatrice, nodCurent, nodCurent.g + costArc,
																		self.calculeaza_h(copieMatrice, tip_euristica)))







raspuns_valid = False
while not raspuns_valid:
	try:
		x = int(input("N = ? ; 5 <= N <= 10; "))
		print("N = ", x)
		if 5 <= x <= 10:
			raspuns_valid = True
		else:
			print("N trebuie sa fie intre 5 si 10")
	except:
		print("N trebuie sa fie un numar. Intre 5 si 10.")





# initializare algoritm
raspuns_valid = False
while not raspuns_valid:
	tip_algoritm = input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
	if tip_algoritm in ['1', '2']:
		raspuns_valid = True
	else:
		print("Nu ati ales o varianta corecta.")


# initializare adancime
raspuns_valid = False
while not raspuns_valid:
	dificultate = input("Dificultate? (raspundeti cu 1, 2 sau 3)\n 1.Usor\n 2.Mediu\n 3.Greu\n")
	if dificultate in ['1', '2', '3']:
		raspuns_valid = True
	else:
		print("Nu ati ales o varianta corecta.")
# initializare jucatori
raspuns_valid = False
while not raspuns_valid:
	Joc.JMIN = input("Doriti sa jucati cu x sau cu o? ").lower()
	if (Joc.JMIN in ['x', 'o']):
		raspuns_valid = True
	else:
		print("Raspunsul trebuie sa fie x sau o (nu zero).")
Joc.JMAX = 'o' if Joc.JMIN == 'x' else 'x'

if dificultate == '1':
	ADANCIME_MAX = 2
elif dificultate == '2':
	ADANCIME_MAX = 3
elif dificultate == '3':
	ADANCIME_MAX = 5


####################################### initializare tabla
Joc.NR_COLOANE = x
tabla_curenta = Joc()
print("Tabla initiala")
print(str(tabla_curenta))
print("JOC.COLOANE = ", Joc.NR_COLOANE)



# creare stare initiala
stare_curenta = NodArbore(tabla_curenta, 'x', ADANCIME_MAX)

# setari interf grafica
pygame.init()
pygame.display.set_caption('x si 0')
# dimensiunea ferestrei in pixeli
# dim_celula=..
ecran = pygame.display.set_mode(
	size=(x*100+(x-1), x*100+(x-1)))  # N *100+ (N-1)*dimensiune_linie_despartitoare (dimensiune_linie_despartitoare=1)
Joc.initializeaza(ecran)

de_mutat = False
tabla_curenta.deseneaza_grid()
capturi_posibile = []
#j_curent = Joc.JMIN
while True:

	if (stare_curenta.j_curent == Joc.JMIN):

		# muta jucatorul
		# [MOUSEBUTTONDOWN, MOUSEMOTION,....]
		# l=pygame.event.get()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()  # inchide fereastra
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:  # click

				pos = pygame.mouse.get_pos()  # coordonatele clickului

				for np in range(len(Joc.celuleGrid)):

					if Joc.celuleGrid[np].collidepoint(
							pos):  # verifica daca punctul cu coord pos se afla in dreptunghi(celula)
						# linia si coloana celulei pe care am facut click
						linie = np // Joc.NR_COLOANE
						coloana = np % Joc.NR_COLOANE
						###############################
						if stare_curenta.tabla_joc.matr[np] == Joc.JMIN:
							if (de_mutat and linie == de_mutat[0] and coloana == de_mutat[1]):
								# daca am facut click chiar pe patratica selectata, o deselectez
								# vezi daca putem face capturi
								de_mutat = False
								stare_curenta.tabla_joc.deseneaza_grid()
							else:
								de_mutat = (linie, coloana)
								# desenez gridul cu patratelul marcat
								# afiseaza si patratelele pt capturi
								capturi_posibile = stare_curenta.tabla_joc.gaseste_capturi(np)
								stare_curenta.tabla_joc.deseneaza_grid(np)



						elif stare_curenta.tabla_joc.matr[np] != 'o' and stare_curenta.tabla_joc.matr[np] != 'x' and stare_curenta.tabla_joc.matr\
								[np] != ('_'+Joc.JMIN):
							if de_mutat:
								#### eventuale teste legate de mutarea simbolului
								print("de mutat on")
								if np not in [captura['position'] for captura in capturi_posibile]:
									print("NU POTI MUTA SIMBOLUL AICI! Trebuie captura si destul buget.")
									print("np= ", np, capturi_posibile)
									print("Click pe o piesa pentru a vedea capturile posibile, fiind marcata cu verde "
										  "pozitia finala a propriului simbol.")
									continue
								else:
									buget_nou = stare_curenta.tabla_joc.buget_JMIN
									tabla = stare_curenta.tabla_joc.matr

									for captura in capturi_posibile:
										if np == captura["position"] and (de_mutat[0]*Joc.NR_COLOANE + de_mutat[1]) == captura["old"]:
											buget_nou = captura["buget"]
											tabla = captura["tabla_noua"]
											break

									#stare_curenta.tabla_joc.matr[np] = Joc.JMIN
									#stare_curenta.tabla_joc.matr[de_mutat[0] * Joc.NR_COLOANE + de_mutat[1]] = 0
									#stare_curenta.tabla_joc =
									stare_curenta.tabla_joc.matr = tabla
									stare_curenta.tabla_joc.buget_JMIN = buget_nou
									de_mutat = False
							#	stare_curenta.tabla_joc.matr[de_mutat[0] * x + de_mutat[1]] = Joc.GOL
							#	de_mutat = False


							else:
								print("SHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
								stare_curenta.tabla_joc.buget_JMIN += stare_curenta.tabla_joc.matr[np]
								# plasez simbolul pe "tabla de joc"
								stare_curenta.tabla_joc.matr[linie * Joc.NR_COLOANE + coloana] = Joc.JMIN
							# sterg pozitiile blocate:
							stare_curenta.tabla_joc.matr = [x if x != "_"+Joc.JMIN else 0 for x in stare_curenta.tabla_joc.matr]

							# afisarea starii jocului in urma mutarii utilizatorului
							print("\nTabla dupa mutarea jucatorului")
							print(str(stare_curenta))

							stare_curenta.tabla_joc.deseneaza_grid()
							# testez daca jocul a ajuns intr-o stare finala
							# si afisez un mesaj corespunzator in caz ca da
							if (afis_daca_final(stare_curenta)):
								break

							# S-a realizat o mutare. Schimb jucatorul cu cel opus
							stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
							#print(stare_curenta.mutari()[0].tabla_joc)
	# --------------------------------
	else:  # jucatorul e JMAX (calculatorul)
		print(str(stare_curenta))
		# Mutare calculator

		# preiau timpul in milisecunde de dinainte de mutare
		#print(stare_curenta.mutari()[0].tabla_joc)
		t_inainte = int(round(time.time() * 1000))
		if tip_algoritm == '1':
			stare_actualizata = min_max(stare_curenta)
		else:  # tip_algoritm==2
			stare_actualizata = alpha_beta(-1000, 1000, stare_curenta)
		stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
		print("Tabla dupa mutarea calculatorului")
		print(str(stare_curenta))

		stare_curenta.tabla_joc.deseneaza_grid()
		# preiau timpul in milisecunde de dupa mutare
		t_dupa = int(round(time.time() * 1000))
		print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

		if (afis_daca_final(stare_curenta)):
			break

		# S-a realizat o mutare. Schimb jucatorul cu cel opus
		stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)


while True :
		for event in pygame.event.get():
			if event.type== pygame.QUIT:
				pygame.quit()
				sys.exit()