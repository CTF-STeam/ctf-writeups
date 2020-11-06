There are 4 parity bits, with 15 possibilities for each position, so it is possible to bruteforce them.

[A little modification of the code for error 1](https://github.com/CTF-STeam/ctf-writeups/blob/master/2020/nactf/Error2/error2_sol.py) is enough to solve this problem (the code is unoptimized but good enough to find the flag in about 10 seconds):

```
from functools import reduce
from itertools import product
from binascii import unhexlify

enc = '0110101001...1100111001' # omitted for readability
enc = [enc[i:i + 15] for i in range(0, len(enc), 15)]

def correct(x, a, b, c, d):
    x = [int(i) for i in x]
    parity = [x[a], x[b], x[c], x[d]]
    x = [k for j, k in enumerate(x) if j not in (a, b, c, d)]
    for j in range(4):
        x.insert(2 ** j - 1, parity[j])
    pos = reduce(lambda a, b: int(a) ^ int(b), [j + 1 for j, bit in enumerate(x) if bit])
    if pos > 15:
        return ''
    x[pos - 1] = int(not x[pos - 1])
    x = [k for j, k in enumerate(x) if j not in (0, 1, 3, 7)]
    x = ''.join([str(i) for i in x])
    return x

for a, b, c, d in product(range(15), range(15), range(15), range(15)):
    flag = ''.join(correct(x, a, b, c, d) for x in enc)
    try:
        flag = unhexlify('%x' % int(flag, 2))
        if b'nactf{' in flag:
            print(flag)
    except:
        continue
print('Done')
```

Flag: `nactf{err0r_c0rr3cti0n_w1th_th3_c0rr3ct_f1le_q73xer7k9}`
