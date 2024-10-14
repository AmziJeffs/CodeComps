# Key observation: We only care about cases where some line contains a 
# majority of the points. When this line exists, we can easily find it
# by random sampling (each time we sample two points, we have a 1/4 chance
# to find the line, so just sample ~50+ times for overwhelming probability).

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

results = []
start_time = time.time()
for case_num, case in enumerate(cases):
	K = 50
	best = len(case)
	# Perform K random samples
	for i in range(K):
		ant1, ant2 = random.sample(case, k=2)
		perp = (ant2[1] - ant1[1], ant1[0]-ant2[0]) # Normal vector to line of interest
		vals = [perp[0]*ant[0] + perp[1]*ant[1] for ant in case] # Compute dot product of each ant with normal
		_, count = Counter(vals).most_common()[0] # Find the largest number of ants that lie on a line with this slope
		best = min(best, len(case) - count) # Update best count
	results.append(best)

	print(f"For case {case_num+1}, {best} ants out of {len(case)} must move.")
	print(f"Time elapsed: {round(time.time()-start_time, 2)} seconds.")
	print("######")

print("Saving results")

with open('results.txt', 'w') as f:
	for i, count in enumerate(results):
		f.write(f'Case #{i+1}: {count}\n')

print("Complete")