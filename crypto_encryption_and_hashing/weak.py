from cryptography.hazmat.primitives import hashes
import random
import string

flag = False
count = 0

while flag == False:
    digest1 = hashes.Hash(hashes.SHA256())
    a = "abcdef"

    digest2 = hashes.Hash(hashes.SHA256())
    b1 = random.choice(string.ascii_letters)
    b2 = random.choice(string.ascii_letters)
    b3 = random.choice(string.ascii_letters)
    b4 = random.choice(string.ascii_letters)
    b5 = random.choice(string.ascii_letters)
    b6 = random.choice(string.ascii_letters)


    b = b1 + b2 + b3 + b4 + b5 + b6
    '''  
    if a != b:
        digest1.update(bytes(a, 'utf-8'))
        digest2.update(bytes(b, 'utf-8'))
    
        fin1 = digest1.finalize()
        fin2 = digest2.finalize()

        defend= fin1.hex()
        attack = fin2.hex()
        
        if defend[0:6] == attack[0:6]:
            flag = True
    '''
    digest1.update(bytes(a, 'utf-8'))
    fin = digest1.finalize()
    print(fin)

    flag = True

    count += 1

file = open("weak-results.txt", "a")
file.write(str(count) + "\n")
file.close()
