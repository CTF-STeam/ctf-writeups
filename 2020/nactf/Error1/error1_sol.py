from functools import reduce
from binascii import unhexlify

enc = '010011011010011010100011011001111110111101000101010011110111010101110110100110001100000111011101100100101111011010110001010011001110011010101111010111111010111010110111010111110110100110011011001101101101011101000111101000110100001010110100100001110110011110111011111101111000001100100011011010010111101100100100000011001101000001001010100000100111001011111101'
enc = [enc[i:i + 15] for i in range(0, len(enc), 15)]
#print(enc)

def correct(enc):
    enc = [int(i) for i in enc]
    #print(enc)
    #print([j for j, bit in enumerate(enc) if bit])
    pos = reduce(lambda a, b: int(a) ^ int(b), [j + 1 for j, bit in enumerate(enc) if bit])
    enc[pos - 1] = int(not enc[pos - 1])
    #print(enc)
    enc = ''.join([str(i) for i in enc])
    return enc[2] + enc[4:7] + enc[8:]

flag = ''.join(correct(x) for x in enc)
flag = unhexlify('%x' % int(flag, 2))
print(flag)

