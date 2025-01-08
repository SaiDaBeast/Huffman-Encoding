from huffman_bit_reader import *
from huffman_bit_writer import *
from ordered_list import *

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char   # stored as an integer - the ASCII character code value
        self.freq = freq   # the freqency associated with the node
        self.left = None   # Huffman tree (node) to the left
        self.right = None  # Huffman tree (node) to the right
        
    def __eq__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        if type(other) == HuffmanNode and self.freq == other.freq and self.char == other.char:
            return True
        return False
        
    def __lt__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        if type(other) == HuffmanNode:
            if self.freq < other.freq:
                return True
            elif self.freq == other.freq:
                return self.char < other.char
            else:
                return False



def cnt_freq(filename):
    '''Opens a text file with a given file name (passed as a string) and counts the 
    frequency of occurrences of all the characters within that file'''
    try:
        file = open(filename)
    except:
        raise FileNotFoundError
    lst = [0]*256
    for line in file:
        for char in line:
            lst[ord(char)] += 1
    file.close()
    return lst

def create_huff_tree(char_freq):
    '''Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree'''
    lst = OrderedList()
    for i in range(len(char_freq)):
        if char_freq[i] > 0:
            lst.add(HuffmanNode(i, char_freq[i]))
    while lst.size() > 1:
        first_node = lst.remove_by_index(0)
        second_node = lst.remove_by_index(0)
        if first_node.char < second_node.char:
            char = first_node.char
        else:
            char = second_node.char
        new_node = HuffmanNode(char, first_node.freq + second_node.freq)
        new_node.left = first_node
        new_node.right = second_node
        lst.add(new_node)
    if not lst.is_empty():
        return lst.head.next.item
    else:
        return None

def create_code(node):
    '''Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation 
    as the index into the arrary, with the resulting Huffman code for that character stored at that location'''
    lst = [""]*256
    create_code_helper(node, lst)
    return lst
    
def create_code_helper(node, lst, code=""):
    if not node == None:
        if node.left == None and node.right == None:
            lst[node.char] = code
        else:
            create_code_helper(node.left, lst, code + "0")
            create_code_helper(node.right, lst, code + "1")
            

def create_header(freqs):
    '''Input is the list of frequencies. Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return “97 3 98 4 99 2” '''
    str = ""
    for i in range(256):
        if freqs[i] > 0:
            str += f"{i} {freqs[i]} "
    return str.strip()

def huffman_encode(in_file, out_file):
    '''Takes inout file name and output file name as parameters - both files will have .txt extensions
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Also creates a second output file which adds _compressed before the .txt extension to the name of the file.
    This second file is actually compressed by writing individual 0 and 1 bits to the file using the utility methods 
    provided in the huffman_bits_io module to write both the header and bits.
    Take not of special cases - empty file and file with only one unique character'''
    #open both out files and process in file
    try:
        freq_list = cnt_freq(in_file)
    except:
        raise FileNotFoundError
    out_file_edited = open(out_file, "w")
    out_file_compressed = HuffmanBitWriter(out_file[:-4] + "_compressed" + out_file[-4:])
    
    #write header into both files
    header = create_header(freq_list)
    if len(header) > 0:
        out_file_edited.write(header + "\n")
        out_file_compressed.write_str(header + "\n")
    #create encoding tree
    huff_tree_root = create_huff_tree(freq_list)
    encode_array = create_code(huff_tree_root)\
    #create string of encoded bits
    coded_str = ""
    file = open(in_file)
    for line in file:
        for char in line:
            coded_str += encode_array[ord(char)]
    #write strings into both files
    out_file_edited.write(coded_str)
    out_file_compressed.write_code(coded_str)
    file.close()
    out_file_edited.close()
    out_file_compressed.close()
    
def huffman_decode(encoded_file, decode_file):
    try:
        in_file = open(encoded_file)
    except:
        raise FileNotFoundError
    out_file = open(decode_file, "w")
    
    bit_reader = HuffmanBitReader(encoded_file)
    header_string = bit_reader.read_str()
    freq_list = parse_header(header_string)
    root_node = create_huff_tree(freq_list)
    if root_node is not None:
        num_of_chars = root_node.freq
        for i in range(num_of_chars):
            curr_node = root_node
            while not (curr_node.left == None and curr_node.right == None):
                if bit_reader.read_bit():
                    curr_node = curr_node.right
                else:
                    curr_node = curr_node.left
            out_file.write(chr(curr_node.char))

    in_file.close()
    out_file.close()
    bit_reader.close()


    
def parse_header(header_string:str):
    lst = [0]*256
    tokens = header_string.split()
    i = 0
    while i < len(tokens):
        lst[int(tokens[i])] = int(tokens[i + 1])
        i += 2
    return lst



