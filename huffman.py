import array_list
import linked_list
import filecmp
from huffman_bits_io import *


# A HuffmanTree is either a:
# - A Huffman Tree Node
# - A Huffman Tree Leaf
# - None

# A Node is a Huffman Tree Node
class Node:
    def __init__(self, char, freq, left, right):
        self.char = char # A character that the Node represents
        self.freq = freq # An integer that corresponds to the frequency of the character in the text file.
        self.left = left # A reference to the right HuffmanTree
        self.right = right # A reference to the left HuffmanTree

    def __eq__(self, other):
        return type(other) == Node and self.char == other.char and self.freq == other.freq and self.left == other.left and self.right == other.right

    def __repr__(self):
        return "%r %r %r %r" % (self.char, self.freq, self.left, self.right)


# A Leaf is a Huffman Tree Leaf
class Leaf:
    def __init__(self, char, freq):
        self.char = char # A character that the Leaf represents
        self.freq = freq # An integer that corresponds to the frequency of the character in the text file.

    def __eq__(self, other):
        return type(other) == Leaf and self.char == other.char and self.freq == other.freq

    def __repr__(self):
        return "%r %r" % (self.char, self.freq)


# -> array list
# Create an array list for counting the occurrences of characters and return the list of occurances
def count_occurances(file_name):
    empty_lst = array_list.empty_list()
    empty_lst.array = [0] * 256
    empty_lst.capacity = 256
    character_lst = array_list.empty_list()
    character_lst.array = [0] * 256
    character_lst.capacity = 256
    file = open(file_name, "r")
    for line in file:
        for word in line:
            character_lst.array[ord(word)] += 1
    file.close()
    if empty_lst == character_lst:
        return array_list.empty_list()
    return character_lst


# HuffmanTree HuffmanTree -> boolean
# A Huffman tree a comes before Huffman tree b if the occurrence count of a is smaller than that of b
def comes_before(tree1, tree2):
    if tree1.freq == tree2.freq:
        return ord(tree1.char) < ord(tree2.char)
    return tree1.freq < tree2.freq


# HuffmanTree -> String
# creates a string from a given Huffman tree by traversing the tree in a pre-order traversal and appending the characters of the visited leaf nodes.
def pre_order_traversal(HuffmanTree, str=''):
    if type(HuffmanTree) != Leaf:
        if type(HuffmanTree.left) == Leaf:
            str += HuffmanTree.left.char
        str = pre_order_traversal(HuffmanTree.left, str)
        if type(HuffmanTree.right) == Leaf:
            str += HuffmanTree.right.char
        str = pre_order_traversal(HuffmanTree.right, str)
    return str


# HuffmanTree -> String
# creates a string from a given Huffman tree by traversing the tree in a pre-order traversal and appending the characters of the visited leaf nodes.
def bin_pre_order_traversal(HuffmanTree, str="", dir="", total=""):
    if type(HuffmanTree) != Leaf:
        if dir == "l":
            str += "0"
        if dir == "r":
            str += "1"
        total = bin_pre_order_traversal(HuffmanTree.left, str, "l", total)
        total = bin_pre_order_traversal(HuffmanTree.right, str, "r", total)
    else:
        if dir == "l":
            str += "0"
            total += ("|" + str)
        if dir == "r":
            str += "1"
            total += ("|" + str)
    return total


# ArrayList -> HuffmanTree
# builds a Huffman tree from a given list of occurrences of characters and returns the root of the tree
def build_huffman(OccuranceList):
    if OccuranceList == array_list.empty_list():
        return None
    huffman_linked_list = linked_list.empty_list()
    for index, occurance in enumerate(OccuranceList.array):
        if occurance != 0:
            temp_leaf = Leaf(chr(index), occurance) #figure out how to go from into to asciib
            huffman_linked_list = linked_list.insert_sorted(huffman_linked_list, temp_leaf, comes_before)
    while linked_list.length(huffman_linked_list) != 1:
        temp_leaf_1 = linked_list.get(huffman_linked_list, 0)
        temp_leaf_2 = linked_list.get(huffman_linked_list, 1)
        huffman_linked_list = linked_list.remove_list(huffman_linked_list, 0)
        huffman_linked_list = linked_list.remove_list(huffman_linked_list, 0)
        total_freq = temp_leaf_1.freq + temp_leaf_2.freq
        if comes_before(temp_leaf_1, temp_leaf_2):
            if ord(temp_leaf_1.char) < ord(temp_leaf_2.char):
                temp_node = Node(temp_leaf_1.char, total_freq, temp_leaf_1, temp_leaf_2)
            else:
                temp_node = Node(temp_leaf_2.char, total_freq, temp_leaf_1, temp_leaf_2)
        huffman_linked_list = linked_list.insert_sorted(huffman_linked_list, temp_node, comes_before)
    return huffman_linked_list.first


# HuffmanTree -> ArrayList
# Goes through the huffman tree via a preorder transversal and builds a huffman code for each character
def character_binary_conversion(HuffmanTree):
    #if type(HuffmanTree) is Leaf:
    #    return
    binary_lst = array_list.empty_list()
    char_lst = pre_order_traversal(HuffmanTree)
    #if len(char_lst) == 1:
    #    return binary_lst
    binary_lst.array = [None] * 256
    binary_lst.capacity = 256
    codes_lst = bin_pre_order_traversal(HuffmanTree).split("|")[1:]
    for index, leaf_char in enumerate(char_lst):
        binary_lst.array[ord(leaf_char)] = codes_lst[index]
    return binary_lst


# string string -> string
# reads an input text file and writes the compressed text into an output file, according to Huffman encoding.
def huffman_encode(input_string, output_string):
    input_file = open(input_string, "r")
    compressed_txt_string = ""
    occurance_lst = count_occurances(input_string)
    huffman_tree = build_huffman(occurance_lst)
    hb_writer = HuffmanBitsWriter(output_string)
    if huffman_tree is None:
        hb_writer.write_byte(0)
        hb_writer.close()
        input_file.close()
        return compressed_txt_string
    character_codes = character_binary_conversion(huffman_tree)
    if type(huffman_tree) is not Leaf:
        for line in input_file:
            for word in line:
                compressed_txt_string = compressed_txt_string + character_codes.array[ord(word)]
        hb_writer.write_byte(len(pre_order_traversal(huffman_tree)))
    else:
        hb_writer.write_byte(1)
        compressed_txt_string += huffman_tree.char
        for index, element in enumerate(occurance_lst.array):
            if element != 0:
                hb_writer.write_byte(index)
                hb_writer.write_int(element)
        hb_writer.close()
        input_file.close()
        return compressed_txt_string
    for index, element in enumerate(occurance_lst.array):
        if element != 0:
            hb_writer.write_byte(index)
            hb_writer.write_int(element)
    hb_writer.write_code(compressed_txt_string)
    hb_writer.close()
    input_file.close()
    return pre_order_traversal(huffman_tree)


# String String ->
# reads a compressed text file and writes the decompressed text into an output text file
def huffman_decode(input_string, output_string):
    decoded_str = ""
    file = open(output_string, "w")
    occurance_list = array_list.empty_list()
    occurance_list.capacity = 256
    occurance_list.array = [0] * 256
    hb_reader = HuffmanBitsReader(input_string)
    num_character = hb_reader.read_byte()
    if num_character == 0:
        try:
            ascii_val = hb_reader.read_byte()
        except:
            file.close()
            hb_reader.close()
            return decoded_str
        #decoded_str += chr(ascii_val)
        #file.write(decoded_str)
        #file.close()
        #return decoded_str
    for counter in range(num_character):
        ascii_val = hb_reader.read_byte()
        occurance = hb_reader.read_int()
        occurance_list.array[ascii_val] = occurance
    huffman_tree = build_huffman(occurance_list)
    num_char = huffman_tree.freq
    while len(decoded_str) != num_char:
       decoded_str += huffman_to_string(huffman_tree, hb_reader)
    file.write(decoded_str)
    file.close()
    hb_reader.close()
    return decoded_str


# HuffmanTree HBReader -> char
# Uses the HBReader object to traverse through the Huffman Tree and returns a character off of the HBReader object.
def huffman_to_string(HuffmanTree, hb_reader):
    if type(HuffmanTree) is Leaf:
        return HuffmanTree.char
    if hb_reader.read_bit() == 0:
        return huffman_to_string(HuffmanTree.left, hb_reader)
    return huffman_to_string(HuffmanTree.right, hb_reader)


import unittest


class TestCases(unittest.TestCase):
    def test_Node_class(self):
        leaf1 = Leaf("a", 3)
        leaf2 = Leaf("b", 7)
        node1 = Node("a", 10, leaf1, leaf2)
        node2 = Node("a", 10, leaf1, leaf2)
        self.assertEqual(node1.char, "a")
        self.assertEqual(node1.freq, 10)
        self.assertEqual(node1.left, leaf1)
        self.assertEqual(node1.right, leaf2)
        self.assertEqual(node1, node2)
        self.assertEqual(node1.__repr__(), "'a' 10 'a' 3 'b' 7")

    def test_Leaf_class(self):
        leaf1 = Leaf('a', 3)
        self.assertEqual(leaf1.char, "a")
        self.assertEqual(leaf1.freq, 3)
        self.assertEqual(leaf1.__repr__(), "'a' 3")

    def test_count_occurances(self):
        lst_occurance = array_list.empty_list()
        lst_occurance.array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 104, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        lst_occurance.capacity = 256
        self.assertEqual(count_occurances("test_text.txt"), lst_occurance)
        self.assertEqual(count_occurances("empty_text.txt"), array_list.empty_list())

    def test_comes_before(self):
        leaf1 = Leaf("a", 3)
        leaf2 = Leaf("b", 7)
        leaf3 = Leaf("c", 7)
        node1 = Node("a", 10, leaf1, leaf2)
        self.assertTrue(comes_before(leaf1, leaf2))
        self.assertFalse(comes_before(leaf2, leaf1))
        self.assertTrue(comes_before(leaf1, node1))
        self.assertTrue(comes_before(leaf2, leaf3))

    def test_pre_order_transversal(self):
        HT1 = Node(' ', 13,
                   Node(' ', 6,
                        Leaf(' ', 3),
                        Leaf('b', 3)),
                   Node('a', 7,
                        Node('c', 3,
                             Leaf('d', 1),
                             Leaf('c', 2)),
                        Leaf('a', 4)))
        self.assertEqual(pre_order_traversal(HT1), " bdca")

    def test_bin_pre_order_transversal(self):
        HT1 = Node(' ', 13,
                   Node(' ', 6,
                        Leaf(' ', 3),
                        Leaf('b', 3)),
                   Node('a', 7,
                        Node('c', 3,
                             Leaf('d', 1),
                             Leaf('c', 2)),
                        Leaf('a', 4)))
        HT2 = Node('a', 3,
                   Node('a',3,
                        Leaf('a', 1),
                        Leaf('b', 2)),
                   Leaf('c',3))
        self.assertEqual(bin_pre_order_traversal(HT1), "|00|01|100|101|11")
        self.assertEqual(bin_pre_order_traversal(HT2), "|00|01|1")

    def test_build_huffman(self):
        HT1 = Node(' ', 13,
                   Node(' ', 6,
                        Leaf(' ', 3),
                        Leaf('b', 3)),
                   Node('a', 7,
                        Node('c', 3,
                             Leaf('d', 1),
                             Leaf('c', 2)),
                        Leaf('a', 4)))
        HT2 = Leaf('a', 1)
        empty_lst = array_list.empty_list()
        self.assertEqual(build_huffman(count_occurances("test_ez.txt")), HT1)
        self.assertEqual(build_huffman(count_occurances("one_char_text.txt")), HT2)
        self.assertEqual(build_huffman(empty_lst), None)

    def test_character_binary_conversion(self):
        HT1 = Node(' ', 13,
                   Node(' ', 6,
                        Leaf(' ', 3),
                        Leaf('b', 3)),
                   Node('a', 7,
                        Node('c', 3,
                             Leaf('d', 1),
                             Leaf('c', 2)),
                        Leaf('a', 4)))
        char_lst = array_list.empty_list()
        char_lst.array = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, '00', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, '11', '01', '101', '100', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        char_lst.capacity = 256
        self.assertEqual(character_binary_conversion(HT1), char_lst)

    def test_encode(self):
        str1 = " bdca"
        str2 = ""
        str3 = "a"
        self.assertEqual(huffman_encode("file0_input.txt", "file0_output.txt"), str1)
        self.assertEqual(huffman_encode("empty_text.txt", "empty_text_encoded.txt"), str2)
        self.assertEqual(huffman_encode("one_char_text.txt", "one_char_text_encoded.bin"), str3)

    def test_huffman_to_string(self):
        HT1 = Node(' ', 13,
                   Node(' ', 6,
                        Leaf(' ', 3),
                        Leaf('b', 3)),
                   Node('a', 7,
                        Node('c', 3,
                             Leaf('d', 1),
                             Leaf('c', 2)),
                        Leaf('a', 4)))
        hb_reader = HuffmanBitsReader("file0_output.txt")
        num_character = hb_reader.read_byte()
        for counter in range(num_character):
            ascii_val = hb_reader.read_byte()
            occurance = hb_reader.read_int()
        self.assertEqual(huffman_to_string(HT1, hb_reader), 'a')
        self.assertEqual(huffman_to_string(HT1, hb_reader), 'b')
        hb_reader.close()

    def test_huffman_file_comp(self):
        huffman_encode("file0_input.txt", "file0_output.bin")
        huffman_decode("file0_output.bin", "decode_output.txt")
        huffman_encode("test_text.txt", "test_text_encoded.bin")
        huffman_decode("test_text_encoded.bin", "test_text_decoded.txt")
        huffman_encode("file1.txt", "file1_encoded.bin")
        huffman_decode("file1_encoded.bin", "file1_decoded.txt")
        #huffman_encode("prideandprejudice.txt", "prideandprejudice_encoding.txt")
        #huffman_decode("prideandprejudice_encoding.txt", "prideandprejudice_decoding.txt")
        self.assertTrue(filecmp.cmp('file0_input.txt', 'decode_output.txt'))
        self.assertTrue(filecmp.cmp('test_text.txt', 'test_text_decoded.txt'))
        self.assertTrue(filecmp.cmp('file1_encoded.bin', 'file1_encoded_soln.bin'))
        #self.assertTrue(filecmp.cmp("prideandprejudice.txt", "prideandprejudice_decoding.txt"))

    def test_blank_file(self):
        huffman_encode("empty_text.txt", "empty_text_encoded.bin")
        huffman_decode("empty_text_encoded.bin", "empty_text_decoded.txt")
        self.assertTrue(filecmp.cmp("empty_text.txt", "empty_text_decoded.txt"))
        self.assertTrue(filecmp.cmp("empty_text_encoded.bin", "file_blank_encoded_soln.bin"))

    def test_one_char_file(self):
        huffman_encode("one_char_text.txt", "one_char_text_encoded.bin")
        huffman_decode("one_char_text_encoded.bin", "one_char_text_decoded.txt")
        huffman_encode("file_one_char.txt", "file_one_char_encoded.bin")
        huffman_decode("file_one_char_encoded.bin", "file_one_char_decoded.txt")
        self.assertTrue(filecmp.cmp("one_char_text.txt", "one_char_text_decoded.txt"))
        self.assertTrue(filecmp.cmp("file_one_char_encoded.bin", "file_one_char_encoded_soln.bin"))
        self.assertTrue(filecmp.cmp("file_one_char.txt", "file_one_char_decoded.txt"))

    def test_one_char_multiple_file(self):
        huffman_encode("one_char_multiple_text.txt", "one_char_multiple_text_encoded.bin")
        huffman_decode("one_char_multiple_text_encoded.bin", "one_char_multiple_text_decoded.txt")
        self.assertTrue(filecmp.cmp("one_char_multiple_text.txt", "one_char_multiple_text_decoded.txt"))

    #def test_large_files(self):
    #    huffman_encode("file_WarAndPeace_intro.txt", "file_WarAndPeace_intro_encoded.bin")
    #    huffman_decode("file_WarAndPeace_intro_encoded.bin", "file_WarAndPeace_intro_decoded.txt")
    #    self.assertTrue(filecmp.cmp("file_WarAndPeace_intro_encoded.bin", "file_WarAndPeace_intro_encoded_soln.bin"))
    #    self.assertTrue(filecmp.cmp("file_WarAndPeace_intro.txt", "file_WarAndPeace_intro_decoded.txt"))

if __name__ == '__main__':
    unittest.main()


