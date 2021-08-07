#!/usr/bin/env python
from pwn import *

def count(str):
    return len([x for x in str if x < 0x80]), len([x for x in str if x >= 0x80])

def guess(str):
    print(str)
    c = count(str)
    print(c)
    if c[0] > 76:
        return 'and'
    elif c[0] < 48:
        return 'or'
    else:
        return 'xor'

r = remote('challenges.ctfd.io', 30044)
r.recvuntil('\n')

for x in range(256):
    #r.recvuntil('Round')
    print(r.recvuntil('\n').rstrip().decode())
    str = r.recvuntil('\n').rstrip().decode()
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

r.interactive()
