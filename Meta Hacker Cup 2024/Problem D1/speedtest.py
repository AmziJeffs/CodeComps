import time

input_file = 'line_of_delivery_part_1_input.txt'

print("Reading input file")
starttime = time.time()

with open(input_file, 'r') as f:
	num_tests = int(f.readline())
	cases = []
	for i in range(num_tests):
		num_stones, goal = [int(a) for a in f.readline().split(" ")]
		case = [goal, []]
		for j in range(num_stones):
			case[1].append(int(f.readline()))
		cases.append(case)

print(len(cases))

print(f"Done, in {time.time()-starttime:.4f} seconds")