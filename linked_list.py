# A LinkedList contains
# - a Pair(value, LinkedList)
# - None

class Pair:
    def __init__(self, first, rest):
        self.first = first # any value
        self.rest = rest # a LinkedList

    def __eq__(self, other):
        return type(other) == Pair and self.first == other.first and self.rest == other.rest

    def __repr__(self):
        return "%r %r" % (self.first, self.rest)

# -> LinkedList
# this function takes no arguments and returns an empty list.
def empty_list():
    return None


# LinkedList int value -> LinkedList
# takes a list, an integer index, and another value as arguments and places the value at index position in the list
def add(anylist, index, value, counter=0):
    if anylist is None and index == 0:
        return Pair(value, None)
    if anylist is None or index < 0:
        raise IndexError
    if index == 0:
        return Pair(value, anylist)
    if counter == index-1:
        return Pair(anylist.first, Pair(value, anylist.rest))
    counter += 1
    return Pair(anylist.first, add(anylist.rest, index, value, counter))


# LinkedList -> int
# takes a list as an argument and returns the number of elements currently in the list
def length(anylist):
    if anylist is None:
        return 0
    if anylist.rest is None:
        return 1
    return length(anylist.rest) + 1

# AnyList -> int
# takes a list and an integer index as arguments and returns the value at the index position in the list
def get(anylist, index, counter=0):
    if anylist is None or index < 0:
        raise IndexError
    if index == counter:
        return anylist.first
    counter += 1
    return get(anylist.rest, index, counter)

# LinkedList int value -> LinkedList
# takes a list, an integer index, and another value (of any type) as arguments and replaces the element at index position in the list with the given value
def set(anylist, index, value, counter=0):
    if anylist is None or index < 0:
        raise IndexError
    if index == counter:
        return Pair(value, anylist.rest)
    counter += 1
    return Pair(anylist.first, set(anylist.rest, index, value, counter))


# LinkedList int -> tuple
# takes a list and an integer index as arguments and removes the element and returns the list
def remove_list(anylist, index, counter=0):
    if anylist is None or index < 0:
        raise IndexError
    if index == counter:
        return anylist.rest
    counter += 1
    return Pair(anylist.first, remove_list(anylist.rest, index, counter))


# LinkedList int -> value
# takes a list and an integer index and removes the element at the index position and returns the element removed
def remove_ele(anylist, index, counter=0):
    if anylist is None or index < 0:
        raise IndexError
    if index == counter:
        return anylist.first
    counter += 1
    return remove_ele(anylist.rest, index, counter)


# LinkedList int -> Tuple
# combines the remove_list and remove_ele functions to return a tuple
def remove(anylist, index):
    return remove_ele(anylist, index), remove_list(anylist, index)


# LinkedList function -> None
# takes a linked list and a function as arguments and applies the provided function to the value at each position in the List
def foreach(linkedList, function):
    if linkedList is None:
        return None
    function(linkedList.first)
    return foreach(linkedList.rest, function)


# int ->
# adds one to the given int parameter
def add_one(element):
    element += 1


# NumList value -> NumList
# Returns a new list containing the new value in the proper location
def insert(numlist, insertnum, func, boolean=True):
    if numlist == None:
        return Pair(insertnum, None)
    if numlist.rest == None:
        if func(numlist.first, insertnum):
            return Pair(numlist.first, Pair(insertnum, None))
    if func(numlist.first, insertnum) and func(insertnum, numlist.rest.first):
        return Pair(numlist.first, Pair(insertnum, numlist.rest))
    if func(insertnum, numlist.first) and boolean:
        boolean=False
        return Pair(insertnum, Pair(numlist.first, numlist.rest))
    return Pair(numlist.first, insert(numlist.rest, insertnum, func, boolean))


# LinkedList function -> LinkedList
# takes a linked list and a "less-than" function as arguments and sorts the List such that the elements are in ascending order as determined by the "less-than" function
def sort(linkedList, lessthan, emptylst=None, counter=0):
    if linkedList is None:
        return emptylst
    emptylst = insert(emptylst, linkedList.first, lessthan)
    counter += 1
    return sort(linkedList.rest, lessthan, emptylst, counter)
        #creating a new list and add items and then return the list, won't change the original list


# song song -> boolean
# returns whether or not the first song parameter is greater than the second song parameter in terms of song number
def song_less_than(song1, song2):
    if song1 <= song2:
        return True
    return False


# song song -> boolean
# returns whether or not the first song parameter is greater than the second song parameter in terms of song album
def album_less_than(album1, album2):
    if album1 <= album2:
        return True
    return False


# song song -> boolean
# returns whether or not the first song parameter is greater than the second song parameter in terms of song artist
def artist_less_than(artist1, artist2):
    if artist1 <= artist2:
        return True
    return False


# song song -> boolean
# returns whether or not the first song parameter is greater than the second song parameter in terms of song title
def title_less_than(title1, title2):
    if title1 <= title2:
        return True
    return False

# ------------------------------------------------------------------------------------------------------------------

# LinkedList value func -> LinkedList
# inserts a value into a sorted list in ascending order based off of the comes before function returns the list including the inserted value.
def insert_sorted(LinkedList, value, func):
    LinkedList = insert(LinkedList, value, func)
    return LinkedList