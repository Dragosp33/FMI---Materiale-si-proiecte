# java_bank_app_scratch
O aplicatie simpla pentru un administrator de finante (exercitiu de imaginatie)

Structura aplicatiei:

Contul bancar care poate fi de 2 tipuri :  - savings
					   - checkings
Savings/Checkings vor fi 2 clase "extend" la clasa Account

Clasa customer va avea ca atribute (first,last)name si numar social(in cazul nostru, cnp)
dar si un obiect de tip cont bancar;


Clasa Banca (are ca atribut o lista de clienti)

iar clasa Menu este folosita (nume sugestiv) pentru interfata grafica si pentru a-i permite
utilizatorului sa interactioneze cu aplicatia.

//
/*
 In pachetul account sunt fisierele care tin de un cont bancar, indiferent de tipul lui 
 In Actiuni avem erorile in cazul unui tip de date invalid 
 iar pachetele Bank si Customer contin fiecare un singur fisier, cel care reprezinta clasa
 
*/
//



Utilizatorul poate introduce numele fisierelor care contin datele necesare (
Este nevoie de 1 fisier ce contine numele bancilor(structura: nrbanca, nume banca)
	       1 fisier ce contine datele despre conturile de savings(numar cont, balanta)
	       1 fisier ce contine datele despre conturile de checking(numar cont, balanta)
	       1 fisier ce contine datele despre clienti(nume,prenume,cont,ssn,nr.cont,Banca)

De altfel, utilizatorul poate introduce manual aceste date, prin actiunile din meniul interactiv
Sau poate direct sa apeleze actiunile din meniul interactiv pe datele deja stocate din fisiere;

Raportul actiunilor va fi facut intr-un fisier cu denumirea data de user la input.
Model:
Actiune,Timestamp
S-a facut o retragere in valoare de x din contul y,04/29/2022 22:01:03

PS: FileWriter.class este un thirdparty pentru a citi/scrie din/in fisiere

Fisierele csv (bank.csv, checking.csv, Customers.csv, savings.csv) sunt pentru datele de intrare
