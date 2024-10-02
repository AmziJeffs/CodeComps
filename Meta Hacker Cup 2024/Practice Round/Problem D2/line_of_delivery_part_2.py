from random import random

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
	def __init__(self, position, energy_to_reach):
		self.position = position
		self.energy_to_reach = energy_to_reach
		self.position_offset = 0
		self.energy_offset = 0
		self.left = None
		self.right = None
		self.priority = random()

	def shift_left(self):
		self.position_offset += 1

	def decrement_energy(self):
		self.energy_offset += 1

	def get_position(self):
		self.push_offsets()
		return self.position

	def get_energy(self):
		self.push_offsets()
		return self.energy_to_reach

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
		self.push_offsets()
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

	def push_offsets(self):
		self.energy_to_reach -= self.energy_offset
		self.position -= self.position_offset
		if self.left:
			self.left.energy_offset += self.energy_offset
			self.left.position_offset += self.position_offset
		if self.right:
			self.right.energy_offset += self.energy_offset
			self.right.position_offset += self.position_offset
		self.energy_offset = 0
		self.position_offset = 0

	def get_rightmost_node(self):
		self.push_offsets()
		if not self.right:
			return self
		else:
			return self.right.get_rightmost_node()

	def insert(self, stone_energy):
		L, R = self.split(stone_energy)

		stone_x = stone_energy
		if L:
			closest_stone_to_left = L.get_rightmost_node()
			energy_left_over = stone_energy - closest_stone_to_left.get_energy() + 1
			stone_x = closest_stone_to_left.get_position() + energy_left_over
			L.shift_left()
		
		stone = MyTreap(stone_x, stone_energy + 1)

		result = L.merge(stone) if L else stone
		result = result.merge(R)
		result.decrement_energy()

		return result 

	def stone_positions(self):
		pos = self.get_position()
		L = self.left.stone_positions() if self.left else []
		R = self.right.stone_positions() if self.right else []
		return L + [pos] + R

results = []

for i, [goal, stones] in enumerate(cases):
	stone_treap = MyTreap(stones[0], stones[0])
	for stone in stones[1:]:
		stone_treap = stone_treap.insert(stone)

	positions = stone_treap.stone_positions()[::-1]

	best_distance = abs(positions[0] - goal)
	best_index = 0

	for j in range(1, len(positions)):
		distance = abs(positions[j] - goal)
		if distance < best_distance:
			best_distance = distance
			best_index = j

	results.append([best_index, best_distance])



print("Saving results")

with open('results.txt', 'w') as f:
	for i, result in enumerate(results):
		f.write(f'Case #{i+1}: {result[0]+1} {result[1]}\n') # Not zero-indexed!

print("Complete")