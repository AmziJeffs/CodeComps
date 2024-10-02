input_file = 'line_of_delivery_part_1_input.txt'

print("Reading input file")

with open(input_file, 'r') as f:
	raw = f.read().split('\n')

num_tests = int(raw.pop(0))
results = []
cases = []

for i in range(num_tests):
	case = [None, []]
	N, G = [int(num) for num in raw[0].split(' ')]
	case[0] = G
	for j in range(N):
		case[1].append(int(raw[j+1]))
	cases.append(case)
	raw = raw[N+1:]

print("Evaluating cases")

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