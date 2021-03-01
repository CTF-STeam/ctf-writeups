import base64
import json
from Crypto.Util.number import *
from factordb.factordb import FactorDB
from math import prod

def factorize(n):
    f = FactorDB(n)
    f.connect()
    return f.get_factor_list()
    '''
    switcher = {
        50041451: [7069, 7079],
        33983429: [199, 389, 439],
        27939893: [223, 349, 359]
        }
    return switcher.get(n, [n])
    '''

def phi(n):
    return prod([x - 1 for x in factorize(n)])

encrypted_data = '7694194 23569352 381554 8429204 2700372 20059219 20474614 4048990 21043567 8061850 1841146 4801372 16942924 3981319 19362534'
encrypted_data = list(map(int, encrypted_data.split()))
print(encrypted_data)
key = 'eyJjb21tb25fa2V5IjogW1sxLCA1MDA0MTQ1MV0sIFsxMzc3NjIxNSwgMzM5ODM0MjldLCBbMzUzNzY5MSwgMjc5Mzk4OTNdLCBbNTYzODI2MSwgMjI5Nzc1MDNdLCBbMTI0ODA1ODMsIDE3MTQ1ODk5XSwgWzIzMDQzNzk5LCAyNTk5MTAzM10sIFs0Mjk4NzQyNSwgNDU2NzQ3MzFdLCBbMTAyMTAwOTcsIDE5NTMxMDg3XSwgWzI1Nzg5NzYzLCAyNjUzNDk5M10sIFsxMTg3NzY2MSwgMjAyNTQwODFdLCBbMTc4MTE3NzEsIDIzMTQ2MTIxXSwgWzEyMTAwODc3LCAyNTI1MDQyOV0sIFsxNTc5NTA4MywgMTgzODU2NjldLCBbNjM0ODkxOSwgMTM3Nzg5ODddLCBbMTQ3NjAzMDMsIDI2MzEwMTMzXV0sICJwcml2YXRlX2tleSI6IFtbMSwgMV0sIFsxMjYxOTg5NywgMTc5MDc4MzNdLCBbMTA0NDM1NjksIDEyODgxNjkyXSwgWzEzNDU4NjE3LCAxMTU4MTMxMF0sIFsxNDg4NTI4NywgMTY4NjU4NjddLCBbMTA0MTE5MDEsIDIxMjE5NzY5XSwgWzE0NDc1NjY1LCAxNjE0OTY5NV0sIFs2MTk2NzIxLCAxMDc0Nzk3MV0sIFsxOTk4NzQ3NywgMjU3ODEwNjldLCBbMTI3Njc0ODMsIDExMTU2NTQ3XSwgWzE2MDg1ODgzLCA3Mjg2MzkyXSwgWzIyOTc1NDQxLCAxNzkwODM4NV0sIFsxNjg4NTg0MywgMTAxOTA5MzNdLCBbNjQ2NTc5NywgNjIyOTc0MV0sIFs3MTk3ODUxLCA3MTMyODQwXV19'
key = json.loads(base64.b64decode(key))
print(key)

print("Your data is: ", end='', file=sys.stderr, flush=True)

for a, (b, n), (c, d) in zip(
    encrypted_data,
    key["common_key"],
    key["private_key"]
):
    #print(a, b, c, d, n, isPrime(n), phi(n))
    ab = pow(a, b, n)
    cd = pow(c, d, phi(n))
    #x = (a ** b) ** (c ** d)
    x = pow(ab, cd, n)
    c1 = chr((x % n) % 256)
    c2 = chr((x % n) // 256 % 256)
    c3 = chr((x % n) // 65536)

    print(c3, c2, c1, sep='', end='', flush=True)

print(flush=True)

print("Decoding finished!", file=sys.stderr, flush=True)

