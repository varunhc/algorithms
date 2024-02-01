# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import random as rand
from typing import List, Optional
from copy import deepcopy


class CuckooHash24:
    def __init__(self, init_size: int):
        self.__num_rehashes = 0
        self.bucket_size = 4
        self.CYCLE_THRESHOLD = 10

        self.table_size = init_size
        self.tables = [[None] * init_size for _ in range(2)]

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
        return self.tables

    # you should *NOT* change any of the existing code above this line
    # you may however define additional instance variables inside the __init__ method.

    def insert(self, key: int) -> bool:
        shuffle_count = -1
        table_id = 0
        while True:
            shuffle_count += 1
            if shuffle_count > self.CYCLE_THRESHOLD:
                return False
            else:
                index_x = self.hash_func(key, table_id)
                if self.tables[table_id][index_x] == None:
                    self.tables[table_id][index_x] = [key]
                    return True
                elif len(self.tables[table_id][index_x]) < self.bucket_size:
                    self.tables[table_id][index_x].append(key)
                    return True
                pop_index = self.get_rand_idx_from_bucket(index_x, table_id)
                popped = self.tables[table_id][index_x].pop(pop_index)
                self.tables[table_id][index_x].append(key)
                key = popped
                table_id = table_id ^ 1

    def lookup(self, key: int) -> bool:
        val0 = self.tables[0][self.hash_func(key, 0)]
        if val0 != None and key in val0:
            return True
        val1 = self.tables[1][self.hash_func(key, 1)]
        if val1 != None and key in val1:
            return True
        return False

    def delete(self, key: int) -> None:
        table_zero_index = self.hash_func(key, 0)
        if key in self.tables[0][table_zero_index]:
            key_index = self.tables[0][table_zero_index].index(key)
            self.tables[0][table_zero_index].pop(key_index)
            if not self.tables[0][table_zero_index]:
                self.tables[0][table_zero_index] = None
            return
        table_one_index = self.hash_func(key, 1)
        if key in self.tables[1][table_one_index]:
            key_index = self.tables[1][table_one_index].index(key)
            self.tables[1][table_one_index].pop(key_index)
            if not self.tables[1][table_one_index]:
                self.tables[1][table_one_index] = None
            return

    def rehash(self, new_table_size: int) -> None:
        self.__num_rehashes += 1;
        self.table_size = new_table_size  # do not modify this line
        temp_tables = deepcopy(self.tables)
        self.tables = [[None] * new_table_size for _ in range(2)]
        for i in temp_tables:
            for j in i:
                if j != None:
                    for k in j:
                        self.insert(k)

    def insert01(self, key: int) -> bool:
        shuffle_count = -1
        table_id = 0
        # orgKey = key
        while True:
            shuffle_count += 1
            if shuffle_count > self.CYCLE_THRESHOLD:
                return False
            else:
                table_x = table_id
                table_y = (table_id + 1) % 2
                index_x = self.hash_func(key, table_x)
                index_y = self.hash_func(key, table_y)

                if not self.tables[table_x][index_x] or len(self.tables[table_x][index_x]) < self.bucket_size:
                    if self.tables[table_x][index_x] == None:
                        self.tables[table_x][index_x] = [key]
                    else:
                        self.tables[table_x][index_x].append(key)
                    return True
                if not self.tables[table_y][index_y] or len(self.tables[table_y][index_y]) < self.bucket_size:
                    if self.tables[table_y][index_y] == None:
                        self.tables[table_y][index_y] = [key]
                    else:
                        self.tables[table_y][index_y].append(key)
                    return True
                pop_index = self.get_rand_idx_from_bucket(index_x, table_x)
                temp = self.tables[table_x][index_x][pop_index]
                self.tables[table_x][index_x][pop_index] = key
                key = temp
                table_id = table_x ^ 1
