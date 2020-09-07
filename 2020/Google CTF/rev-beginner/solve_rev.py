#!/usr/bin/python3 -u
from Crypto.Util.number import long_to_bytes, bytes_to_long
from binascii import hexlify

flag = 0x0AAF986EB34F823D4385F1A8D49B45876
#flag ^= 0x10
#print(hex(flag))
flag -= 0x6763746613371337FEE1DEADDEADBEEF
#print(hex(flag))

'''
print()
flag = b'CTF{0123456789}'[::-1]
print(flag)
print()
# C98640.{}571T32F
flag = 0x433938363430007b7d35373154333246
print(hex(flag))
flag += 0x6763746613371337FEE1DEADDEADBEEF
print(hex(flag))
flag ^= 0xAAF986EB34F823D4385F1A8D49B45876
print(hex(flag))
'''

order = [0,0xD,0xC,0xA,8,4,0xF,3,0xE,9,0xB,5,1,7,6,2]
def shuffle(s):
  res = ''
  for i in order:
    res += s[i]
  return res

flag = 'CTF{S0MEf0rM3!}\x00'
#flag = 'CTF{0123456789}\x00'
print(flag)
flag = shuffle(flag)
print(flag)
flag = hexlify(flag.encode())
print(flag.decode())
# C98640.{}571T32F
flag = int(flag, 16)
#flag = 0x432133726653007b7d304d3054444d46
print(hex(flag))
flag += 0x6763746613371337FEE1DEADDEADBEEF
print(hex(flag))
flag ^= 0xAAF986EB34F823D4385F1A8D49B45876
print(hex(flag))
'''
def reverse(add, xor, result, carry = 0):
    result ^= xor
    result -= add
    if result < 0:
        result += 0x100
    x = result
    print(hex(x), chr(x))
    return x

reverse(0xef, 0x76, ord('C'))
reverse(0xbe, 0x58, ord('T'))
reverse(0xad, 0xb4, ord('F'))
reverse(0xde, 0x49, ord('{'))
reverse(0xe1, 0x5f, ord('M'))
reverse(0xfe, 0x38, ord('D'))
reverse(0x13, 0x23, ord('0'))
reverse(0x63, 0xf9, ord('}'))
reverse(0x74, 0x86, ord('!'))
reverse(0x66, 0xeb, ord('3'))
reverse(0x37, 0xf8, ord('r'))
reverse(0xad, 0x8d, ord('S'))
reverse(0xde, 0x1a, ord('1'))
reverse(0x67, 0xaa, 0x00)
'''
