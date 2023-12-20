# Name: Jun Seo
# OSU Email: seoj2@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6 portfolio
# Due Date:12/08/2023
# Description: collision resolution with open addressing in Hashmap

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        add item into Hashmap with given key and value. check and make sure table load is below 0.5
        otherwise call resize and double the size. amortized O(1)
        """
        if self.table_load() >= 0.5:
        # if current load factor of the table is greater or equal to 1.0 then must resize to double its current capacity
            new_capacity = self._capacity * 2
            self.resize_table(new_capacity)
        index = self._hash_function(key) % self._capacity
        node = HashEntry(key,value)
        if self._buckets[index] == None:
            self._buckets.set_at_index(index, node)
            self._size += 1
            return
        quadratic = 0
        if self._buckets[index] != None:
            if self._buckets[index].key == key:# if key is matched, then replace the value
                if self._buckets[index].is_tombstone == True: # if item was previously removed, then revive the item by setting tombstone as false

                    self._buckets[index].is_tombstone = False
                    self._size += 1
                    return
                self._buckets.set_at_index(index, node)
                return
            temp_index = index
            while self._buckets[temp_index] != None: #Quadratic probing
                quadratic += 1
                if self._buckets[temp_index].key == key:
                    if self._buckets[temp_index].is_tombstone == True:
                        self._buckets[temp_index].is_tombstone = False
                        self._size += 1
                        return
                    self._buckets.set_at_index(temp_index,node)
                    return
                temp_index = index + quadratic * quadratic
                if temp_index >= self._buckets.length()-1:
                    temp_index = (index + quadratic * quadratic) % self._capacity

            self._buckets.set_at_index(temp_index,node)
            self._size +=1

    def resize_table(self, new_capacity: int) -> None:
        """
        rehash all the items using another HashMap. amortized O(1)
        """

        if new_capacity < self._size:
            return
        if self._capacity == 1:
            return None

        if self._is_prime(new_capacity) is False and new_capacity >1: # if new capacity is not prime number
            new_capacity = self._next_prime(new_capacity) #find next prime number and set as new capacity
        if new_capacity == 1:
            new_capacity = self._capacity

        new_hash = HashMap(new_capacity, self._hash_function) # create new HashMap
        for i in range(self._capacity):
            if self._buckets[i] != None:
                new_hash.put(self._buckets[i].key,self._buckets[i].value) # rehash all the items by calling put function into new_hash
        self._capacity = new_hash._capacity
        self._size = new_hash._size
        self._buckets = new_hash._buckets# set new Hashmap as current Hashmap


    def table_load(self) -> float:
        """
        returns current hash table load factor. O(1)
        """
        load_factor = self._size / self._capacity
        return float(load_factor)

    def empty_buckets(self) -> int:
        """
        returns the number of empty buckets. O(1)
        """
        empty = self._capacity - self._size
        return empty

    def get(self, key: str) -> object:
        """
        search for item with given key and return the value. amortized O(1)
        """

        index = self._hash_function(key) % self._capacity
        if self._buckets.get_at_index(index) != None:
            if self._buckets.get_at_index(index).key == key:
                if self._buckets.get_at_index(index).is_tombstone == True: # if item was previously removed then return None
                    return None
                else:
                    return self._buckets.get_at_index(index).value #return the value
            else:
                quadratic = 0
                temp_index = index + quadratic * quadratic
                while self._buckets[temp_index] != None:
                    quadratic += 1

                    if self._buckets[temp_index].key == key:
                        if self._buckets.get_at_index(temp_index).is_tombstone == True:
                            return None
                        else:
                            return self._buckets.get_at_index(temp_index).value

                    temp_index = index + quadratic * quadratic

                    if temp_index >= self._buckets.length() - 1:
                        temp_index = (index + quadratic * quadratic) % self._capacity

        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        search for item with given Key. if item was removed in the past, return False. amortized O(1)
        """
        index = self._hash_function(key) % self._capacity
        if self._buckets.get_at_index(index) != None:
            if self._buckets.get_at_index(index).key == key:
                if self._buckets.get_at_index(index).is_tombstone == True:
                    return False
                else:
                    return True
            else:
                quadratic = 0
                temp_index = index + quadratic * quadratic
                while self._buckets[temp_index] != None:
                    quadratic += 1

                    if self._buckets[temp_index].key == key:
                        if self._buckets.get_at_index(temp_index).is_tombstone == True: # if item was already erased in the past, then return False
                            return False
                        else:
                            return True

                    temp_index = index + quadratic * quadratic

                    if temp_index >= self._buckets.length() - 1:
                        temp_index = (index + quadratic * quadratic) % (self._capacity)
                return False
        else:
            return False

    def remove(self, key: str) -> None:
        """
        removed item with given key- removed item should be replaced as tombstone= mark is_tombstone as True. amortized O(1)
        """

        index = self._hash_function(key) % self._capacity
        if self._buckets.get_at_index(index) != None:
            if self._buckets.get_at_index(index).key != key:
                quadratic = 0
                temp_index = index + quadratic * quadratic
                while self._buckets[temp_index] != None:
                    quadratic += 1

                    if self._buckets[temp_index].key == key:
                        if self._buckets[temp_index].is_tombstone == True: # if item was already erased in the past, then just return
                            return None
                        self._buckets.get_at_index(temp_index).is_tombstone = True # remove item by marking tombstone as true
                        self._size -= 1 # decrease the size
                        return
                    temp_index = index + quadratic * quadratic

                    if temp_index >= self._buckets.length() - 1:
                        temp_index = (index + quadratic * quadratic) % (self._capacity)
            if self._buckets.get_at_index(index).key == key:
                if self._buckets[index].is_tombstone == True:
                    return None
                else:
                    self._buckets.get_at_index(index).is_tombstone = True
                    self._size -= 1
        else:
            return

    def get_keys_and_values(self) -> DynamicArray:
        """
        returns the dynamicarray with key/value paired as tuple. amortized O(1)
        """
        count = 0
        new_array = DynamicArray()

        index_count = 0
        while index_count < self._capacity:
            if self._buckets[index_count] != None:
                if self._buckets[index_count].is_tombstone == False: # check and make sure if item was previously erased(marked as tombstone), only add if its not previouisly erased

                    new_array.append((self._buckets[index_count].key,self._buckets[index_count].value))

            index_count += 1

        return new_array

    def clear(self) -> None:
        """
        clear the items. O(1)
        """
        temp_capacity = self._capacity
        new_hash = HashMap(self._capacity,self._hash_function)
        self._buckets = new_hash._buckets
        self._size = 0

    def __iter__(self):
        """
        initialize a variable to track the iterator's progress
        """

        self._index = 0
        return self

    def __next__(self):
        """
        build a iterator functionality.
        """
        try:
            while self._buckets[self._index] == None: # iterate through until the index that has items
                self._index = self._index +1
            value = self._buckets[self._index]
        except DynamicArrayException:
            raise StopIteration
        self._index = self._index + 1
        return value


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    # print("\nPDF - __iter__(), __next__() example 1")
    # print("---------------------")
    # m = HashMap(10, hash_function_1)
    # for i in range(5):
    #     m.put(str(i), str(i * 10))
    # print(m)
    # for item in m:
    #     print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
