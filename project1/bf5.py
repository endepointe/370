
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
and fill in a bitarray. I am choosing a value for m based on a 32bit hash
function divided by the number of hash functions used in each bloom filter.

Size of bloom filter with:

  - 3 hash functions: 178956971 bytes (179 MB)

  - 5 hash functions: 107374183 bytes (108 MB)

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
  outfile5 = open(sys.argv[3], 'w')

  ############################################
  # Write the number of entries to output file
  outfile5.write(str(in_content[0]))

  print("Creating bloom filters... Please wait...")

  ###################################################
  # Since all hash functions have a range of 32 bits,
  # choosing a max value of:
  #           4294967295 / (number of hash functions)

  ##########################
  # Number of hash functions
  k_5 = 5
  m = 4294967295
  m_5 = math.ceil((m / k_5))

  ####################
  # create a bit array
  zeroes_5 = '0' * m_5
  bloom_filter_5 = bitarray(zeroes_5)

  ##########################################
  # bloom filter for passwords to be checked
  bf_5 = bitarray(zeroes_5)

  ########################################
  # flags for whether the password matches
  maybe_5 = False

  ###########################################
  # used to find the average time it takes to
  # check each password
  total_time_ns_5 = 0

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
    # 5 hashes
    bf_5[h1 % m_5] = 1
    bf_5[h2 % m_5] = 1
    bf_5[h3 % m_5] = 1
    bf_5[h4 % m_5] = 1
    bf_5[h5 % m_5] = 1

    ############
    # time start
    t5_0 = time.perf_counter()
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
    t5_1 = time.perf_counter()
    total_5 = t5_1 - t5_0
    total_time_ns_5 += total_5
    # time end
    ##########

    ########################################
    # if maybe is true, the word might be in
    # the list of bad passwords.
    if maybe_5 == True:
      s = str(bytes(pw.strip()), 'utf-8') + " maybe " + "\n"
      outfile5.write(s)
    else:
      s = str(bytes(pw.strip()), 'utf-8') + " no " + "\n"
      outfile5.write(s)
  # end of password matching
  ##########################

  print("Bloom filter created. To see the results, open:")
  in_count = len(dict_content)
  print("\t+", sys.argv[3])
  print("\t\t- bloom filter size:", bf_5.buffer_info()[1], "bytes")
  print("\t\t- hash count:", k_5)
  print("\t\t- bit count:", m_5)
  print("\t\t- input count:", in_count)
  p_5 = float(1 - (math.e ** ((-1*in_count*k_5)/m_5))) ** k_5
  print("\t\t- collision probability:",str(p_5))
  print("\t\t- average time to check:", float(total_time_ns_5 / in_count), "ns")

if __name__ == '__main__':
    main()
