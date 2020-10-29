

import sympy

a = 2**768
b = 2**1024

with open('primes.txt', 'w') as f:
	for i in range(4000):
		f.write(str(sympy.randprime(a, b)) + '\n')