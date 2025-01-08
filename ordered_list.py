class Node:
    '''Node for use with doubly-linked list'''
    def __init__(self, item):
        self.item = item
        self.next = None
        self.prev = None

class OrderedList:
    '''A doubly-linked ordered list of items, from lowest (head of list) to highest (tail of list)'''

    def __init__(self):
        '''Use ONE dummy node as described in class
           ***No other attributes***
           DO NOT have an attribute to keep track of size'''
        self.head = Node(None)
        self.head.next = self.head
        self.head.prev = self.head

    def is_empty(self):
        '''Returns True if OrderedList is empty
            MUST have O(1) performance'''
        return self.head.next == self.head

    def add(self, item):
        '''Adds an item to OrderedList, in the proper location based on ordering of items
           from lowest (at head end of list) to highest (at tail end of list) and returns True.
           If the item is already in the list, do not add it again and return False.
           MUST have O(n) average-case performance, O(1) best-case performance.  Assume that all 
           items added to your list can be compared using the < operator and can be compared for equality/inequality using ==.
           Make no other assumptions about the items in your list'''
        new = Node(item)
        x = self.head.next
        while x != self.head:
            if x.item == item:
                return False
            elif x.item > item:
                break
            x = x.next
        x.prev.next = new
        new.prev = x.prev
        x.prev = new
        new.next = x
        return True
        
    def remove_by_value(self, item):
        '''Removes the first occurrence of an item from OrderedList. If item is removed (was in the list) 
           returns True.  If item was not removed (was not in the list) returns False
           MUST have O(n) average-case performance, O(1) best-case performance'''
        x = self.head.next
        while x != self.head and x.item != item:
            x = x.next
        if x == self.head:
            return False
        x.prev.next = x.next
        x.next.prev = x.prev
        return True

    def index(self, item):
        '''Returns index of the first occurrence of an item in OrderedList (assuming head of list is index 0).
           If item is not in list, return None
           MUST have O(n) average-case performance, O(1) best-case performance'''
        if self.is_empty():
            return None
        if self.head.next.item == item:
            return 0
        x = self.head.next
        index = 0
        while x != self.head and x.item != item:
            x = x.next
            index += 1
        if x == self.head:
            return None
        return index

    def remove_by_index(self, index):
        '''Removes and returns item at index (assuming head of list is index 0).
           If index is negative or >= size of list, raises IndexError
           MUST have O(n) average-case performance, O(1) best-case performance'''
        if index < 0 or self.is_empty():
            raise IndexError
        x = self.head.next
        for i in range(index):
            x = x.next
            if x == self.head:
                raise IndexError
        x.next.prev = x.prev
        x.prev.next = x.next
        return x.item

    def search(self, item):
        '''Searches OrderedList for item, returns True if item is in list, False otherwise"
           To practice recursion, this method must call a RECURSIVE method that
           will search the list
           MUST have O(n) average-case performance, O(1) best-case performance'''
        if self.is_empty() or self.head.next.item > item or self.head.prev.item < item:
            return False
        if self.head.next.item == item or self.head.prev.item == item:
            return True
        return self.search_helper(item, self.head.next)
    
    def search_helper(self, item, node):
        if node.item == item:
            return True
        if node == self.head:
            return False
        return self.search_helper(item, node.next)

    def python_list(self):
        '''Return a Python list representation of OrderedList, from head to tail
           For example, list with integers 1, 2, and 3 would return [1, 2, 3]
           MUST have O(n) performance'''
        lst = []
        x = self.head.next
        while self.head != x:
            lst.append(x.item)
            x = x.next
        return lst

    def python_list_reversed(self):
        '''Return a Python list representation of OrderedList, from tail to head, using recursion
           For example, list with integers 1, 2, and 3 would return [3, 2, 1]
           To practice recursion, this method must call a RECURSIVE method that
           will return a reversed list
           MUST have O(n) performance'''
        return self.python_list_reversed_helper(self.head.prev)
    
    def python_list_reversed_helper(self, node):
        if node == self.head:
            return []
        lst = [node.item]
        lst += self.python_list_reversed_helper(node.prev)
        return lst

    def size(self):
        '''Returns number of items in the OrderedList
           To practice recursion, this method must call a RECURSIVE method that
           will count and return the number of items in the list
           MUST have O(n) performance'''
        return self.size_helper(self.head.next)

    def size_helper(self, node):
        if node == self.head:
            return 0
        return 1 + self.size_helper(node.next)
