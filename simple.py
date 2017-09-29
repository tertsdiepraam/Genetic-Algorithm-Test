import random
import math
# https://nl.mathworks.com/help/gads/how-the-genetic-algorithm-works.html

operators = ['+', '-', '*', '/']
max_int = 30
length = 31
mutability = 10
num_sequences = 100

class DNA:
	def __init__(self, sequence, fitness):
		self.sequence = sequence
		self.fitness = fitness

def generate(length):
	sequence = []
	for i in range(length):
		if i % 2 == 0:
			if not random.randint(0,2):
				sequence.append("x")
			else:
				sequence.append(str(random.randint(1,max_int)))
		else:
			sequence.append(random.choice(operators))
	return sequence

def crossover(father, mother):
	return [father[i] if math.randint(0,1) else mother[i] for i in range(len(father))]

def mutate(parent):
	sequence = []
	for char in parent:
		if not random.randint(0, mutability):
			if parent.index(char) % 2 == 0:
				if not random.randint(0,2):
					sequence.append("x")
				else:
					sequence.append(str(random.randint(1,max_int)))
			else:
				sequence.append(random.choice(operators))
		else:
			sequence.append(char)
	return sequence

def float_range(start, stop, step=1):
	counter = start
	while counter < stop:
		counter += step
		yield counter

def get_fitness(sequence, check):
	scores = []
	for i in float_range(0.1, math.pi, 0.1):
		x = i
		ans = eval("".join(sequence))
		scores.append(abs(ans-check(i)))
	return sum(scores)/len(scores)

if __name__ == "__main__":
	sequences = [generate(length) for i in range(num_sequences)]
	sequences.sort(key=lambda x: get_fitness(x, math.sin))
	iteration = 1
	while True:
		new_gen = [mutate(DNA) for DNA in sequences]
		sequences = [new_gen[i] if get_fitness(new_gen[i], math.sin) < get_fitness(sequences[i], math.sin) else sequences[i] for i in range(len(sequences))]
		if iteration % 100 == 0:
			best_seq = sorted(sequences, key= lambda seq: get_fitness(seq, math.sin))[0]
			print("Iteration:", iteration)
			print("Sequence:", "".join(best_seq))
			print("Deviation:", get_fitness(best_seq, math.sin))
			print()
		iteration += 1
