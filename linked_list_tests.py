import unittest
from linked_list import *


class TestList(unittest.TestCase):
    # Note that this test doesn't assert anything! It just verifies your
    #  class and function definitions.
    def test_interface(self):
        temp_list = empty_list()
        temp_list = add(temp_list, 0, "Hello!")
        length(temp_list)
        get(temp_list, 0)
        temp_list = set(temp_list, 0, "Bye!")
        remove(temp_list, 0)

    def test_class(self):
        list1 = Pair(1, Pair(2, Pair(3, None)))
        self.assertEqual(list1.__repr__(), "1 2 3 None")

    def test_empty_list(self):
        self.assertEqual(empty_list(), None)

    def test_add(self):
        temp_list = empty_list()
        list1 = Pair(1, Pair(2, Pair(3, None)))
        list2 = Pair(1, Pair(2, Pair(4, Pair(3, None))))
        list3 = Pair(1, Pair(2, Pair(3, Pair(4, None))))
        list4 = Pair(1, Pair(2, Pair(3, Pair(5, Pair(4, None)))))
        list5 = Pair(0, Pair(1, Pair(2, Pair(3, None))))
        list6 = Pair(1, Pair(0, Pair(2, Pair(3, None))))
        self.assertEqual(add(temp_list, 0, "hello"), Pair("hello", None))
        self.assertEqual(add(list1, 1, 0), list6)
        self.assertEqual(add(list1, 2, 4), list2)
        self.assertEqual(add(list3, 3, 5), list4)
        self.assertEqual(add(list1, 0, 0), list5)
        self.assertRaises(IndexError, add, list1, -1, "hello")

    def test_length(self):
        emptylist = empty_list()
        list1 = Pair(1, Pair(2, Pair(3, None)))
        self.assertEqual(length(list1), 3)
        self.assertEqual(length(emptylist), 0)

    def test_get(self):
        emptylist = empty_list()
        list1 = Pair(1, Pair(2, Pair(3, None)))
        self.assertEqual(get(list1, 2), 3)
        self.assertRaises(IndexError, get, emptylist, 0)

    def test_set(self):
        emptylist = empty_list()
        list1 = Pair(1, Pair(2, Pair(3, None)))
        list2 = Pair(1, Pair(6, Pair(3, None)))
        self.assertEqual(set(list1, 1, 6), list2)
        self.assertRaises(IndexError, set, emptylist, 0, "hello")

    def test_remove(self):
        emptylist = empty_list()
        list1 = Pair(1, Pair(2, Pair(3, None)))
        tuple1 = (2, Pair(1, Pair(3, None)))
        list2 = Pair(1, Pair(2, Pair(3, Pair(4, None))))
        tuple2 = (4, Pair(1, Pair(2, Pair(3, None))))
        self.assertRaises(IndexError, remove, emptylist, 0)
        self.assertEqual(remove(list1, 1), tuple1)
        self.assertEqual(remove(list2, 3), tuple2)

    def test_remove_ele(self):
        list1 = Pair(1, Pair(2, Pair(3, Pair(4, None))))
        int1 = 2
        self.assertEqual(remove_ele(list1, 1), int1)
        self.assertRaises(IndexError, remove_ele, list1, -1)

    def test_remove_list(self):
        list1 = Pair(1, Pair(2, Pair(3, Pair(4, None))))
        list2 = Pair(1, Pair(3, Pair(4, None)))
        self.assertEqual(remove_list(list1, 1), list2)
        self.assertRaises(IndexError, remove_list, list1, -1)

    def test_foreach(self):
        list1 = Pair(1, Pair(2, Pair(3, Pair(4, None))))
        list2 = list1
        list2 = foreach(list2, add_one)
        self.assertEqual(list2, None)

    #def test_add_one(self):
    #    value = 0
    #    self.assertEqual(add_one(value), 1)

    def test_insert(self):
        list1 = Pair(1, Pair(2, Pair(4, Pair(5, None))))
        list2 = Pair(1, Pair(2, Pair(3, Pair(4, Pair(5, None)))))
        list3 = Pair(-199, Pair(-2, Pair(1, Pair(5, None))))
        list4 = Pair(-199, Pair(-2, Pair(1, Pair(5, Pair(6, None)))))
        list5 = Pair(2, Pair(3, Pair(None, None)))
        list6 = Pair(0, Pair(2, Pair(3, Pair(None, None))))
        list7 = Pair(-199, Pair(-2, Pair(0, Pair(1, Pair(5, None)))))
        self.assertEqual(insert(list1, 3, song_less_than), list2)
        self.assertEqual(insert(list3, 6, song_less_than), list4)
        self.assertEqual(insert(list5, 0, song_less_than), list6)
        self.assertEqual(insert(list3, 0, song_less_than), list7)
        self.assertEqual(insert(None, 3, song_less_than), Pair(3, None))

    def test_sort(self):
        list1 = Pair(3, Pair(2, Pair(6, Pair(1, Pair(0, Pair(5, None))))))
        list2 = Pair(0, Pair(1, Pair(2, Pair(3, Pair(5, Pair(6, None))))))
        self.assertEqual(sort(list1, song_less_than), list2)

    def test_album_less_than_linked(self):
        album1 = "apple"
        album2 = "beta"
        self.assertTrue(album_less_than(album1, album2))
        self.assertFalse(album_less_than(album2, album1))

    def test_artist_less_than_linked(self):
        artist1 = "andrew"
        artist2 = "bob"
        self.assertTrue(artist_less_than(artist1, artist2))
        self.assertFalse(artist_less_than(artist2, artist1))

    def test_title_less_than_linked(self):
        title1 = "art"
        title2 = "bolts"
        self.assertTrue(title_less_than(title1, title2))
        self.assertFalse(title_less_than(title2, title1))

    def test_insert_sorted(self):
        list1 = Pair(1, Pair(2, Pair(4, Pair(5, None))))
        list2 = Pair(1, Pair(2, Pair(3, Pair(4, Pair(5, None)))))
        list3 = Pair(-199, Pair(-2, Pair(1, Pair(5, None))))
        list4 = Pair(-199, Pair(-2, Pair(1, Pair(5, Pair(6, None)))))
        list5 = Pair(2, Pair(3, Pair(None, None)))
        list6 = Pair(0, Pair(2, Pair(3, Pair(None, None))))
        list7 = Pair(-199, Pair(-2, Pair(0, Pair(1, Pair(5, None)))))
        self.assertEqual(insert_sorted(list1, 3, song_less_than), list2)
        self.assertEqual(insert_sorted(list3, 6, song_less_than), list4)
        self.assertEqual(insert_sorted(list5, 0, song_less_than), list6)
        self.assertEqual(insert_sorted(list3, 0, song_less_than), list7)
        self.assertEqual(insert_sorted(None, 3, song_less_than), Pair(3, None))

if __name__ == '__main__':
    unittest.main()
