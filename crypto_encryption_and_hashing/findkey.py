import sys
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from binascii import hexlify, unhexlify, b2a_hex

plain = b'This is a top secret.\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b'

cipher_file = open(sys.argv[1])
cipher_arr = cipher_file.readlines()
cipher = ' '.join([str(elem) for elem in cipher_arr]).strip()
cipher = bytes.fromhex(cipher)

words_file = open(sys.argv[2])
words = words_file.readlines()

iv = 16 * b'\x00'

for word in words:
    if len(word) < 16:
           
        w = word.strip() 
        key = w.ljust(16)
        cipher1 = Cipher(algorithms.AES(bytes(key,'utf-8')), modes.CBC(iv))
        encryptor = cipher1.encryptor()
        ct = encryptor.update(plain) + encryptor.finalize()
        s0 = hexlify(ct).decode('utf-8').strip()
        decryptor = cipher1.decryptor()

        if cipher == ct:
            print("Found")
            print("original:\t",hexlify(cipher).decode('utf-8').strip())
            print("generated:\t",s0)
            print("keyword:\t",w)
            print("plain text:\t",decryptor.update(ct) + decryptor.finalize())
