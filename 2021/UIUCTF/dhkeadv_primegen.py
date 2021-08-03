from Crypto.Util.number import *

while True:
    p = 2
    while p.bit_length() < 1024:
        p *= getPrime(16)
    if p.bit_length() < 2048:
        p = p + 1
    if isPrime(p):
        print(p)
        break
    else:
        print('Failed')
