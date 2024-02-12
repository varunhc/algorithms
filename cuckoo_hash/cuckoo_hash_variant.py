# based on https://www.cs.princeton.edu/~mfreed/docs/cuckoo-eurosys14.pdf
# main difference from cuckoo 24: two hash functions operating on the same table;
# always insert at hash0 in case h0 and h1 are full; so basically h1 is never used for popping

import random as rand
from typing import List, Optional
from copy import deepcopy


class CuckooHash24:
    def __init__(self, init_size: int):
        self.__num_rehashes = 0
        self.bucket_size = 4
        self.CYCLE_THRESHOLD = 10

        self.table_size = init_size
        self.table = [None] * init_size

    def get_rand_idx_from_bucket(self, bucket_idx: int, table_id: int) -> int:
        # you must use this function when you need to displace a random key from a bucket during insertion (see the description in requirements.py).
        # this function randomly chooses an index from a given bucket for a given table. this ensures that the random
        # index chosen by your code and our test script match.
        #
        # for example, if you are inserting some key x into table 0, and hash_func(x, 0) returns 5, and the bucket in index 5 of table 0 already has 4 elements,
        # you will call get_rand_bucket_index(5, 0) to determine which key from that bucket to displace, i.e. if get_random_bucket_index(5, 0) returns 2, you
        # will displace the key at index 2 in that bucket.
        rand.seed(int(str(bucket_idx) + str(table_id)))
        return rand.randint(0, self.bucket_size - 1)

    def hash_func(self, key: int, table_id: int) -> int:
        key = int(str(key) + str(self.__num_rehashes) + str(table_id))
        rand.seed(key)
        return rand.randint(0, self.table_size - 1)

    def get_table_contents(self) -> List[List[Optional[List[int]]]]:
        # the buckets should be implemented as lists. Table cells with no elements should still have None entries.
        return self.table

    # you should *NOT* change any of the existing code above this line
    # you may however define additional instance variables inside the __init__ method.

    def insert(self, key: int) -> bool:
        shuffle_count = -1
        while True:
            shuffle_count += 1
            if shuffle_count > self.CYCLE_THRESHOLD:
                return False
            else:
                # try hash 0 insertion
                index_x = self.hash_func(key, 0)
                if self.table[index_x] == None:
                    self.table[index_x] = [key]
                    return True
                elif len(self.table[index_x]) < self.bucket_size:
                    self.table[index_x].append(key)
                    return True
                # try hash 1 insertion
                index_y = self.hash_func(key, 1)
                if self.table[index_y] == None:
                    self.table[index_y] = [key]
                    return True
                elif len(self.table[index_y]) < self.bucket_size:
                    self.table[index_y].append(key)
                    return True
                pop_index = self.get_rand_idx_from_bucket(index_x, 0)
                popped = self.table[index_x][pop_index]
                self.table[index_x][pop_index] = key
                key = popped

    def lookup(self, key: int) -> bool:
        val0 = self.table[self.hash_func(key, 0)]
        if val0 != None and key in val0:
            return True
        val1 = self.table[self.hash_func(key, 1)]
        if val1 != None and key in val1:
            return True
        return False

    def delete(self, key: int) -> None:
        table_zero_index = self.hash_func(key, 0)
        if key in self.table[table_zero_index]:
            key_index = self.table[table_zero_index].index(key)
            self.table[table_zero_index].pop(key_index)
            if not self.table[table_zero_index]:
                self.table[table_zero_index] = None
            return
        table_one_index = self.hash_func(key, 1)
        if key in self.table[table_one_index]:
            key_index = self.table[table_one_index].index(key)
            self.table[table_one_index].pop(key_index)
            if not self.table[table_one_index]:
                self.table[table_one_index] = None
            return

    def rehash(self, new_table_size: int) -> None:
        self.__num_rehashes += 1;
        self.table_size = new_table_size  # do not modify this line
        temp_tables = deepcopy(self.table)
        self.table = [None] * new_table_size
        for i in temp_tables:
            if i!=None:
                for j in i:
                    self.insert(j)
