import sys
from bloom_filter2 import BloomFilter

def main():

    bloom = BloomFilter(max_elements=10000, error_rate=0.1)
    assert "test-key" not in bloom
    bloom.add("test-key")
    assert "test-key" in bloom

    '''
    dict_file = open(sys.argv[1], encoding="unicode_escape")
    in_file = open(sys.argv[2], encoding="unicode_escape")
    out_file_1 = sys.argv[3]
    out_file_2 = sys.argv[4]
    
    dict_content = dict_file.readlines()

    print(dict_content[0])
    '''

if __name__ == '__main__':
    main()
