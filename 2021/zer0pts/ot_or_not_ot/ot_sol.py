from Crypto.Util.number import *
from base64 import b64encode, b64decode
from pwn import *

r = remote('crypto.ctf.zer0pts.com', 10130)

r.recvuntil('Encrypted flag: ')
ct = r.recvuntil('\n').decode()
print(f'Encrypted flag: {ct}')
ct = b64decode(ct)
iv = b64encode(ct[:16])
ct = b64encode(ct[16:])
print(f'IV: {iv}')
print(f'Ciphertext: {ct}')

r.recvuntil('p = ')
p = int(r.recvuntil('\n').decode())
print(f'p = {p}')

r.recvuntil('key.bit_length() = ')
bln = int(r.recvuntil('\n').decode())
print(f'key.bit_length() = {bln}')

key = ''
while len(key) < bln:
    r.recvuntil('t = ')
    t = int(r.recvuntil('\n').decode())
    print(f't = {t}')
    a = 2
    b = a * (p - 1) % p
    c = inverse(t, p)
    d = inverse(a, p)
    print(r.recvuntil('a = ').decode() + str(a))
    r.sendline(str(a))
    print(r.recvuntil('b = ').decode() + str(b))
    r.sendline(str(b))
    print(r.recvuntil('c = ').decode() + str(c))
    r.sendline(str(c))
    print(r.recvuntil('d = ').decode() + str(d))
    r.sendline(str(d))
    r.recvuntil('x = ')
    x = int(r.recvuntil('\n').decode())
    print(f'x = {x}')
    r.recvuntil('y = ')
    y = int(r.recvuntil('\n').decode())
    print(f'y = {y}')
    r.recvuntil('z = ')
    z = int(r.recvuntil('\n').decode())
    print(f'z = {z}')
    xz = x * z % p
    if xz == 1 or xz == p - 1:
        key = '0' + key
    else:
        key = '1' + key
    yz = y * z % p
    if yz == 1 or yz == p - 1:
        key = '0' + key
    else:
        key = '1' + key
    print(f'Key: {key}')
print(f'IV: {iv}')
print(f'Ciphertext: {ct}')
r.interactive()
