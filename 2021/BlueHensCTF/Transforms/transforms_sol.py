#!/usr/bin/env python
from pwn import *
from Crypto.Util.number import *
from binascii import unhexlify

def convert_to_bytes(cfrom, data):
    print(data)
    if cfrom == 'hexdigest':
        data = unhexlify(data.decode())
    elif cfrom == 'integer':
        data = long_to_bytes(data.decode())
    elif cfrom == 'bytearray':
        data = bytes(eval(data.decode()))
    elif cfrom == 'string':
        return data
    else:
        data = eval(data.decode())
    return data

def convert_from_bytes(cto, data):
    if cto == 'hexdigest':
        data = hex(bytes_to_long(data))[2:]
        if len(data) % 2:
            data = '0' + data
    elif cto == 'integer':
        data = str(bytes_to_long(data))
    elif cto == 'bytearray':
        data = str([x for x in data])
    elif cto == 'string':
        return data.decode('latin-1')
    else:
        data = eval(data.decode())
    return data

r = remote('challenges.ctfd.io', 30008)
r.recvuntil('\n')

for x in range(100):
    print(x + 1)
    print(r.recvuntil('\n').rstrip().decode())
    #r.recvuntil('\n')
    r.recvuntil('convert ')
    cfrom = r.recvuntil(' to ').decode().replace(' to ', '')
    cto = r.recvuntil(': ').decode().replace(': ', '')
    print(f'convert from {cfrom} to {cto}')
    data = r.recvuntil('\n').rstrip().replace(b' @@@@@', b'')
    data = convert_to_bytes(cfrom, data)
    print(data)
    data = convert_from_bytes(cto, data)
    print(data)
    r.recvuntil('> ')
    r.sendline(data)
    result = r.recvuntil('\n')
    print(result.decode())

r.interactive()

'''
    #print(str)
    str = eval(str)
    g = guess(str)
    print(g)
    r.recvuntil('Which function was used?\n')
    r.sendline(g)
    res = r.recvuntil('\n').decode()
    print(res)
    if 'wrong' in res:
        print(r.recvuntil('\n').decode())
'''

