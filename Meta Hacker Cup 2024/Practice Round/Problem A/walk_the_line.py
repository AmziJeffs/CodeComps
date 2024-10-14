print("Reading input file")

input_file = "walk_the_line_input.txt"
cases = []

with open(input_file, "r") as f:
	num_tests = int(f.readline())
	for _ in range(num_tests):
		N, K = [int(a) for a in f.readline().split(" ")]
		animal_speeds = []
		for _ in range(N):
			animal_speeds.append(int(f.readline()))
		cases.append([K, animal_speeds])


print("Evaluating cases")

results = []

for K, animal_speeds in cases:
	# Compute the number of animals, and the fastest speed among them
	N = len(animal_speeds)
	quickest = min(animal_speeds)

	# If more than one animal, the fastest animal should ferry them all
	# repeatedly, taking a total of N - 2 trips back and forth, plus
	# one final trip carrying the last animal.
	# If only one animal, simply cross the bridge and check if the speed
	# is fast enough.
	if N > 1:
		results.append(quickest * (2 * (N - 2) + 1) <= K) 
	else:
		results.append(quickest <= K)


print("Saving results")

with open("results.txt", "w") as f:
	for i, result in enumerate(results):
		f.write(f"Case #{i+1}: {"YES" if result else "NO"}\n")


print("Complete")