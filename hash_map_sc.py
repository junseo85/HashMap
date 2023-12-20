# Name: Jun Seo
# OSU Email: seoj2@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6 portfolio
# Due Date:12/08/2023
# Description: collision resolution with chaining in Hashmap


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        add item into Hashmap with given key and value. check and make sure table load is below 1.0
        otherwise call resize and double the size. amortized O(1)
        """

        if self.table_load() >= 1.0:
        # if current load factor of the table is greater or equal to 1.0 then must resize to double its current capacity
            new_capacity = self._capacity * 2
            self.resize_table(new_capacity)
        index = self._hash_function(key) % self._capacity
        index_num = 0

        if self.get(key) is None:
            self._buckets[index].insert(key,value)
            self._size += 1
            return
        if self.get(key) is not None:
            while index_num < self._capacity: #loop through linked list and search for matching key
                for a in self._buckets[index_num]:
                    if a.key == key:# if matching key is found, then replace the value
                        a.value = value
                        return
                    if a.next != None and a.key != key: #iterate through linked list
                        a = a.next
                index_num += 1
            self._buckets[index].insert(key,value)
            self._size +=1

    def resize_table(self, new_capacity: int) -> None:
        """
        rehash all the items using another HashMap. amortized O(1)
        """

        if new_capacity <1:
            return None



        new_hash = HashMap(new_capacity, self._hash_function) # create new HashMap
        

        index_count = 0
        while index_count <self._capacity:
            for a in self._buckets[index_count]:
                if a.key != None:
                    index = self._hash_function(a.key) % new_capacity

                    new_hash.put(a.key,a.value)
                    # new_hash._buckets.set_at_index(index,a)
                    # new_hash._size+= 1
                    if a.next != None:
                        a = a.next
            index_count += 1

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
        returns empty bucket. O(n)
        """
        count = 0
        for i in range(self._capacity):
            if self._buckets[i]._head == None:
            # if self.get(self._buckets[i]) is None:
                count += 1
        return int(count)
        # return self._capacity-self._size
    def get(self, key: str):
        """
        returns the value with given key. amortized O(1)
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        for i in self._buckets[index]:
            if i.key == key:#find matching key
                return i.value #return the value

    def contains_key(self, key: str) -> bool:
        """
        if given key is in hash map, return True, otherwise return False. amortized O(1)
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        for i in self._buckets[index]:
            if i.key == key:  # find matching key
                return True
        return False

    def remove(self, key: str) -> None:
        """
        removes the given key and value from the hash map. amortized O(1)
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        for i in self._buckets[index]:
            if i.key == key:  # find matching key
                self._buckets[index].remove(key)
                self._size -=1
    def get_keys_and_values(self) -> DynamicArray:
        """
        find key and value from hash map and put in new Dynamic array as tuple(key,value) then return the dynamic array. amortized O(1)
        """

        count = 0
        new_array = DynamicArray()
        index_count = 0
        while index_count < self._capacity:
            for a in self._buckets[index_count]:
                if a.key != None:
                    new_array.append((a.key, a.value))
                    count += 1
                    if a.next != None:
                        a = a.next
            index_count += 1
        return new_array

    def clear(self) -> None:
        """
        erase all the items in the hash but keep the original capacity. O(1)
        """
        temp_capacity = self._capacity
        new_hash = HashMap(self._capacity,self._hash_function)
        self._buckets = new_hash._buckets
        self._size = 0
        self._capacity = temp_capacity


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    find the highest frequency for the mode value and return list of item that matches with highest frequency and with frequency. O(n)
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()
    # put items in hashmap with frequency
    no_duplicate = DynamicArray() # array with no duplicate
    for i in range( da.length()):
        if map.contains_key(da[i]) == False:
            map.put(da[i],1)
            no_duplicate.append(da[i])
        elif map.contains_key(da[i]) == True:
            value = map.get(da[i])
            value += 1
            map.put(da[i],value)
    new_da = DynamicArray()
    max = 0
    index = 0
    #search for max number
    while index < da.length():
        for a in range(da.length()):
            if map.get(da[index]) != None and map.get(da[index])> max:
                max = map.get(da[index])
            index += 1
    # find all the items that matches same max number(frequency) then put in new_da dynamic array

    for k in range(no_duplicate.length()):
        if map.get(no_duplicate[k]) == max:
            new_da.append(no_duplicate[k])
    return new_da, max


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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
