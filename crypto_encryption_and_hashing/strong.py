from cryptography.hazmat.primitives import hashes
import random
import string

flag = False
count = 0

while flag == False:
    digest1 = hashes.Hash(hashes.SHA256())
    a1 = "abcdef"
    a2 = "ghthiz"

    digest2 = hashes.Hash(hashes.SHA256())
    b1 = random.choice(string.ascii_letters)
    b2 = random.choice(string.ascii_letters)
    b3 = random.choice(string.ascii_letters)
    b4 = random.choice(string.ascii_letters)
    b5 = random.choice(string.ascii_letters)
    b6 = random.choice(string.ascii_letters)

    b = b1 + b2 + b3 + b4 + b5 + b6

    c1 = random.choice(string.ascii_letters)
    c2 = random.choice(string.ascii_letters)
    c3 = random.choice(string.ascii_letters)
    c4 = random.choice(string.ascii_letters)
    c5 = random.choice(string.ascii_letters)
    c6 = random.choice(string.ascii_letters)

    c = c1 + c2 + c3 + c4 + c5 + c6

    if b != c: 
        if a1 != b and a1 != c and a2 != b and a2 != c:
            digest1.update(bytes(a1, 'utf-8'))
            digest1.update(bytes(a2, 'utf-8'))

            digest2.update(bytes(b, 'utf-8'))
            digest2.update(bytes(c, 'utf-8'))
        
            fin1 = digest1.finalize()
            fin2 = digest2.finalize()

            defend= fin1.hex()
            attack = fin2.hex()
            
            if defend[0:6] == attack[0:6]:
                flag = True

    count += 1

file = open("strong-results.txt", "a")
file.write(str(count))
file.write("\n")
file.close()
