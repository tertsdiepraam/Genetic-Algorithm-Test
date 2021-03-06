# Genetic-Algorithm-Test
Simple implementation of a genetic algorithm using Python. Which is used to approximate sin(x).

## Methodology
There are to programs in this repository. The first is a simple, naïve implementation of a genetic algorithm, which evolves by altering a string. The second is a work-in-progress version, which has improved understanding of the mathematics involved, by modeling the structures as a tree. Each node in the tree has an associated operator and arguments, which could be a number or another node.

The programs try to approximate sin(x) on the interval [0,pi/2], by mutating polynomials randomly, selecting the top half of the sequences and repeating the cycle with these polynomials.

## Results
Below are some of the graphs the simple program generated. The graphs are drawn using [Desmos](https://www.desmos.com/calculator). The red line represents sin(x) and the orange line represents the graph generated by the program.
![First result](https://github.com/tertsdiepraam/Genetic-Algorithm-Test/blob/master/images/2.PNG?raw=true)

![Second result](https://github.com/tertsdiepraam/Genetic-Algorithm-Test/blob/master/images/2.PNG?raw=true)
