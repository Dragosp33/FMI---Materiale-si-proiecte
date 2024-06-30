#ex1:

start_state = [1, 0, 1, 1]
coeficienti = [0, 0, 1, 1]

lfsr = [1, 0, 1, 1]
period = 0


""""
while True:
    #taps: 16 15 13 4; feedback polynomial: x^16 + x^15 + x^13 + x^4 + 1
    bit = (lfsr ^ (lfsr >> 1) ^ (lfsr >> 3) ^ (lfsr >> 12)) & 1
    lfsr = (lfsr >> 1) | (bit << 15)
    period += 1
    if (lfsr == start_state):
        print(period)
        break
    """

print(lfsr)
while True:
    aux = lfsr
    for i in range(0, 3):
            lfsr[i] = aux[i+1]
    lfsr[3] = (aux[0] + aux[1]) % 2

    print(lfsr)
    if lfsr == start_state:
            break


#ex2


"""

    
    c) nu as recomanda modul acesta de folosire (mode_ecb) deoarece:
        este cel mai simplu si totodata cel mai slab mod de criptare dintre cele 
        disponibile in AES, intrucat fiecare block de text clar este criptat independent,
        putand fi gasite astfel corelatii intre blockurile de text
        
    d)    BLOCK-SIZE: FIXAT LA 16BYTES;
          dimensiunea cheii: 16bytes
    e)
"""



from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

key = b'o cheie oarecare'
cipher = AES.new(key, AES.MODE_EAX)
#initial:
#data = b'testtesttesttesttesttesttesttest'

datab = b'test'
cipher = AES.new(key, AES.MODE_ECB)
ct_bytes = cipher.encrypt(pad(datab, AES.block_size))

print(ct_bytes)

#cipher = AES.new(key, AES.MODE_ECB)
#data2 = cipher.encrypt(datab)

#print(data2)


#f)
#o alta implementare:
"""modulele clasice precum ebc, numite si "CBC"
    ofera protectie doar in ceea ce priveste confidentialitatea dar nu si integritatea,
    insemnand ca mesajul, desi vine critpat, poate fi alterat sau poate proveni din alte
    surse. Astfel, mai nou, au fost implementate noile metode numite "AEAD" pentru 
    a asigura atat confidentialitatea cat si integritatea.
    
    Pe langa textul criptat si un nonce - iv (vector de initializare) AEAD - urile 
    necesita si un tag - mac (de preferat hashuit si acesta)
    
    
    mai jos se foloseste modulul CCM - counter with cipher block chaining message authentication code
"""
import json
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

header = b"header"
data = b"secret"
key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_CCM)
cipher.update(header)
ciphertext, tag = cipher.encrypt_and_digest(data)

json_k = [ 'nonce', 'header', 'ciphertext', 'tag' ]
json_v = [ b64encode(x).decode('utf-8') for x in [cipher.nonce, header, ciphertext, tag] ]
result = json.dumps(dict(zip(json_k, json_v)))
print(result)

#######ex3:
from Crypto.Cipher import DES

key1 = b'\x10\x00\x00\x00\x00\x00\x00\x00'
key2 = b'\x20\x00\x00\x00\x00\x00\x00\x00'

cipher1 = DES.new(key1, DES.MODE_ECB)
cipher2 = DES.new(key2, DES.MODE_ECB)

plaintext = b'Provocare MitM!!'
ciphertext = cipher2.encrypt(cipher1.encrypt(plaintext))

print(ciphertext)


#### fie cele 2 functii pentru criptare:
def encodeText(k: int, text):
    key = format(k, 'x') + '\x00\x00\x00\x00\x00\x00\x00'
    cipher1 = DES.new(key.encode(), DES.MODE_ECB)
    return cipher1.encrypt(text)


def decodeText(k: int, text):
    key = format(k, 'x') + '\x00\x00\x00\x00\x00\x00\x00'
    cipher1 = DES.new(key.encode(), DES.MODE_ECB)
    return cipher1.decrypt(text)


## un algoritm pentru bruteforce:
def bruteForce(plaintext_result, ciphertext):
    for i in range(16):
        for j in range(16):
            plaintext = decodeText(j, decodeText(i, ciphertext))
            if plaintext == plaintext_result:
                return i, j
    return False

#16*16 chei; ideea algoritmului: dictionar de chei, vedem prin bruteforce care din combinatiile de chei
#vor corespunde cu textul criptat.