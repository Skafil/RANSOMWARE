import os
from cryptography.fernet import Fernet
import socket

# Zmienne potrzebne od ustanowienia połączenia z klientem.
HOST = socket.gethostbyname(socket.gethostname()) # Wyslij na loopback.
PORT = 40445  # Wybrany losowo
BUFFER_SIZE = 4096
BYTEORDER_LENGTH = 8 # We don't need big buffer size to send size of file
FORMAT = "utf-8"


# Nawiąż połączenie z klientem.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5) # Nasłuchuj max 5 połączeń

def main():
    files = []
    secret_phase = "katanga"

    # Znajdź wszystkie pliki i wrzuć do listy poza pewnymi wyjątkami.
    for file in os.listdir():
        if (file == "decoding.py") or (file == "coding.py") or (file == "crypto_key.key")  or (file == "instrukcja.txt"):
            continue
        if os.path.isfile(file):
            files.append(file)

    # Serwer zaakceptował połączenie z klientem. Od tego momentu
    # Używamy zmiennej "conn" zamiast "s".
    conn, addr = s.accept()

    # (1) Odbierz klucz od klienta
    key = conn.recv(BUFFER_SIZE)
    
    # Zapisz klucz do pliku
    with open("crypto_key.key", "wb") as thekey:
        thekey.write(key)

    # (2) Odbierz słowo klucz od klienta.
    user_phase = conn.recv(BUFFER_SIZE).decode(FORMAT)
    # print("[i] Serwer krok (2). user_phase: ", user_phase)
    # print("[i] Serwer - secret_phrase: ", secret_phase)
    # print("[i] Serwer - porównanie phrase: ", secret_phase == user_phase)
    if user_phase == secret_phase:

        # (3) Potwierdz, ze podano dobre slowo klucz
        conn.send("ACK".encode(FORMAT))
        print("[+] Serwer - wyslano ACK (3)")

        # Odczytaj klucz z serwera
        with open("crypto_key.key", "rb") as thekey:
            key = thekey.read()

        # (4) Wyslij klucz do klienta
        conn.send(key)
        print("[+] Serwer - wyslano klucz (4)")
    
    else:
        # (3) Podano zle slowo klucz
        s.send('NACK'.encode(FORMAT))
        print("[-] Serwer - wyslano NACK (3)")
    
    conn.close()

main()