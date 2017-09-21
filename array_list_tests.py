import unittest
from array_list import *


class TestList(unittest.TestCase):

    def test_class(self):
        list1 = List()
        self.assertEqual(list1.__repr__(), "10 0 [None, None, None, None, None, None, None, None, None, None]")

    def test_empty_list(self):
        list1 = List()
        self.assertEqual(empty_list(), list1)

    def test_add(self):
        list1 = List()
        list2 = List()
        list3 = List()
        list1.array = [1,2,3,4,5, None, None, None, None, None]
        list1.length = 5
        list2.array = [1, 2, 3, 1, 4, 5, None, None, None, None, None]
        list2.length = 6
        list2.capacity = 11
        list3.array = [0, 1, 2, 3, 1, 4, 5, None, None, None, None, None]
        list3.length = 7
        list3.capacity = 12
        self.assertEqual(add(list1, 3, 1), list2)
        self.assertEqual(add(list1, 0, 0), list3)
        self.assertRaises(IndexError, add, list1, -1, 0)

    def test_length(self):
        list1 = List()
        list2 = List()
        list2.length = 10
        self.assertEqual(length(list1), 0)
        self.assertEqual(length(list2), 10)

    def test_get(self):
        list1 = List()
        list2 = List()
        list1.array = [1,2,3,4,5, None, None, None, None, None]
        list1.length = 5
        self.assertEqual(get(list1, 3), 4)
        self.assertRaises(IndexError, get, list1, 15)

    def test_set(self):
        list1 = List()
        list2 = List()
        list1.array = [1,2,3,4,5, None, None, None, None, None]
        list2.array = [0,2,3,4,5, None, None, None, None, None]
        list1.length = 5
        list2.length = 5
        self.assertEqual(set(list1, 0, 0), list2)
        self.assertRaises(IndexError, set, list1, 100, 0)

    def test_remove(self):
        list1 = List()
        list2 = List()
        list3 = List()
        list4 = List()
        list1.array = [1,2,3,4,5, None, None, None, None, None]
        list1.length = 5
        list2.array = [1,3,4,5, None, None, None, None, None]
        list2.length = 4
        list2.capacity = 9
        list3.array = [5,4,3,None, None, None, None, None, None, None]
        list3.length = 3
        list4.array = [4, 3, None, None, None, None, None, None, None]
        list4.capacity = 9
        list4.length = 2
        tuple1 = (2, list2)
        tuple2 = (5, list4)
        self.assertEqual(remove(list1, 1), tuple1)
        self.assertRaises(IndexError, remove, list1, 5)
        self.assertRaises(IndexError, remove, list3, 3)
        self.assertEqual(remove(list3, 0), tuple2)

if __name__ == '__main__':
    unittest.main()
