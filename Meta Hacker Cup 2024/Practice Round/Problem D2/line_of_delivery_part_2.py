from random import random
import time

input_file = 'line_of_delivery_part_2_input.txt'

print("Reading input file")

with open(input_file, 'r') as f:
	num_tests = int(f.readline())
	cases = []
	for i in range(num_tests):
		num_stones, goal = [int(a) for a in f.readline().split(" ")]
		case = [goal, []]
		for j in range(num_stones):
			case[1].append(int(f.readline()))
		cases.append(case)

print("Evaluating cases")

class MyTreap():
	def __init__(self, energy_to_reach):
		self.energy_to_reach = energy_to_reach
		self.offset = 0
		self.left = None
		self.right = None
		self.priority = random()

	def decrement_energy(self):
		self.offset += 1

	def get_energy(self):
		self.push_offset()
		return self.energy_to_reach

	def push_offset(self):
		self.energy_to_reach -= self.offset
		if self.left:
			self.left.offset += self.offset
		if self.right:
			self.right.offset += self.offset
		self.offset = 0

	def split(self, energy_threshold):
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
		self.push_offset()
		if not self.right:
			return self
		else:
			return self.right.get_rightmost_node()

	def insert(self, stone_energy):
		L, R = self.split(stone_energy)
		
		new_stone = MyTreap(stone_energy + 1)

		result = L.merge(new_stone) if L else new_stone
		result = result.merge(R)
		result.decrement_energy()

		return result 

	def stone_energies_to_reach(self):
		pos = self.get_energy()
		L = self.left.stone_energies_to_reach() if self.left else []
		R = self.right.stone_energies_to_reach() if self.right else []
		return L + [pos] + R

start_time = time.time()

results = []

for goal, stones in cases:
	stone_treap = MyTreap(stones[0])
	for stone in stones[1:]:
		stone_treap = stone_treap.insert(stone)

	energies = stone_treap.stone_energies_to_reach()
	positions = [energy + i for i, energy in enumerate(energies)]
	positions = positions[::-1]

	best_distance = abs(positions[0] - goal)
	best_index = 0

	for i in range(1, len(positions)):
		distance = abs(positions[i] - goal)
		if distance < best_distance:
			best_distance = distance
			best_index = i

	results.append([best_index, best_distance])


print(f"Evaluation completed in {(time.time()-start_time):.2f} seconds")

print("Saving results")

with open('results.txt', 'w') as f:
	for i, result in enumerate(results):
		f.write(f'Case #{i+1}: {result[0]+1} {result[1]}\n') # Not zero-indexed!

print("Complete")