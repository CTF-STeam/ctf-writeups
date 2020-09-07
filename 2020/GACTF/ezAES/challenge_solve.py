from Crypto.Cipher import AES
import binascii
import hashlib

KEY_first = 'T0EyZaLRzQmNe2'
cipher1 = 'c70000000000a32c412a3e7474e584cd'
cipher2 = '72481dab9dd83141706925d92bdd39e4'
plain1 = 'ow about it?\x1fnrf'
plain2 = 'O[\xef\xcb\x0e:\n\n\n\n\n\n\n\n\n\n'

def decrypt(cipher, iv, passphrase):
    aes = AES.new(passphrase, AES.MODE_CBC, iv)
    return aes.decrypt(cipher)

# iterate through relevant ascii range
for i in range(128):
    for j in range(128):
        key = bytes(KEY_first + chr(i) + chr(j), "utf-8")
        dec_plain2 = decrypt(binascii.unhexlify(cipher2), binascii.unhexlify(cipher1), key)
        if dec_plain2[14] == ord(plain2[14]) and dec_plain2[15] == ord(plain2[15]):
            print('[+] Found plain2: %s with key: %s' % (dec_plain2, key))

key = b'T0EyZaLRzQmNe2pd'
KEYSIZE = len(key)

def pad(message):
    p = bytes((KEYSIZE - len(message) % KEYSIZE) * chr(KEYSIZE - len(message) % KEYSIZE),encoding='utf-8')
    return message + p

h = hashlib.md5(key).hexdigest()
SECRET = binascii.unhexlify(h)[:10]
message = pad(b'AES CBC Mode is commonly used in data encryption. What do you know about it?' + SECRET)
print('[+] Message:', message)

cipher = [None] * 5 + [binascii.unhexlify(cipher2)]
plain = [message[(i<<4):(i<<4) + 16] for i in range(6)]
for i in range(5, 0, -1):
    cipher[i - 1] = decrypt(cipher[i], plain[i], key)
print('[+] Cipher:', cipher)
iv = decrypt(cipher[0], plain[0], key)
print('[+] IV:', iv)
print('[+] Flag: gactf{%s}' % iv.decode('utf-8'))

