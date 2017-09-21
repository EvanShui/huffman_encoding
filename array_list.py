
# - an array to hold the elements
# - a length representing the number of non None elements in the array
# - a capacity representing how many total elements
# a List is a List that mimics that of the python list with the fields length and capacity
class List:
    def __init__(self):
        self.capacity = 10 # a capacity
        self.length = 0 # a length
        self.array = [None] * 10 # an array

    def __eq__(self, other):
        return type(other) == List and self.capacity == other.capacity and self.length == other.length and self.array == other.array

    def __repr__(self):
        return "%r %r %r" % (self.capacity, self.length, self.array)


# None -> AnyList
# This function takes no argument and returns an empty list
def empty_list():
    return List()

# list int value -> list
# takes a list, an integer index, and another value as arguments and places the value at the index position in the list
def add(arraylist, index, value):
    if index > arraylist.length or index < 0:
        raise IndexError
    array = [None] * (arraylist.capacity + 1)
    for i in range(arraylist.length):
        if i >= index:
            array[i + 1] = arraylist.array[i]
        else:
            array[i] = arraylist.array[i]
    array[index] = value
    arraylist.array = array
    arraylist.length += 1
    arraylist.capacity += 1
    return arraylist


# list -> int
# returns the length of the array list
def length(arraylist):
    return arraylist.length


# list int -> int
# returns the element within the array at the specified index
def get(arraylist, index):
    if index >= arraylist.length or index < 0:
        raise IndexError
    return arraylist.array[index]


# list int value -> list
# sets the elemenet at the specified index to the value and returns the array class as a whole
def set(arraylist, index, value):
    if index >= arraylist.length or index < 0:
        raise IndexError
    arraylist.array[index] = value
    return arraylist


# list int -> tuple
# removes the specified element from the array list and returns a tuple of the element that was removed and the resulting list
def remove(arraylist, index):
    if index >= arraylist.length or index < 0:
        raise IndexError
    array = [None] * (arraylist.capacity - 1)
    value = arraylist.array[index]
    for i in range(arraylist.length):
        if i >= index:
            array[i] = arraylist.array[i+1]
        else:
            array[i] = arraylist.array[i]
    arraylist.array = array
    arraylist.length -= 1
    arraylist.capacity -= 1
    return value, arraylist