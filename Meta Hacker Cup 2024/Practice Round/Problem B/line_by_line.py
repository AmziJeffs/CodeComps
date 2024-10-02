input_file = 'line_by_line_input.txt'

print("Reading input file")

with open(input_file, 'r') as f:
	raw = f.read().split('\n')

num_tests = int(raw.pop(0))
results = []

print("Evaluating cases")

for i in range(num_tests):
	N, P = [int(num) for num in raw[i].split(' ')]
	P = P/100
	results.append(100 * (P**((N-1)/N)-P))

print("Saving results")

with open('results.txt', 'w') as f:
	for i, result in enumerate(results):
		f.write(f'Case #{i+1}: {result}\n')

print("Complete")