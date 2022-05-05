import sys
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from binascii import hexlify, unhexlify, b2a_hex
from base64 import b64encode, b64decode

plain_file = open(sys.argv[1])
plain_arr = plain_file.readlines()
plain = ' '.join([str(elem) for elem in plain_arr]).strip()
print(len(plain))

cipher_file = open(sys.argv[2])
cipher_arr = cipher_file.readlines()
cipher = ' '.join([str(elem) for elem in cipher_arr]).strip()
print("cipher:",cipher, len(cipher))

words_file = open(sys.argv[3])
words = words_file.readlines()

print("size:", len('a'.encode('utf-8')))

#iv = bytes(bytearray(16 * [0]))
iv = bytes(16 * b'\00')

print("iv:",iv, len(iv))

# key is less than 16 chars. check words.txt
for word in words[len(words) - 10:len(words)]:
#for word in words:
    # check the word
    if len(word) <= 16:
        sw = bytes(str(word).strip(), 'utf-8')
        ss = sw.decode('utf-8')
        #pad the word
        key = bytes(sw.ljust(16, b"\x20"))
        #print("key(bytes):",key,len(key))

        cipher1 = Cipher(algorithms.AES(key), modes.CBC(iv))

        encryptor = cipher1.encryptor()

        ct = encryptor.update(key) + encryptor.finalize()
        print(ct)

        s0 = hexlify(ct).decode('utf-8').strip()

        #decryptor = cipher1.decryptor()

        #decryptor = cipher1.decryptor()
        #print(decryptor.update(ct) + decryptor.finalize())

        if cipher1 == s0:
            print("okay")

        if cipher1 == cipher:
            print("okay")
         
        if s0 == cipher:
            print("ct:\t", s0)
            print("cipher:\t",cipher)

