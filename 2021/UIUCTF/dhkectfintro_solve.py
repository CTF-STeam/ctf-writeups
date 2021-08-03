from Crypto.Cipher import AES
from binascii import unhexlify

# pad key to 16 bytes (128bit)
def pad_key(k):
    key = ""
    i = 0
    padding = "uiuctf2021uiuctf2021"
    while (16 - len(key) != len(k)):
        key = key + padding[i]
        i += 1
    key = key + k
    return bytes(key, encoding='ascii')

ciphertext = unhexlify('b31699d587f7daf8f6b23b30cfee0edca5d6a3594cd53e1646b9e72de6fc44fe7ad40f0ea6')

iv = bytes("kono DIO daaaaaa", encoding = 'ascii')
for k in range(31):
    key = pad_key(str(k))
    cipher = AES.new(key, AES.MODE_CFB, iv)
    flag = cipher.decrypt(ciphertext)
    if b'uiuctf' in flag:
        print(flag)
