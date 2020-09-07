### Main idea:
- If the same plaintext is xored with 2 different keys, xoring the ciphertexts will give the same result as xoring the key.
- Therefore if 2 ciphertexts have the same key length, the xored result will have the same block repeated (cyclic). This gives us the key length.
- We can get a lot of ciphertexts from the server, so collect 500 of them and we have lot of ciphertexts with the same key length.
- With 2 ciphertexts with different key lengths (co-prime), from the first byte of key1 we can reconstruct both keys and test all possible decrypted results.

The final step takes some effort, at first from analysis we knew the decrypted file contains non-ascii characters so we wasted a lot of time trying different file formats. Finally we looked for the flag in the decrypted files and found the plaintext with mixed English and German and Chinese (so crazy!!!)

### Step 1: collecting 500 ciphertexts

This was done using a [batch script](mtp_collect.bat) (under Windows XD)

```
@echo off

for /l %%x in (1, 1, 500) do (
   echo %%%x
   nc mtp.chujowyc.tf 4003 >> mtp_in.txt
)
```

### Step 2: finding ciphertexts with the same key length and recover the length

```
import binascii
import socket
from mtp_in import ct, ct2

ct = binascii.unhexlify(ct)
ct2 = binascii.unhexlify(ct2)

def xor(data, key):
    out = []
    for k in range(0, len(data), len(key)):
        block = data[k : k + len(key)]
        out.append(bytes([a ^ b for a, b in zip(block, key)]))
    return b''.join(out)

def is_cyclic_l(s, l):
    for st in range(l):
        for i in range(st, len(s), l):
            if s[st] != s[i]:
                return False
    return True

def is_cyclic(s):
    lmin = 128
    lmax = 256
    for l in range(lmin, lmax):
        if is_cyclic_l(s, l):
            return True, l
    return False, 0

def get_more_ct_fromfile(ct):
    file = open('mtp_in.txt', 'r')  
    while True: 
        line = file.readline().strip()
        if not line: 
            break
        if len(line) != 103678:
            continue
        b = binascii.unhexlify(line)
        x = xor(ct, b)
        c, l = is_cyclic(x)
        if c:
            print(l)
    file.close() 
```

After this we get: 2 ciphertexts with length 203 and 194.

### Step 3: bruteforce the first byte of key1 and find the flag

```
LEN = len(ct)
K1L = 203
K2L = 194

def find_combo(x):
    k1 = [0] * K1L
    k2 = [0] * K2L
    k1[0] = x
    for i in range(0, LEN, K1L):
        p = k1[0] ^ ct[i]
        k2[i % K2L] = p ^ ct2[i]
    for i in range(0, LEN, K2L):
        p = k2[0] ^ ct2[i]
        k1[i % K1L] = p ^ ct[i]
    k1 = bytes(k for k in k1)
    k2 = bytes(k for k in k2)
    p1 = xor(ct, k1)
    p2 = xor(ct2, k2)
    c = xor(p1, k1)
    assert c == ct
    c = xor(p2, k2)
    assert c == ct2
    file = open('mtp\\' + str(x) + '.txt', 'wb')
    file.write(p1)
    file.close()
    return b'chCTF' in p1

for c in range(256):
    x = find_combo(c)
    if x:
        print(c, x)
```

Output:

```
59 True
```

And here's the content of [59.txt](59.txt):

```
$ grep chCTF *
59.txt:  3. [[3]](../Text/chapter01.xhtml#fnref3) Parmenides （约前515一？），希腊哲学家，chCTF{arbitr4tily_l0n9_0n3_t1m3_p4d_46723469238746952873642934786529} 公认的埃利亚学派（Eleatic）的最杰出者。​
```
