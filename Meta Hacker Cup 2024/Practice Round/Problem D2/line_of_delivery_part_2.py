from random import random
import time

print("Reading input file")

input_file = 'line_of_delivery_part_2_input.txt'
cases = []

with open(input_file, 'r') as f:
	num_tests = int(f.readline())
	for _ in range(num_tests):
		num_stones, goal = [int(a) for a in f.readline().split(" ")]
		stones = []
		for _ in range(num_stones):
			stones.append(int(f.readline()))
		cases.append([goal, stones])


print("Evaluating cases")

class MyTreap():
	"""
	Custom treap implementation that allows efficient decrementing of all
	elements simultaneously.

	Rather than storing the *positions* of all stones, we store the energy
	needed to hit each stone, from which we can later recover the positions.
	"""
	
	def __init__(self, energy_to_reach):
		"""
		Initialize a treap containing a single stone which requires
		energy_to_reach units of energy to collide with.
		"""

		self.energy_to_reach = energy_to_reach # Value stored in node
		self.offset = 0 # Amount node's value should be shifted left
		self.left = None # Left child of node
		self.right = None # Right child of node
		self.priority = random() # Randomize priority to optimize treap depth

	def decrement_energy(self):
		"""
		Decrement all values in the treap.
		"""

		self.offset += 1

	def get_energy(self):
		""" 
		Get the value from this node.
		"""

		self.push_offset() # Account for offset shifts
		return self.energy_to_reach

	def push_offset(self):
		"""
		Update the value in the node and its children according to the amount
		of accumulated offset.
		"""

		self.energy_to_reach -= self.offset
		if self.left:
			self.left.offset += self.offset
		if self.right:
			self.right.offset += self.offset
		self.offset = 0

	def split(self, energy_threshold):
		"""
		Split the treap into (possibly null) treaps L and R where L contains
		all values up to energy_threshold, and R contains all values that 
		exceed energy_threshold.
		"""

		if self.get_energy() <= energy_threshold:
			if self.right:
				L, R = self.right.split(energy_threshold)
				self.right = L
				return self, R
			else:
				return self, None
		else:
			if self.left:
				L, R = self.left.split(energy_threshold)
				self.left = R
				return L, self
			else:
				return None, self

	def merge(self, T):
		""" 
		Merge self with another treap T. Assumes that all values in T are at
		least as large as those in self.
		"""

		self.push_offset()
		if T == None:
			return self
		if not self.right:
			self.right = T 
			return self
		if self.priority > T.priority:
			merged = self.right.merge(T)
			self.right = merged 
			return self
		else:
			merged = self.merge(T.left)
			T.left = merged
			return T

	def get_rightmost_node(self):
		"""
		Get the rightmost, i.e. largest, value in the treap.
		"""

		self.push_offset()
		if not self.right:
			return self
		else:
			return self.right.get_rightmost_node()

	def insert(self, stone_energy):
		"""
		Insert a new value into the treap, and decrement all values that were
		already present.
		"""

		L, R = self.split(stone_energy)
		new_stone = MyTreap(stone_energy + 1)
		result = L.merge(new_stone) if L else new_stone
		result = result.merge(R)
		result.decrement_energy()
		return result 

	def stone_energies_to_reach(self):
		"""
		Get a sorted list of all values in the treap.
		"""

		pos = self.get_energy()
		L = self.left.stone_energies_to_reach() if self.left else []
		R = self.right.stone_energies_to_reach() if self.right else []
		return L + [pos] + R


start_time = time.time()
results = []

for goal, stones in cases:
	# First, insert all stones into a treap.
	stone_treap = MyTreap(stones[0])
	for stone in stones[1:]:
		stone_treap = stone_treap.insert(stone)

	# Get the list of energies to reach each stone in the final configuration.
	energies = stone_treap.stone_energies_to_reach()

	# To obtain the positions of each stone, note that the energy required
	# to reach it is the difference of its position and the number of stones
	# that precede it. 
	positions = [energy + i for i, energy in enumerate(energies)]

	# Reverse the positions list. Now, the i-th element is where the i-th
	# thrown stone lands.
	positions = positions[::-1]

	# From here, we proceed as in Problem D1. We find the best possible
	# distance to the goal, and loop through the stones until we find the
	# first one that lands at that distance.
	distances_to_goal = [abs(position - goal) for position in positions]
	min_distance = min(distances_to_goal)

	for i in range(len(stones)):
		if abs(positions[i] - goal) == min_distance:
			results.append([i, min_distance])
			break

print(f"Evaluation completed in {(time.time()-start_time):.2f} seconds")


print("Saving results")

with open("results.txt", "w") as f:
	for i, result in enumerate(results):
		f.write(f"Case #{i+1}: {result[0]+1} {result[1]}\n") # Not zero-indexed!

print("Complete")