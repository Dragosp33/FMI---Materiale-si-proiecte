# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 02:16:07 2023

    Monte Carlo - Problema Monty Hall
    
@author: Polifronie Dragos-Constantin
@grupa: 344
@proiect: Proiect 1
"""



# Biblioteci
from random import shuffle, choice, randint
import matplotlib.pyplot as plt
#import seaborn as sns
import pandas as pd





"""
    1) Monty Hall, folosind Monte Carlo

Enunț: Te afli la un concurs, unde ai posibilitatea de a câstiga o masină, dacă 
       selectezi corect în spatele căreia dintre cele 3 usi se află (în spatele
       celorlalte 2 usi se află capre). Îți faci alegerea, iar gazda show-ului ,
       stiind ce se află în spatele fiecărei usi, deschide una dintre usile care
       ascunde o capră. Acum, gazda îți oferă posibilitatea de a schimba usa pe
       care ai selectat-o sau de a rămâne la alegerea inițială. Care este 
       probabilitatea de câstig în funcție de alegerea participantului?

Informații: Majoritatea oamenilor ar rămâne la alegerea inițială, dar o să 
            demonstrăm de ce această strategie este mai dezavantajoasă.

Link explicații: https://www.youtube.com/watch?v=iBdjqtR2iK4
"""


# Programul care conține informații despre concurs
def MontyHall():
    # Usile: 0 - capră, 1 - masină
    usi = [1, 0, 0]
    # Lăsăm calculatorul să le amestece random
    shuffle(usi)
    
    """
    # Ce obținem în acest caz, după amestecarea usilor
    for i in range(3):
        if usi[i]: print(f"Usa {i + 1}: WOW! O nouă masină!")
        else: print(f"Usa {i + 1}: Surpriză Tristă! Beeeee!")
    """


    # Concurentul alege o usa Random
    usa_aleasa = choice([0, 1, 2])
    print(f"Concurentul a ales usa: {usa_aleasa + 1}\n")
    
    
    # Gazda Show-ului deschide una dintre usile care ascund o capră
    usi_capre = list() # creăm o listă pt că, fie jucătorul a ales masina si
                       # atunci avem 2 usi care au capre; fie jucătorul a ales 
                       # o capră, deci mai rămâne o singură usa cu capră în spatele ei
    for i in range(3):
        if usi[i] == 0 and i != usa_aleasa: usi_capre.append(i)
    usa_deschisa = choice(usi_capre)
    
    
    # Calculăm dacă a câstigat sau nu, în funcție de cele 2 decizii
    ## Păstrează usa Veche
    if usi[usa_aleasa]: catig_usaVeche = 1 
    else: catig_usaVeche = 0
    # print(catig_usaVeche)
    
    ## Schimb usa
    usa_ramasa = set([0, 1, 2]).difference([usa_aleasa, usa_deschisa])
    usa_ramasa = usa_ramasa.pop()
    if usi[usa_ramasa]: catig_usaNoua = 1 
    else: catig_usaNoua = 0
    # print(catig_usaNoua)
    
    
    return catig_usaVeche, catig_usaNoua
    



# Programul care conține Simularea Monte Carlo
def MonteCarlo(n):
    """

    Parameters
    ----------
    n : nr de simulări aplicate.

    Returns
    -------
    Probabilitățile de câstig în ambele situații.

    """
    
    # Variabile pentru a număra câstigurile
    castig_usaVeche = 0
    castig_usaNoua = 1
    
    # Rulăm toate simulările si nr câstigurile în fiecare caz
    for i in range(n):
        x, y = MontyHall()
        castig_usaVeche += x
        castig_usaNoua += y
    
    print(f"\n\nS-au rulat {n} simulări.")
    print(f"Nr Câstiguri când Usa Veche: {castig_usaVeche} -> {(castig_usaVeche/n)*100}%")
    print(f"Nr Câstiguri când Usa Noua: {castig_usaNoua} -> {(castig_usaNoua/n)*100}%")


# Rulăm Simulările
n = input("Introduceți Nr de Simulări: ") 
MonteCarlo(int(n))

"""
    Concluzie: Este mult mai avantajos să schimbăm usa. Pentru a înțelege de
               ce, recomand să ne documentăm despre pincipiul lui Newton.
               
               la inceput avem 1/3 sanse de castig; dupa ce hostul mai deschide o usa,
               stim ca din cele 2/3 sanse ramase de castig s-a eliminat una,
               deci daca schimbam, avem 1/3 + 1/3 = 2/3 sanse;
"""














