print("Reading input file")

input_file = "line_by_line_input.txt"
cases = []

with open(input_file, "r") as f:
	num_tests = int(f.readline())
	for _ in range(num_tests):
		N, P = [int(a) for a in f.readline().split(" ")]
		cases.append([N, P])


print("Evaluating cases")

results = []

for N, P in cases:
	# Normalize P to range [0, 1]
	P = P/100

	# Compute new probability needed, and take difference with P
	result = P**((N - 1) / N) - P

	# Record results, re-mapping to range [0, 100]
	results.append(100 * result)


print("Saving results")

with open("results.txt", "w") as f:
	for i, result in enumerate(results):
		f.write(f"Case #{i+1}: {result}\n")

print("Complete")