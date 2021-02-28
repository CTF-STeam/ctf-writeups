import requests
from bs4 import BeautifulSoup
from binascii import hexlify, unhexlify
from base64 import b64decode

URL = 'http://167.71.246.232:8080/crypto.php'

def encrypt(pt):
    #print(hexlify(pt).decode())
    post_data = { 'text_to_encrypt': pt.decode(), 'do_encrypt': 'Encrypt' }
    r = requests.post(URL, data=post_data)
    soup = BeautifulSoup(r.text, 'html.parser')
    return hexlify(b64decode(soup.b.text)).decode()

def find_next(kf):
    ln = len(kf)
    if ln % 16 != 15:
        prefix = b'A' * (15 - ln % 16)
        start_ct = (ln - ln % 16) << 1
    else:
        prefix = b'A' * 16
        start_ct = (ln - ln % 16 + 16) << 1
    ct = encrypt(prefix)
    print(ct)
    ct = ct[start_ct:start_ct + 32]
    print(ct)
    for c in b'etoanihsrdlucgwyfmpbkvjxqz_0123456789{}0ETOANIHSRDLUCGWYFMPBKVJXQZ':
        print(prefix + kf + bytes([c]))
        ctt = encrypt(prefix + kf + bytes([c]))
        print(ctt)
        ctt = ctt[start_ct:start_ct + 32]
        print(ctt)
        if ct == ctt:
            return c

known_flag = b'f'

#print(encrypt(b'a'))

while not b'}' in known_flag:
    c = find_next(known_flag)
    known_flag += bytes([c])
    print(known_flag)
