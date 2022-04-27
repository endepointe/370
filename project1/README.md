
# Script files used
- bloomfilter.py
- bf3.py
- bf5.py

## Step 1: 
  Install the packages used

	pip3 install time bitarray mmh3 spookyhash xxhash fnv --user

## Step 2: 
  Run the python script

	python3 bloomfilter.py dictionary.txt sample_input.txt out3.txt out5.txt


### Note: 

	bloomfilter.py takes approx 1 minute to complete on flip. This is 
 	because I am contructing and filling two bloom filters in the same
	loop. This is only for Assignment submission purposes. 

	The writeup included with this submission contains screenshots to 
	each individual blooom filter with 3 and 5 hash functions, respectively.

	They run much faster when separated. Also, when run individually, the
  time to check for the hash 3 bloom filter is less than the time to 
  check for the hash 5 bloom filter.

	If you would like to run them yourself, change up the commandline
	arguments and run the following individually:
		
	python3 bf3.py dictionary.txt sample_input.txt out3.txt

	and	

	python3 bf5.py dictionary.txt sample_input.txt out5.txt	
