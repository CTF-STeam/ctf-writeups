#!/usr/bin/env python3
import binascii
import socket
from mtp_in import ct, ct2

ct = binascii.unhexlify(ct)
ct2 = binascii.unhexlify(ct2)

def xor(data, key):
    out = []
    for k in range(0, len(data), len(key)):
        block = data[k : k + len(key)]
        out.append(bytes([a ^ b for a, b in zip(block, key)]))
    return b''.join(out)

def get_ct():
    HOST = 'mtp.chujowyc.tf'
    PORT = 4003
    buffer = b''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            try:
                chunk = s.recv(4096)
                buffer += chunk
            except BlockingIOError:
                pass

            #print(len(buffer))
            if b'\n' in buffer:
                break
    return buffer.rstrip()

def is_cyclic_l(s, l):
    for st in range(l):
        #print('st', st)
        #print('l', l)
        for i in range(st, len(s), l):
            #print('n', n)
            if s[st] != s[i]:
                #print(st, i, s[st], s[i])
                return False
    return True

def is_cyclic(s):
    lmin = 128
    lmax = 256
    for l in range(lmin, lmax):
        if is_cyclic_l(s, l):
            return True, l
    return False, 0

def get_more_ct():
    for x in range(1024):
        print(x)
        b = binascii.unhexlify(get_ct())
        print(len(b))
        x = xor(ct, b)
        c, l = is_cyclic(x)
        if c:
            print(binascii.hexlify(b))
            print(l)
            break

def get_more_ct_fromfile(ct):
    file = open('mtp_in.txt', 'r')  
    while True: 
        line = file.readline().strip()
        if not line: 
            break
        #print(len(line))
        if len(line) != 103678:
            continue
        b = binascii.unhexlify(line)
        #print(len(b))
        x = xor(ct, b)
        c, l = is_cyclic(x)
        if c:
            #print(binascii.hexlify(b))
            print(l)
            #break
    file.close() 

LEN = len(ct)
K1L = 203
K2L = 194
#K3L = 133

'''
def apply(pt, ctx, pos, kc, klen):
    #print(pt[:10])
    for i in range(pos % klen, LEN, klen):
        c = ctx[i] ^ kc
        if pt[i] < 0:
            pt[i] = c
            if not apply(pt, ct, i, pt[i] ^ ct[i], K1L):
                return False
            if not apply(pt, ct2, i, pt[i] ^ ct2[i], K2L):
                return False
            if not apply(pt, ct3, i, pt[i] ^ ct3[i], K3L):
                return False
        elif pt[i] != c:
            #print(i, pt[i], c)
            return False
    return True

def test_char(c):
    pt = [-1] * LEN
    return apply(pt, ct, 0, c, K1L)
'''

def find_combo(x):
    k1 = [0] * K1L
    k2 = [0] * K2L
    k1[0] = x
    for i in range(0, LEN, K1L):
        p = k1[0] ^ ct[i]
        k2[i % K2L] = p ^ ct2[i]
    #print(k1[0] ^ ct[0])
    for i in range(0, LEN, K2L):
        p = k2[0] ^ ct2[i]
        k1[i % K1L] = p ^ ct[i]
    #print(k2[0] ^ ct2[0])
    k1 = bytes(k for k in k1)
    #print(k1)
    k2 = bytes(k for k in k2)
    p1 = xor(ct, k1)
    p2 = xor(ct2, k2)
    c = xor(p1, k1)
    assert c == ct
    c = xor(p2, k2)
    assert c == ct2
    #print(p1[:20])
    #print(p2[:10])
    '''
    file = open('mtp\\' + str(x) + '.txt', 'wb')
    file.write(p1)
    file.close()'''
    #assert p1 == p2
    #k4 = xor(p1, ct5)
    #cy, len = is_cyclic(k4)
    #cy = test_cyclic(p1)
    return b'chCTF' in p1
    #print(x, k1, k2)
    #return True

'''
def test_cyclic(pt):
    file = open('mtp_in.txt', 'r')  
    for _ in range(10): 
        line = file.readline().strip()
        if not line: 
            break
        if len(line) != 103678:
            continue
        b = binascii.unhexlify(line)
        #print(len(b))
        x = xor(pt, b)
        c, l = is_cyclic(x)
        if not c:
            file.close()
            return False
    file.close()
    return True
'''
#print(ct[:10])
#get_more_ct()
#get_more_ct_fromfile(ct)
# 203
#get_more_ct_fromfile(ct2)
# 194
#get_more_ct_fromfile(ct3)
# 133
#brute_char(0)


for c in range(256):
    x = find_combo(c)
    if x:
        print(c, x)

'''
print(len(ct))
print(len(ct2))
x = xor(ct, ct2)

c, l = is_cyclic(x)
print(c, l)
'''
#print(is_cyclic_l(b'012345678912012345678912', 12))

#c, l = is_cyclic(b'012345678912012345678912012')
#print(c, l)

'''
for x in range(2, 512, 2):
	pt = xor(binascii.unhexlify(ct[:x]), binascii.unhexlify(ct[x:x+x]))
	print(pt)
'''
