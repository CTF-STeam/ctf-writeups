from Crypto.Util.number import long_to_bytes, bytes_to_long
from gmpy2 import mpz, to_binary
#from secret import flag, key

ALPHABET = bytearray(b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ#")

def base_n_encode(bytes_in, base):
	return mpz(bytes_to_long(bytes_in)).digits(base).upper().encode()

def base_n_decode(bytes_in, base):
	bytes_out = to_binary(mpz(bytes_in, base=base))[:1:-1]
	return bytes_out

def encrypt(bytes_in, key):
	out = bytes_in
	for i in key:
		#print(i)
		out = base_n_encode(out, ALPHABET.index(i))
	return out

def decrypt(bytes_in, key):
	out = bytes_in
	for i in key:
		out = base_n_decode(out, ALPHABET.index(i))
	return out

def all_valid(b):
    return all(x >= 32 and x < 128 for x in b)

def bf_key(flag_enc):
    for c in ALPHABET:
        try:
            flag = base_n_decode(flag_enc, ALPHABET.index(c))
            if all_valid(flag):
                    return c, flag
        except:
                continue
    return None

with open("flag_enc", "rb") as f:
    flag_enc = f.read()
print(flag_enc[:16])

key = ''
while len(flag_enc) > 16:
    c, flag_enc = bf_key(flag_enc)
    key += chr(c)
    print(key, flag_enc[:16])
