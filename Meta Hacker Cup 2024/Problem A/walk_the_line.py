input_file = 'walk_the_line_input.txt'

print("Reading input file")

with open(input_file, 'r') as f:
	raw = f.read().split('\n')

num_tests = int(raw.pop(0))
results = []

print("Evaluating cases")

for i in range(num_tests):
	# Compute the number of animals, goal time, and speeds
	N, K = [int(num) for num in raw[0].split(' ')]
	animals = []
	for j in range(N):
		animals.append(int(raw[j+1]))

	quickest = min(animals) # Find the quickest animal to ferry all the others
	result = None
	if N > 1:
		result = (quickest * (2*(N-2) + 1) <= K) # quickest animal must cross there and back 
											     # for all but the last animal, for which
											     # it must cross only the final trip.
	else:
		result = (quickest <= K) # If only one animal, just need to check its speed
	
	# Store results and update list of cases
	results.append(result)
	raw = raw[N+1:]

print("Saving results")

with open('results.txt', 'w') as f:
	for i, result in enumerate(results):
		f.write(f'Case #{i+1}: {"YES" if result else "NO"}\n')

print("Complete")