
'''
CS 370
Project 1
Alvin Johns 

In a production environment, any password greater than 16 would
be rejected.

The number of bits required to reach probability, P(k), where 

  k = the number of hash functions 
  n = number of expected insertions
  m = number of bits (the unknown)

is given by the formula:

  P(k) = (1 - e^((-kn)/m))^k

Setting P(k,n) to a desired amount, 0.01 for this example and solving
for m produces:

  m = (-kn) / ln(1 - (0.01)^(1/k))

This value, m, results in a number that is too much for my machine to compute
and fill in a bitarray. I am choosing a value for m between 100 and 1000.
'''

import sys
import time
import math
from bitarray import bitarray
# Non-crypto hash functions:
import mmh3 # https://pypi.org/project/mmh3/
import spookyhash # https://pypi.org/project/spookyhash/
import xxhash # https://pypi.org/project/xxhash/
import fnv # https://pypi.org/project/fnv/
import zlib # https://docs.python.org/3/library/zlib.html#module-zlib

def main():

  dict_file = open(sys.argv[1], encoding="unicode_escape")
  dict_content = dict_file.readlines()
  in_file = open(sys.argv[2], encoding="unicode_escape")
  in_content = in_file.readlines()
  outfile3 = open(sys.argv[3],'w')
  outfile5 = open(sys.argv[4], 'w')
  
  #############
  # Probability
  p = float(0.01)

  ###############################
  # Number of expected insertions
  n = int(in_content[0],base=10) 

  ################################################
  # Set the number of bits for desired probability.
  # Chosen based on previous explanation in this file.
  # Number of bits must be a whole number.
  #m_3 = math.ceil((-k_3 * n) / math.log(1 - (p ** (float(1 / k_3)))))
  #m_5 = math.ceil((-k_5 * n) / math.log(1 - (p ** (float(1 / k_5)))))
  # Since all hash functions have a range of 32 bits,
  # choosing a max value of 4294967295 / (number of hash functions)

  ##########################
  # Number of hash functions
  k_5 = 5 
  k_3 = 3
  m = 4294967295 
  m_3 = int(math.ceil((m / k_3)) / 1)
  m_5 = int(math.ceil((m / k_5)) / 1)

  '''
  m_3 = math.ceil((-k_3 * n) / math.log(1 - (p ** (float(1 / k_3)))))
  m_5 = math.ceil((-k_5 * n) / math.log(1 - (p ** (float(1 / k_5)))))
  print("bit count with 3 hash fns:", m_3)
  print("bit count with 5 hash fns:", m_5)
  print("insertion count:", n)
  print("probability:", p)
  '''

  ####################  
  # create a bit array 
  zeroes_3 = '0' * m_3
  bloom_filter_3 = bitarray(zeroes_3)
  zeroes_5 = '0' * m_5
  bloom_filter_5 = bitarray(zeroes_5)

  # bloom filter for passwords to be checked
  bf_3 = bitarray(zeroes_3)
  bf_5 = bitarray(zeroes_5)

  # flags for whether the password matches 
  maybe_3 = False
  maybe_5 = False

  #print(bloom_filter_3.buffer_info(),bloom_filter_5.buffer_info())

  ####################################################
  # Setup the hashes and fill in the bitarray for each
  # bad password using 3, then 5 hash functions.
  for word in dict_content:

    badpw = bytes(word.strip(), 'utf-8')

    h1 = zlib.adler32(badpw)
    h2 = mmh3.hash(badpw, signed=False)
    h3 = spookyhash.hash32(badpw)
    h4 = xxhash.xxh32(badpw).intdigest()
    h5 = fnv.hash(badpw, algorithm=fnv.fnv, bits=32) 

    # 3 hashes
    bloom_filter_3[h1 % m_3] = 1
    bloom_filter_3[h2 % m_3] = 1
    bloom_filter_3[h3 % m_3] = 1

    # 5 hashes
    bloom_filter_5[h1 % m_5] = 1
    bloom_filter_5[h2 % m_5] = 1
    bloom_filter_5[h3 % m_5] = 1
    bloom_filter_5[h4 % m_5] = 1
    bloom_filter_5[h5 % m_5] = 1
  # end of initial bloom filter to check against
  ##############################################

  ###############################################
  # match the password with list of bad passwords
  for word in in_content[1:]:
    pw = bytes(word.strip(), 'utf-8')

    h1 = zlib.adler32(pw)
    h2 = mmh3.hash(pw, signed=False)
    h3 = spookyhash.hash32(pw)
    h4 = xxhash.xxh32(pw).intdigest()
    h5 = fnv.hash(pw, algorithm=fnv.fnv, bits=32) 

    ##########
    # 3 hashes
    bf_3[h1 % m_3] = 1
    bf_3[h2 % m_3] = 1
    bf_3[h3 % m_3] = 1

    ############
    # time start
    t3_0 = time.perf_counter_ns() 
    # compare bloom filters
    if 1 == bloom_filter_3[h1 % m_3] and bf_3[h1 % m_3] == 1:
      if 1 == bloom_filter_3[h2 % m_3] and bf_3[h2 % m_3] == 1:
        if 1 == bloom_filter_3[h3 % m_3] and bf_3[h3 % m_3] == 1:
          maybe_3 = True
        else:
          maybe_3 = False
      else:
        maybe_3 = False
    else:
      maybe_3 = False
    # time end
    ##########

    t3_1 = time.perf_counter_ns()
    total_3 = t3_1 - t3_0

    # if maybe_3 is true, the word might be in 
    # the list of bad passwords.
    if maybe_3 == True:
      s = str(bytes(pw.strip()), 'utf-8') + " maybe " + str(total_3) + "\n"
      outfile3.write(s)
    else:
      s = str(bytes(pw.strip()), 'utf-8') + " no " + str(total_3) + "\n"
      outfile3.write(s)

    ##########
    # 5 hashes
    bf_5[h1 % m_5] = 1
    bf_5[h2 % m_5] = 1
    bf_5[h3 % m_5] = 1
    bf_5[h4 % m_5] = 1
    bf_5[h5 % m_5] = 1
 
    ############
    # time start
    t5_0 = time.perf_counter_ns() 
    # compare bloom filters
    if 1 == bloom_filter_5[h1 % m_5] and bf_5[h1 % m_5] == 1:
      if 1 == bloom_filter_5[h2 % m_5] and bf_5[h2 % m_5] == 1:
        if 1 == bloom_filter_5[h3 % m_5] and bf_5[h3 % m_5] == 1:
          if 1 == bloom_filter_5[h4 % m_5] and bf_5[h4 % m_5] == 1:
            if 1 == bloom_filter_5[h5 % m_5] and bf_5[h5 % m_5] == 1:
              maybe_5 = True
            else:
              maybe_5 = False
          else:
            maybe_5 = False
        else:
          maybe_5 = False
      else:
        maybe_5 = False
    else:
      maybe_5 = False
    # time end
    ##########

    t5_1 = time.perf_counter_ns()
    total_5 = t5_1 - t5_0

    # if maybe is true, the word might be in 
    # the list of bad passwords.
    if maybe_5 == True:
      s = str(bytes(pw.strip()), 'utf-8') + " maybe " + str(total_5) + "\n"
      outfile5.write(s)
    else:
      s = str(bytes(pw.strip()), 'utf-8') + " no " + str(total_5) + "\n"
      outfile5.write(s)
  # end of password matching
  ##########################


if __name__ == '__main__':
    main()
