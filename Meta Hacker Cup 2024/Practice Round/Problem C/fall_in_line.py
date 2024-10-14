import time
import random
from collections import Counter

print("Reading input file")

input_file = "fall_in_line_input.txt"
cases = []

with open(input_file, "r") as f:
	num_tests = int(f.readline())
	for _ in range(num_tests):
		num_ants = int(f.readline())
		case = []
		for _ in range(num_ants):
			case.append([int(coord) for coord in f.readline().split(" ")])
		cases.append(case)


print("Evaluating cases")

# Key observation: We only care about cases where some line contains a 
# majority of the points. When this line exists, we can easily find it
# by random sampling (each time we sample two points, we have a 1/4 chance
# to find the line, so just sample K = ~50+ times for overwhelming probability).

results = []
start_time = time.time()
K = 50

for case_num, case in enumerate(cases):
	best = len(case)
	for _ in range(K):
		# Sample two distinct ants
		ant1, ant2 = random.sample(case, k = 2)

		# Compute normal vector to line between ants
		perp = (ant2[1] - ant1[1], ant1[0] - ant2[0])

		# Compute dot product of every ant with normal vector
		vals = [perp[0] * ant[0] + perp[1] * ant[1] for ant in case]

		# Find the largest number of ants on any line perpendicular to normal
		_, count = Counter(vals).most_common()[0]

		# Update our best count
		best = min(best, len(case) - count)

		# If we found a line with the majority of ants on it, we can stop
		if best < len(case) // 2:
			break

	results.append(best)

	print(f"For case {case_num+1}, {best} ants out of {len(case)} must move.")
	print(f"Time elapsed: {round(time.time()-start_time, 2)} seconds.")
	print("")

print("Saving results")

with open("results.txt", "w") as f:
	for i, count in enumerate(results):
		f.write(f"Case #{i+1}: {count}\n")

print("Complete")