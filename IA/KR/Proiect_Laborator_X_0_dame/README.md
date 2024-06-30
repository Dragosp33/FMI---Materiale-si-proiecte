# KR - Proiect X si 0 cu capturi si window_of_4 - MinMax cu Alpha Beta

Proiect de laborator cu nota maxima; Un joc de X si 0 modificat;

Fiecare jucator incepe cu `buget=S`
Tabla initiala are notate numere de la 0 la 3, reprezentand bugetul care se va adauga jucatorului la plasarea unui simbol nou pe acea casuta.

Un jucator poate captura simbolul adversarului pe diagonala, sarind practic peste acesta, daca in urmatoarea casuta pe diagonala nu se afla niciun simbol ( casuta goala ) si bugetul acopera costul marcat pe acea casuta. Dupa capturare, adversarul nu poate plasa o casuta noua in pozitia eliminata ( se reseteaza la urmatorul turn ). Capturile se pot face in lant, intr-o singura mutare, daca sunt indeplinite conditiile si daca bugetul este de ajuns. `Cost_total_capturi += nr_captura_curenta * nr_pozitie `

Scopul este crearea unei ferestre de 4 simboluri

Pentru estimarile starilor folosite in algoritmul `Alpha-Beta` s-au luat in calcul formarea unor configuratii aproape finale - 3 simboluri si simbol adversar blocat - care duc la o stare finala imediata, si configuratii de cate 2 simboluri cu sau fara blocaj. Initial, cel mai mic factor pentru estimarea unei stari este diferenta dintre `buget_max * piese_max - buget_min * piese_min` pentru a incuraja calculatorul sa aleaga o pozitie care ii va mari bugetul, dar sa prefere in locul unei piese departate cu un buget mai mare, o configuratie cu 2 simboluri.

Astfel, capturarea are cel mai mare factor, ducand in cazul configuratiilor cu 3 simboluri direct la starea de castig.

# Run:

Utilizatorul este intrebat de numarul N care va denota gridul (matrice N\*N), Algoritmul folosit, Dificultatea care denota adancimea pana la care va merge algoritmul si simbolul cu care doreste sa inceapa.

In interfata grafica din pygame sunt desenate initial bugetele casutelor iar mai apoi se desfasoara jocul in mod normal. Daca jucatorul face click pe o un simbol propriu deja pus pe tabla (se va marca cu rosu), poate vedea ( marcate cu verde ) posibilitatile de capturare a pieselor adversare. Daca calculatorul face o captura, utilizatorului ii este aratata casuta care a fost eliminata cu o culoare gri ( aceasta casuta fiind blocata pentru aceasta runda.)
