from binascii import unhexlify

encrypted = unhexlify('031a1b1c1d1e1f2f4b0e0b4807234b51210f4f102a074c412a2f2120302b2b25')

key = b'abcdefghijklmnopqrstuvwxyzabcdef'
flag = [0] * 32
for i in range(31, -1, -1):
    flag[i] = encrypted[31 - i] ^ key[31 - i] ^ i
flag = ''.join(chr(x) for x in flag)
print(flag)

