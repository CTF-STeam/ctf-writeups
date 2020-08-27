from Crypto.Util.number import getRandomInteger, long_to_bytes
from functools import reduce

enc = '1b4eb59dce68c7d5173871ff3211a35bc8d089147c0c4c0f7cdf1b9489d4a640ee173557778095d84d0cd344e213100f2923e8ea96'
enc = bin(int(enc, 16))[2:].zfill(len(enc) * 4)

kpt = 'The flag is: '
kpt = ''.join(bin(ord(x))[2:].zfill(8) for x in kpt)

class LFSR:
	def __init__(self, size, salt, invert, register = 0):
		assert(size == 17 or size == 25)
		self.size = size
		if register != 0:
			self.register = register
		else:
			self.register = ((salt >> 3) << 4) + 8 + (salt & 0x7)
		self.taps = [0, 14]
		if size == 25:
			self.taps += [3, 4]
		self.invert = 1 if invert == True else 0
	def clock(self):
		output = reduce(lambda x, y: x ^ y, [(self.register >> i) & 1 for i in self.taps])
		self.register = (self.register >> 1) + (output << (self.size - 1))

		output ^= self.invert
		return output

LEN1 = 17
LEN2 = 25

def find_reg2(lfsr17):
        reg2 = ''
        for i in range(LEN2):
                reg2 += str(lfsr17.clock() ^ int(kpt[i]) ^ int(enc[i]))
        return int(reg2[::-1], 2)

def brute(salt1):
        lfsr17 = LFSR(17, salt1, True)
        reg2 = find_reg2(lfsr17)
        lfsr25 = LFSR(25, 0, False, reg2)
        pt = kpt[:25]
        for i in range(LEN2, len(enc)):
                x = lfsr17.clock() ^ lfsr25.clock() ^ int(enc[i])
                if i < len(kpt) and x != int(kpt[i]):
                        return False, None
                pt += str(x)
        return True, pt

for salt1 in range(1 << 16):
        found, pt = brute(salt1)
        if found:
                print('[+] Found: ', pt)
                print(long_to_bytes(int(pt, 2)))
