#!/bin/env python2

import string
import random

dict = string.ascii_letters + string.digits + '{}_@$!'


def load64(b):
    return sum((b[i] << (8*i)) for i in range(8))


def pad(x, n):
    # n = 16
    x = hex(x).lstrip('0x').strip('L')
    return '0'*(n - len(x)) + x


def ACAC(x):
    assert x < 2**64
    x ^= x >> 27
    x *= 0x2a636f7468616e2b
    x &= 0xffffffffffffffff
    x ^= x >> 34
    x *= 0x49534954445455c9
    x &= 0xffffffffffffffff
    x ^= x >> 23
    return x


def encode(flag):
    result = ''
    for i in range(0, len(flag)-8, 8):
        result += pad(ACAC(load64(flag[i:i+8])), 16)
    return result


if __name__ == "__main__":
    with open('flag.txt', 'rb') as f:
        data = f.read()

    # You know what this mean, right?
    data = list(data)
    for i, j in enumerate(data):
        if j not in dict:
            data[i] = chr(random.randint(0x7f, 0xff))
    data = bytearray(data)

    cipher = encode(data)

    with open('cipher.txt', 'w') as g:
        g.write(cipher)
