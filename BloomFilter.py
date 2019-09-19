import io
import hashlib

DEFAULT_LENGTH = 1024 * 1024 # 1MB

class BloomFilter(object):

    def __init__(self, hash_length=DEFAULT_LENGTH):

        self.hash_length = hash_length
        self.vector = [0] * self.hash_length

    def add_bit_vector(self, vector):

        #check vector is binary string
        if set(vector) not in [{"1","0"}, {"0","1"}]:
            raise Exception("Vector must be a binary string")
        
        self.vector = list(vector)
        self.hash_length = len(vector)

    def add_strings_from_file(self, file_):

        if isinstance(file_, io.TextIOWrapper):
            f = file_

        elif isinstance(file_, str):
            f = open(file_, "r")

        else:
            raise Exception("file_ must be an open file pointer or a filename")
        
        for line in f.readlines():
            if " " in line or "," in line: # Handles lines with multiple words, including lines with commas
                self.add_strings([l for l in line.split() if l not in [" ", ","]])
                continue

            self.add_string(line)
        
    def add_strings(self, strings):

        for string in strings:
            self.add_string(string)
    
    def add_string(self, string):

        blake2 = self.get_blake2_hash(string)
        blake2_dec = self.get_blake2_value(string)

        self.vector[blake2_dec] = 1
    
    def get_blake2_value(self, string):

        blake2 = self.get_blake2_hash(string)

        return int(blake2, 16) % self.hash_length

    def get_blake2_hash(self, string):

        h = hashlib.blake2b()
        h.update(bytes(string, "utf-8"))

        return bytes(h.hexdigest(), "utf-8")

    def test_for_string(self, string):

        blake2 = self.get_blake2_value(string)

        if self.vector[blake2] == 1:
            print(f"{string} is possibly in the set")
        else:
            print(f"{string} is definitely not in the set")

    def __repr__(self):

        return "".join(str(b) for b in self.vector)

    def write_vector_to_file(self, fname):

        with open(fname, "w") as f:
            f.write(self.__repr__())



if __name__ == "__main__":

    bf = BloomFilter()

    bf.add_bit_vector(open("hash.txt", "r").readline())
    #bf.add_strings_from_file("usernames.txt")
    bf.write_vector_to_file("hash.txt")

    bf.test_for_string("NicoleB330")
    bf.test_for_string("cheese")


    #bf.add_strings("Hello world this is a bloom filter".split(" "))

    #bf.test_for_string("Hello")
    #bf.test_for_string("cheese")