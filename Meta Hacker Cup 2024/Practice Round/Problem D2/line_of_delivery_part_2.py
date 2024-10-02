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
	def __init__(self, position):
		self.position = position
		self.offset = 0
		self.left = None
		self.right = None
		self.priority = random()
		self.num_children = 0

	def get_position(self):
		if offset != 0:
			self.position -= offset
		if self.left:
			self.left.offset = offset
		if self.right:
			self.right.offset = offset
		self.offset = 0
		return self.position

	def count_children(self):
		self.num_children = 0
		if self.left != None:
			self.num_children += 1 + self.left.num_children
		if self.right != None:
			self.num_children += 1 + self.right.num_children

	def children_to_left(self):
		num = self.num_children
		if self.right != None:
			num -= 1 + self.right.num_children
		return num

def split(T, x):
	if T == None:
		return None, None
	else:
		if T.get_position() <= x:
			L, R = split(T.right, x)
			T.right = L
			T.count_children()
			return T, R
		else:
			L, R = split(T.left, x)
			T.left = R
			T.count_children()
			return L, T

def merge(T1, T2):
	if T1 == None:
		return T2
	if T2 == None:
		return T1
	if T1.priority > T2.priority:
		merged_right = merge(T1.right, T2)
		T1.right = merged_right
		T1.count_children()
		return T1
	else:
		merged_left = merge(T1, T2.left)
		T2.left = merged_left
		T2.count_children()
		return T2

def insert_stone(T, x):
	# Find where our stone lands
	N = T
	while True:
		if N == None:
			break
		if N.position <= x + N.num_to_left():
			if N.right == None:
				break
			N = N.right
		else:
			if N.left == None:
				break
			N = N.left
	stone_lands_at = x
	if N != None:
		stone_lands_at += 


for goal, stones in cases:
	# The set of energies is the same as the set of positions where stones land
	# So, start by computing the shortest distance from some stone to the goal.
	distances_to_goal = [abs(stone-goal) for stone in stones]
	min_distance = min(distances_to_goal)

	# Now we need to find the least-indexed stone that lands at this distance.
	# We can just iterate through the stones, noting that the i-th stone will
	# land in the place i-th from last in the sorted list of resting positions.
	resting_places = sorted(stones, reverse = True)
	for i in range(len(resting_places)):
		if abs(resting_places[i]-goal) == min_distance:
			results.append([i, min_distance])
			break

print("Saving results")

with open('results.txt', 'w') as f:
	for i, result in enumerate(results):
		f.write(f'Case #{i+1}: {result[0]+1} {result[1]}\n') # Not zero-indexed!

print("Complete")