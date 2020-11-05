The second part of the video in the hint tells you the elegance of Hamming code, watch it and you know exactly what to do: [https://www.youtube.com/watch?v=b3NxrZOu_CE](https://www.youtube.com/watch?v=b3NxrZOu_CE)

For each group of 15 bits, xor the positions of all 1 bits and you'll get the position of the flipped bit:

```
from functools import reduce
from binascii import unhexlify

enc = '0100110110...1011111101' # omitted for readability
enc = [enc[i:i + 15] for i in range(0, len(enc), 15)]

def correct(enc):
    enc = [int(i) for i in enc]
    pos = reduce(lambda a, b: int(a) ^ int(b), [j + 1 for j, bit in enumerate(enc) if bit])
    enc[pos - 1] = int(not enc[pos - 1])
    enc = ''.join([str(i) for i in enc])
    return enc[2] + enc[4:7] + enc[8:]

flag = ''.join(correct(x) for x in enc)
flag = unhexlify('%x' % int(flag, 2))
print(flag)
```

Flag: `nactf{hamm1ng_cod3s_546mv3q9a0te}`
