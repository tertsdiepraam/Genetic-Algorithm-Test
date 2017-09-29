import math
import random
import functools

# Each operator has a lmabda function which is used to solve the Formula
# and it has a mathmatical representation, which will be formatted using the
# format method for strings
operators = {
	'add': (lambda x, y: x+y, '({}+{})'),
	'sub': (lambda x, y: x-y, '({}-{})'),
	'mul': (lambda x, y: x*y, '({}*{})'),
	'div': (lambda x, y: x/y, '({}/{})'),
	#'pow': (lambda x, y: x**y, '({}^{})'),
	#'mod': (lambda x, y: x%y, '({}%{})'),
	#'sin': (math.sin, 'sin({})'),
	#'cos': (math.cos, 'cos({})'),
	#'abs': (abs, '|{}|'),
	#'fac': (math.factorial, '{}!'),
}

settings = {
	'mutability': 10, # in %
	'num_sequences': 100,
	'depth': 5,
}

class Formula():
	def __init__(self, operator, *args):
		self.operator = operator
		self.arguments = args
		self.memo = {}
		self.fitness = None

	def set_args(self, *args):
		self.arguments = args

	def __repr__(self):
		return str(self)

	def __str__(self):
		return ''.join(
			str(x) for x in (
				self.operator,
				'(',
				*(','.join(str(y) for y in self.arguments),
				')'
				)
			)
		)

	def math_repr(self):
		# generates a representation, which can be understood by graphical calculators to plot the appropriate graphical
		# the representation is based on the representations defined with the operators
		args = [arg.math_repr() if type(arg) is Formula else arg for arg in self.arguments]
		return operators[self.operator][1].format(*args)

	def walk_through(self):
		yield self.operator
		for argument in self.arguments:
			if type(argument) is Formula:
				for item in argument.walk_through():
					yield item
			else:
				yield argument

	def walk_through_arguments(self):
		for argument in self.arguments:
			if type(argument) is Formula:
				for item in argument.walk_through_arguments():
					yield item
			else:
				yield argument

	def walk_through_operators(self):
		yield self.operator
		for argument in self.arguments:
			if type(argument) is Formula:
				for item in argument.walk_through_operators():
					yield item

	def solve(self, n):
		if n in self.memo.keys():
			return self.memo[n]
		arguments = []
		for arg in self.arguments:
			if type(arg) == Formula:
				arguments.append(arg.solve(n))
			elif arg == 'x':
				arguments.append(n)
			else:
				arguments.append(int(arg))
		self.memo[n] = operators[self.operator][0](*arguments)
		return self.memo[n]

	# methods below must NOT change the object itself, but only return a new Formula
	# to ensure correct memoization
	@staticmethod
	def generate(max_depth):
		assert max_depth >= 0, "max_depth can not be lower than zero, it is {}".format(max_depth)
		operator = random.choice(list(operators.keys()))
		arguments = []
		for i in range(operators[operator][0].__code__.co_argcount):
			if max_depth and random.randint(0,1):
				arguments.append(Formula.generate(max_depth-1))
			else:
				arguments.append(rand_num_or_x())
		return Formula(operator, *arguments)

	def copy(self):
		return Formula(self.operator, *self.arguments.deepcopy())

	def mutate(self):
		# TODO: needs mutation which will add or remove functions
		if random.randint(0, 100) <= settings['mutability']:
			operator = random.choice(list(operators.keys()))
		else:
			operator = self.operator
		arguments = []
		for i in range(operators[operator][0].__code__.co_argcount):
			if len(self.arguments) > i:
				if random.randint(0, 100) <= settings['mutability']:
					arguments.append(self.arguments[i])
				else:
					arguments.append(rand_num_or_x())
			else:
				arguments.append(rand_num_or_x())
		return Formula(operator, *arguments)

	def crossover(self, other):
		raise NotImplementedError

def rand_num_or_x():
	if random.randint(0,3):
		return random.randint(1,99)
	else:
		return 'x'

def float_range(start, stop, step=1):
	# same as range() but accepts floats
	counter = start
	while counter < stop:
		counter += step
		yield counter

def get_fitness(formula, check, start, stop, step):
	scores = []
	if formula.fitness:
		return formula.fitness
	for i in float_range(start, stop, step):
		x = i
		try:
			ans = formula.solve(i)
		except ZeroDivisionError:
			continue
		try:
			check_ans = check(i)
		except ZeroDivisionError:
			continue
		scores.append(abs(ans-check(i)))
	if len(scores) == 0:
		return None
	formula.fitness = sum(scores)/len(scores)
	return formula.fitness

@functools.cmp_to_key
def compare(item1, item2):
	# custom function which is used by the sort method
	# it sorts None to the end to ensure that those Formulas are left out in the next generation
	fit1 = get_fitness(item1, math.sin, 0.1, math.pi/2, 0.1)
	fit2 = get_fitness(item2, math.sin, 0.1, math.pi/2, 0.1)
	try:
		return fit1 < fit2
	except TypeError:
		if type(fit1) in [int, float]:
			return -1
		elif type(fit2) in [int, float]:
			return 1
		else:
			return 0

def main():
	formula_list = [Formula.generate(settings['depth']) for _ in range(settings['num_sequences'])]
	formula_list.sort(key=compare)
	iteration = 1
	while True:
		print("Iteration:   ", iteration)
		print("Best Formula:", formula_list[0])
		print("Mathmatical: ", formula_list[0].math_repr())
		print("Fitness:     ", formula_list[0].fitness)
		print()
		formula_list = formula_list[:int(len(formula_list)/2)]
		formula_list += [f.mutate() for f in formula_list]
		formula_list.sort(key=compare)
		iteration += 1

# testing
def test():
	F = Formula.generate(4)
	print(F)
	print(F.math_repr())
	print(F.solve(10))

if __name__ == '__main__':
	#main()
	test()
