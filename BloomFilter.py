import time
import hashlib

MIN_LEN = 4
My_HASH = 6
MAX_LEN = 32

class BloomFilter(object):

    def __init__(self, file="bloom_hashes.txt"):
        """
        Function to load the bloom hashes
        """

        with open(file, "r") as f:

            self.hashes = f.read().splitlines()
    
    def check_word(self, word):
        
        st = time.time()

        h = create_hash(word, My_HASH)

        print(h)
        if h in self.hashes:
            print(f"'{word}' may be in the set")
        else:
            print(f"'{word}' is not in the set")
        
        print(f"Bloom filter took {time.time() - st:.010f}s")
    
    def check_word_no_bloom(self, word):

        with open("usernames.txt", "r", encoding="utf-8") as f:

            lines = f.read().splitlines()
        
        st = time.time()
        if word in lines:
            print(f"No bloom: {word} in lines")

        print(f"No bloom filter took {time.time() - st:.010f}s")

    

def create_bloom_hash(data:list, maximum:int=My_HASH, output_file:str="bloom_hashes.txt"):
    """
    This function creates hashes from the data provided.
    Parameters:
    data (list): List of words to hash. 
    maximum (int): max length of the hash in bytes. Larger hashes increase accuracy, but increase memory usage. The maximum value is 32.
    output_file (str): Name of the file to output the hashes to.

    Returns:
    None
    """

    if not isinstance(data, (list, tuple)):
        raise TypeError("'data' must be an iterable")
    
    if not isinstance(maximum, int):
        raise TypeError("'maximum' must be an integer")
    
    if maximum not in range(MIN_LEN, MAX_LEN+1):
        raise ValueError(f"'maximum' must be an integer between {MIN_LEN}-{MAX_LEN}")

    if not isinstance(output_file, str):
        raise TypeError("'output_file' must be a string")

    hashes = set()
    for word in data:

        h = create_hash(word, maximum)
        hashes.add(h)
    
    hashes = list(hashes)
    hashes.sort()
    with open(output_file, "w") as f:
        f.writelines("\n".join(hashes))


def create_hash(word, length):

    m = hashlib.blake2b(digest_size=length)
    m.update(bytes(word, "utf-8"))
    return m.hexdigest()

def create():
    with open("usernames.txt", "r", encoding="utf-8") as f:

        to_hash = []
        lines = f.read().splitlines()

        for line in lines:

            if line.startswith("#"):
                line = f.readline()
                continue

            to_hash.append(line)
        
        create_bloom_hash(to_hash)


if __name__ == "__main__":

    # create()
    b = BloomFilter()
    b.check_word("TestyTesterson")
    b.check_word_no_bloom("TestyTesterson")