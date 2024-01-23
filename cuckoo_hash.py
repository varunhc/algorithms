# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import random as rand
from typing import List

class CuckooHash:
	def __init__(self, init_size: int):
		self.__num_rehashes = 0
		self.CYCLE_THRESHOLD = 10

		self.table_size = init_size
		self.tables = [[None]*init_size for _ in range(2)]

	def hash_func(self, key: int, table_id: int) -> int:
		key = int(str(key) + str(self.__num_rehashes) + str(table_id))
		rand.seed(key)
		return rand.randint(0, self.table_size-1)

	def get_table_contents(self) -> List[List[int]]:
		return self.tables

	# you should *NOT* change any of the existing code above this line
	# you may however define additional instance variables inside the __init__ method.

	def insert(self, key: int) -> bool:
		shuffle_count = -1
		table_id = 0
		while True:
			shuffle_count += 1
			if shuffle_count>self.CYCLE_THRESHOLD:
				return False
			else:
				index = self.hash_func(key, table_id)
				if self.tables[table_id][index]!=None:
					temp = self.tables[table_id][index]
					self.tables[table_id][index] = key
					key = temp
					table_id = (table_id+1) % 2
				else:
					self.tables[table_id][index] = key
					return True

	def lookup(self, key: int) -> bool:
		val0 = self.tables[0][self.hash_func(key, 0)]
		if key == val0:
			return True
		val1 = self.tables[1][self.hash_func(key, 1)]
		if key == val1:
			return True
		return False

	def delete(self, key: int) -> None:
		table_zero_index = self.hash_func(key, 0)
		if key == self.tables[0][table_zero_index]:
			self.tables[0][table_zero_index] = None
			return
		table_one_index = self.hash_func(key, 1)
		if key == self.tables[1][table_one_index]:
			self.tables[1][table_one_index] = None
			return

	def rehash(self, new_table_size: int) -> None:
		self.__num_rehashes += 1; self.table_size = new_table_size # do not modify this line
		temp_tables = self.tables.copy()
		self.tables = [[None]*new_table_size for _ in range(2)]
		for i in temp_tables:
			for j in i:
				if j!=None:
					self.insert(j)
