#!/usr/local/bin/python

import random
from Crypto.Util.number import bytes_to_long

with open('flag.txt', 'r') as f:
	m = f.read()

with open('primes.txt', 'r') as f:
	primes = f.readlines()


print("This is a game of luck")
print("Lets hope you get a modulus that can be FACTORED xD")
print("Good luck~")
input("Press enter for next triplet: ")

while(1):
	p = int(random.choice(primes))
	q = int(random.choice(primes))
	while(p == q):
		q = int(random.choice(primes))

	N = p*q
	e = 65537
	c = pow(bytes_to_long(bytes(m.encode('utf-8'))), e, N)

	print("="*79)
	print("N = {}".format(N))
	print("e = {}".format(e))
	print("c = {}".format(c))
	print("="*79)
	input("Press enter for next triplet: ")
