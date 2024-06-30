import secrets
import string

def funct1():
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(10))
        if (any(c.islower() for c in password)
                and any(c in string.punctuation for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)):
            break
    return password

print(funct1())
#poate fi folosit pentru a genera un cod random de acces

def funct2_URL(site):
    url = site
    url += "/"+secrets.token_urlsafe(30) + funct1() + secrets.token_hex(4)
    return url

print(funct2_URL("exemplu.com"))
#poate fi folosita la transmiterea unui link de recuperare a parolei/verificare a contului.


def funct3_token():
    return secrets.token_hex(32)

print(funct3_token())
#poate fi folosita pentru creearea unui id de sesiune;


#d)
a=input()
b=input()
print(secrets.compare_digest(a, b))


#e)
print(secrets.token_bytes(100))


#f)
import hashlib
parola_normala = "@admin!ADMIN@"
parola_hashuita = hashlib.sha256(parola_normala.encode('utf-8'))
print(parola_hashuita.hexdigest())


